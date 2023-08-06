# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the data drift logic between two datasets, relies on the DataSets API."""

import warnings
from datetime import timezone, datetime, timedelta

from azureml.core import Dataset, Experiment, Run
from azureml.core.compute import AmlCompute, ComputeTarget
from azureml.core.workspace import Workspace
from azureml.datadrift import alert_configuration
from azureml.datadrift._logging._telemetry_logger import _TelemetryLogger
from azureml.datadrift._logging._telemetry_logger_context_adapter import \
    _TelemetryLoggerContextAdapter
from azureml.datadrift._restclient import DataDriftClient
from azureml.datadrift._restclient.api_versions import PUBLICPREVIEW
from azureml.datadrift._restclient.models import (AlertConfiguration, CreateDataDriftDto, CreateDataDriftRunDto,
                                                  UpdateDataDriftDto)
from azureml.datadrift._result_handler import _get_metrics_path, _all_outputs, _show
from azureml.datadrift._schedule_state import ScheduleState
from azureml.datadrift._utils.constants import (
    COMPUTE_TARGET_TYPE_AML, RUN_TYPE_ADHOC, RUN_TYPE_BACKFILL, DATADRIFT_TYPE_DATASET,
    DATADRIFT_TYPE_MODEL, DATADRIFT_CONSTRUCTOR, DATADRIFT_CREATE, DATADRIFT_CREATE_FROM_MODEL,
    DATADRIFT_CREATE_FROM_DATASET, DATADRIFT_GET, DATADRIFT_GET_BY_NAME, DATADRIFT_LIST,
    DATADRIFT_RUN, DATADRIFT_ENABLE_SCHEDULE, DATADRIFT_DISABLE_SCHEDULE, DATADRIFT_UPDATE,
    DATADRIFT_BACKFILL, DATADRIFT_GET_OUTPUT, DATADRIFT_SHOW, DATADRIFT_IN_PROGRESS_MSG,
    DEFAULT_LOOKBACK_CYCLES
)
from azureml.exceptions import ComputeTargetException
from azureml.pipeline.core import Schedule
from dateutil.relativedelta import relativedelta
from msrest.exceptions import HttpOperationError

from ._utils.parameter_validator import ParameterValidator

module_logger = _TelemetryLogger.get_telemetry_logger(__name__)

DEFAULT_COMPUTE_TARGET_NAME = "datadrift-server"
DEFAULT_VM_SIZE = "STANDARD_D2_V2"
DEFAULT_VM_MAX_NODES = 4
DEFAULT_DRIFT_THRESHOLD = 0.2


class DataDriftDetector:
    """Class for Azure ML DataDriftDetector.

    The DataDriftDetector class provides a set of APIs to identify drift between a given baseline and target dataset.
    A DataDriftDetector object is created with a workspace, and either specifying the baseline and target datasets
    directly or having them inferred from a model name, version, and whitelist of webservice endpoints. See
    https://aka.ms/datadrift for documentation.
    """

    def __init__(self, workspace, model_name, model_version):
        """Datadriftdetector constructor.

        The DataDriftDetector constructor is used to retrieve a cloud representation of a DataDriftDetector object
        associated with the provided workspace. Must provide model_name and model_version.

        :param workspace: Object that points to workspace
        :type workspace: azureml.core.workspace.Workspace
        :param model_name: Name of model to run DataDriftDetector on
        :type model_name: str
        :param model_version: Version of model
        :type model_version: int
        :return: A DataDriftDetector object
        :rtype: DataDriftDetector
        """
        if workspace is ... or model_name is ... or model_version is ...:
            # Instantiate an empty DataDriftDetector object. Will be initialized by DataDriftDetector.get()
            return

        log_context = {'workspace_name': workspace.name, 'workspace_id': workspace._workspace_id,
                       'model_name': model_name, 'model_version': model_version,
                       'subscription_id': workspace.subscription_id, 'workspace_location': workspace.location}

        self._logger = _TelemetryLoggerContextAdapter(module_logger, log_context)

        workspace = ParameterValidator.validate_workspace(workspace)
        model_name = ParameterValidator.validate_model_name(model_name)
        model_version = ParameterValidator.validate_model_version(model_version)
        _TelemetryLogger.log_event(DATADRIFT_CONSTRUCTOR, **log_context)
        with _TelemetryLogger.log_activity(self._logger, activity_name="constructor") as logger:

            try:
                dd_list = DataDriftDetector._get_datadrift_list(workspace, model_name=model_name,
                                                                model_version=model_version, logger=logger)
                if len(dd_list) > 1:
                    error_msg = "Multiple DataDriftDetector objects for: {} {} {}".format(workspace, model_name,
                                                                                          model_version)
                    logger.error(error_msg)
                    raise LookupError(error_msg)
                elif len(dd_list) == 1:
                    dto = dd_list[0]
                    self._initialize(workspace, dto)
                else:
                    error_msg = "DataDriftDetector object for model_name: {}, model_version: {} doesn't exist. " \
                                "Create with DatadriftDetector.create_from_model()".format(model_name, model_version)
                    raise KeyError(error_msg)
            except HttpOperationError as e:
                logger.error(e.message)
                raise

    def _initialize(self, workspace, client_dto):
        r"""Class DataDriftDetector Constructor helper.

        :param workspace: Object that points to workspace
        :type workspace: azureml.core.workspace.Workspace
        :param client_dto: DataDrift Client DTO object from service call
        :type client_dto: azureml.datadrift._restclient.models.DataDriftDto
        :return: A DataDriftDetector object
        :rtype: DataDriftDetector
        """
        self._workspace = workspace
        self._frequency = client_dto.frequency
        self._schedule_start = client_dto.schedule_start_time
        self._schedule_id = client_dto.schedule_id
        self._interval = client_dto.interval
        self._state = client_dto.state
        self._alert_config = client_dto.alert_configuration
        self._type = client_dto.type if client_dto.type else DATADRIFT_TYPE_MODEL
        self._id = client_dto.id
        self._model_name = client_dto.model_name
        self._model_version = client_dto.model_version
        self._services = client_dto.services
        self._compute_target_name = client_dto.compute_target_name
        self._drift_threshold = client_dto.drift_threshold
        self._baseline_dataset_id = client_dto.base_dataset_id
        self._target_dataset_id = client_dto.target_dataset_id
        self._feature_list = client_dto.features
        self._latency = client_dto.job_latency
        self._name = client_dto.name
        self._latest_run_time = client_dto.latest_run_time if hasattr(client_dto, 'latest_run_time') else None

        # Set alert configuration
        self._alert_config = alert_configuration.AlertConfiguration(
            client_dto.alert_configuration.email_addresses) if client_dto.alert_configuration else None

        # Instantiate service client
        self._client = DataDriftClient(self.workspace.service_context)

        if not hasattr(self, '_logger'):
            log_context = {
                'workspace_name': workspace.name, 'model_name': client_dto.model_name,
                'model_version': client_dto.model_version, 'dd_id': client_dto.id,
                'workspace_id': workspace._workspace_id, 'workspace_location': workspace.location,
                'subscription_id': workspace.subscription_id}

            self._logger = _TelemetryLoggerContextAdapter(module_logger, log_context)

    def __repr__(self):
        """Return the string representation of a DataDriftDetector object.

        :return: DataDriftDetector object string
        :rtype: str
        """
        return str(self.__dict__)

    @property
    def workspace(self):
        """Get the workspace of the DataDriftDetector object.

        :return: Workspace object
        :rtype: azureml.core.workspace.Workspace
        """
        return self._workspace

    @property
    def name(self):
        """Get the name of the DataDriftDetector object.

        :return: DataDriftDetector name
        :rtype: str
        """
        return self._name

    @property
    def model_name(self):
        """Get the model name associated with the DataDriftDetector object.

        Will return None for Dataset Based DataDriftDetectors.

        :return: Model name
        :rtype: str
        """
        return self._model_name

    @property
    def model_version(self):
        """Get the model version associated with the DataDriftDetector object.

        Will return None for Dataset Based DataDriftDetectors.

        :return: Model version
        :rtype: int
        """
        return self._model_version

    @property
    def services(self):
        """Get the list of services attached to the DataDriftDetector object.

        :return: List of service names
        :rtype: builtin.list[str]
        """
        return self._services

    @property
    def compute_target(self):
        """Get the Compute Target attached to the DataDriftDetector object.

        :return: Compute Target
        :rtype: azureml.core.ComputeTarget
        """
        return self._get_compute_target(self._compute_target_name)

    @property
    def frequency(self):
        """Get the frequency of the DataDriftDetector schedule.

        :return: String of either "Day", "Week" or "Month"
        :rtype: str
        """
        return self._frequency

    @property
    def interval(self):
        """Get the interval of the DataDriftDetector schedule.

        :return: Integer value of time unit
        :rtype: int
        """
        return self._interval

    @property
    def feature_list(self):
        """Get the list of whitelisted features for the DataDriftDetector object.

        :return: List of feature names
        :rtype: builtin.list[str]
        """
        return self._feature_list

    @property
    def drift_threshold(self):
        """Get the drift threshold for the DataDriftDetector object.

        :return: Drift threshold
        :rtype: float
        """
        return self._drift_threshold

    @property
    def baseline_dataset(self):
        """Get the baseline dataset. Will return None for Model Based DataDriftDetectors.

        :return: Dataset type of the baseline dataset
        :rtype: azureml.data.tabular_dataset.TabularDataset
        """
        return Dataset.get_by_id(self.workspace, self._baseline_dataset_id)

    @property
    def target_dataset(self):
        """Get the target dataset.  Will return None for Model Based DataDriftDetectors.

        :return: Dataset type of the baseline dataset
        :rtype: azureml.data.tabular_dataset.TabularDataset
        """
        return Dataset.get_by_id(self.workspace, self._target_dataset_id)

    @property
    def schedule_start(self):
        """Get the start time of the schedule.

        :return: Datetime object of schedule start time in UTC
        :rtype: datetime.datetime
        """
        return self._schedule_start

    @property
    def alert_config(self):
        """Get the alert configuration for the DataDriftDetector object.

        :return: AlertConfiguration object.
        :rtype: azureml.datadrift.AlertConfiguration
        """
        return self._alert_config

    @property
    def state(self):
        """Denotes the state of the DataDriftDetector schedule.

        :return: One of 'Disabled', 'Enabled', 'Disabling', 'Enabling'
        :rtype: str
        """
        return self._state

    @property
    def enabled(self):
        """Get the boolean value for whether the DataDriftDetector is enabled or not.

        :return: Boolean value; true for enabled
        :rtype: bool
        """
        return self._state == ScheduleState.Enabled.name

    @property
    def latency(self):
        """Get the latency of the DataDriftDetector schedule jobs (in hours).

        :return: Number of hours
        :rtype: int
        """
        return self._latency

    @property
    def drift_type(self):
        """Get the type of the DataDriftDetector, either 'ModelBased' or 'DatasetBased'.

        :return: Type of DataDriftDetector
        :rtype: str
        """
        return self._type

    @staticmethod
    def create(workspace, model_name, model_version, services, compute_target=None, frequency=None, interval=None,
               feature_list=None, schedule_start=None, alert_config=None, drift_threshold=None):
        r"""Create a new DataDriftDetector object in the Azure Machine Learning Workspace.

        Throws an exception if a DataDriftDetector for the same model_name and model_version already exists in the
        workspace. **NOTE:** This is deprecated and will be removed from future versions. Please use
        :meth:`azureml.datadrift.DataDriftDetector.create_from_model`

        .. remarks::
            Model-based DataDriftDetectors enable users to calculate data drift between a model's training dataset and
            its scoring dataset. There can only be one DataDriftDetector for a specific model name and version, however
            the services list can be updated after creating the DataDriftDetector object. The model training dataset
            can be specified during model registration.

            .. code-block::python

                from azureml.core import Workspace, Dataset
                from azureml.datadrift import DataDriftDetector

                ws = Workspace.from_config()

                detector = DataDriftDetector.create(workspace=ws,
                                                    model_name="my_model",
                                                    model_version=1,
                                                    services=["my_services"],
                                                    compute_target_name='my_compute_target',
                                                    frequency="Day",
                                                    feature_list=['my_feature_1', 'my_feature_2'],
                                                    alert_config=AlertConfiguration(email_addresses=['user@contoso.com']),
                                                    drift_threshold=0.3)

        :param workspace: Object that points to workspace
        :type workspace: azureml.core.workspace.Workspace
        :param model_name: Name of model to run DataDriftDetector on
        :type model_name: str
        :param model_version: Version of model
        :type model_version: int
        :param services: Optional, list of AzureML webservices to run DataDriftDetector schedule
        :type services: builtin.list[str]
        :param compute_target: Optional, AzureML ComputeTarget or ComputeTarget name; DataDriftDetector will create one
                               if none specified
        :type compute_target: azureml.core.ComputeTarget or str
        :param frequency: Optional, how often the pipeline is run. Supports "Day", "Week" or "Month"
        :type frequency: str
        :param interval: Optional, how often the pipeline runs based on frequency. i.e. If frequency = "Day" and \
                         interval = 2, the pipeline will run every other day
        :type interval: int
        :param feature_list: Optional, whitelisted features to run the datadrift detection on. DataDriftDetector jobs
                             will run on all features if no feature_list is specified.
        :type feature_list: builtin.list[str]
        :param schedule_start: Optional, start time of data drift schedule in UTC. Current time used if None specified
        :type schedule_start: datetime.datetime
        :param alert_config: Optional, configuration object for DataDriftDetector alerts
        :type alert_config: azureml.datadrift.AlertConfiguration
        :param drift_threshold: Optional, threshold to enable DataDriftDetector alerts on. Defaults to 0.2
        :type drift_threshold: float
        :return: A DataDriftDetector object
        :rtype: azureml.datadrift.DataDriftDetector
        """
        logger = _TelemetryLogger.get_telemetry_logger('datadriftdetector.create')
        log_context = {'workspace_name': workspace.name, 'workspace_id': workspace._workspace_id,
                       'model_name': model_name, 'model_version': model_version,
                       'subscription_id': workspace.subscription_id, 'workspace_location': workspace.location}

        logger = _TelemetryLoggerContextAdapter(logger, log_context)
        _TelemetryLogger.log_event(DATADRIFT_CREATE, **log_context)
        with _TelemetryLogger.log_activity(logger, activity_name="datadriftdetector.create") as logger:
            logger.warning("Deprecated, please use create_from_model(). Will be removed in future releases.")
            return DataDriftDetector.create_from_model(workspace, model_name, model_version, services, compute_target,
                                                       frequency, interval, feature_list, schedule_start, alert_config,
                                                       drift_threshold)

    @staticmethod
    def create_from_model(workspace, model_name, model_version, services, compute_target=None,
                          frequency=None, interval=None, feature_list=None, schedule_start=None, alert_config=None,
                          drift_threshold=None):
        r"""Create a new DataDriftDetector object in the Azure Machine Learning Workspace.

        Throws an exception if a DataDriftDetector for the same model_name and model_version already exists in the
        workspace.

        .. remarks::
            Model-based DataDriftDetectors enable users to calculate data drift between a model's training dataset and
            its scoring dataset. There can only be one DataDriftDetector for a specific model name and version, however
            the services list can be updated after creating the DataDriftDetector object. The model training dataset
            can be specified during model registration.

            .. code-block::python

                from azureml.core import Workspace, Dataset
                from azureml.datadrift import DataDriftDetector

                ws = Workspace.from_config()

                detector = DataDriftDetector.create_from_model(workspace=ws,
                                                               model_name="my_model",
                                                               model_version=1,
                                                               services=["my_services"],
                                                               compute_target_name='my_compute_target',
                                                               frequency="Day",
                                                               feature_list=['my_feature_1', 'my_feature_2'],
                                                               alert_config=AlertConfiguration(email_addresses=['user@contoso.com']),
                                                               drift_threshold=0.3)

        :param workspace: Object that points to workspace
        :type workspace: azureml.core.workspace.Workspace
        :param model_name: Name of model to run DataDriftDetector on
        :type model_name: str
        :param model_version: Version of model
        :type model_version: int
        :param services: Optional, list of AzureML webservices to run DataDriftDetector schedule
        :type services: builtin.list[str]
        :param compute_target: Optional, AzureML ComputeTarget or ComputeTarget name; DataDriftDetector will create one
                               if none specified
        :type compute_target: azureml.core.ComputeTarget or str
        :param frequency: Optional, how often the pipeline is run. Supports "Day", "Week" or "Month"
        :type frequency: str
        :param interval: Optional, how often the pipeline runs based on frequency. i.e. If frequency = "Day" and \
                         interval = 2, the pipeline will run every other day
        :type interval: int
        :param feature_list: Optional, whitelisted features to run the datadrift detection on. DataDriftDetector jobs
                             will run on all features if no feature_list is specified.
        :type feature_list: builtin.list[str]
        :param schedule_start: Optional, start time of data drift schedule in UTC. Current time used if None specified
        :type schedule_start: datetime.datetime
        :param alert_config: Optional, configuration object for DataDriftDetector alerts
        :type alert_config: azureml.datadrift.AlertConfiguration
        :param drift_threshold: Optional, threshold to enable DataDriftDetector alerts on. Defaults to 0.2
        :type drift_threshold: float
        :return: A DataDriftDetector object
        :rtype: azureml.datadrift.DataDriftDetector
        """
        workspace = ParameterValidator.validate_workspace(workspace)
        model_name = ParameterValidator.validate_model_name(model_name)
        model_version = ParameterValidator.validate_model_version(model_version)
        services = ParameterValidator.validate_services(services)
        compute_target = ParameterValidator.validate_compute_target(compute_target, workspace)
        frequency = ParameterValidator.validate_frequency(frequency)
        interval = ParameterValidator.validate_interval(interval)
        feature_list = ParameterValidator.validate_feature_list(feature_list)
        schedule_start = ParameterValidator.validate_datetime(schedule_start)
        alert_config = ParameterValidator.validate_alert_configuration(alert_config)
        drift_threshold = ParameterValidator.validate_drift_threshold(drift_threshold)

        logger = _TelemetryLogger.get_telemetry_logger('datadriftdetector.create_from_model')
        log_context = {'workspace_name': workspace.name, 'workspace_id': workspace._workspace_id,
                       'model_name': model_name, 'model_version': model_version,
                       'subscription_id': workspace.subscription_id, 'workspace_location': workspace.location}

        logger = _TelemetryLoggerContextAdapter(logger, log_context)
        _TelemetryLogger.log_event(DATADRIFT_CREATE_FROM_MODEL, **log_context)
        with _TelemetryLogger.log_activity(logger, activity_name="datadriftdetector.create_from_model") as logger:

            dd_client = DataDriftClient(workspace.service_context)

            try:
                if list(dd_client.list(model_name, model_version, logger=logger)):
                    error_msg = "DataDriftDetector already exists for model_name: {}, model_version: {}. Please use " \
                                "DataDriftDetector.get() to retrieve the object".format(model_name, model_version)
                    raise KeyError(error_msg)
            except HttpOperationError as e:
                logger.error(e.message)
                raise

            if not compute_target:
                # Set to default workspace compute if it exists
                compute_target = DataDriftDetector._get_default_compute_target(workspace)

            if isinstance(compute_target, ComputeTarget):
                compute_target = compute_target.name

            if not drift_threshold:
                drift_threshold = DEFAULT_DRIFT_THRESHOLD

            # Write object to service
            dto = CreateDataDriftDto(frequency=frequency,
                                     schedule_start_time=schedule_start.replace(tzinfo=timezone.utc).isoformat()
                                     if schedule_start else None,
                                     interval=interval,
                                     alert_configuration=AlertConfiguration(
                                         email_addresses=alert_config.email_addresses)
                                     if alert_config else None,
                                     model_name=model_name,
                                     model_version=model_version,
                                     services=services,
                                     compute_target_name=compute_target,
                                     drift_threshold=drift_threshold,
                                     features=feature_list,
                                     type=DATADRIFT_TYPE_MODEL)
            client_dto = dd_client.create(dto, logger)
            DataDriftDetector._validate_client_dto(client_dto, logger)

            dd = DataDriftDetector(..., ..., ...)
            dd._initialize(workspace, client_dto)
            return dd

    @staticmethod
    def create_from_datasets(workspace, name, baseline_dataset, target_dataset, compute_target=None,
                             frequency=None, feature_list=None, alert_config=None, drift_threshold=None, latency=None):
        """Create a new DataDriftDetector object from a baseline tabular dataset and a target timeseries dataset.

        .. remarks::
            Dataset-based DataDriftDetectors enable users to calculate data drift between a baseline dataset, which
            must be a :class:`azureml.data.tabular_dataset.TabularDataset`, and a target dataset, which must be a
            time-series dataset. A time-series dataset is simply a :class:`azureml.data.tabular_dataset.TabularDataset`
            with the fine_grain_timestamp property. The DataDriftDetector can then run adhoc or scheduled jobs to
            determine if the target dataset has drifted from the baseline dataset.

            .. code-block::python

                from azureml.core import Workspace, Dataset
                from azureml.datadrift import DataDriftDetector

                ws = Workspace.from_config()
                baseline = Dataset.get_by_name(ws, 'my_baseline_dataset')
                target = Dataset.get_by_name(ws, 'my_target_dataset')

                detector = DataDriftDetector.create_from_datasets(workspace=ws,
                                                                  name="my_unique_detector_name",
                                                                  baseline_dataset=baseline,
                                                                  target_dataset=target,
                                                                  compute_target_name='my_compute_target',
                                                                  frequency="Day",
                                                                  feature_list=['my_feature_1', 'my_feature_2'],
                                                                  alert_config=AlertConfiguration(email_addresses=['user@contoso.com']),
                                                                  drift_threshold=0.3,
                                                                  latency=1)

        :param workspace: Object that points to workspace
        :type workspace: azureml.core.workspace.Workspace
        :param name: Unique name of the DataDriftDetector object
        :type name: str
        :param baseline_dataset: Dataset to compare the target dataset against
        :type baseline_dataset: azureml.data.tabular_dataset.TabularDataset
        :param target_dataset: Dataset to run either adhoc or scheduled DataDrift jobs for. Must be Time Series
        :type target_dataset: azureml.data.tabular_dataset.TabularDataset
        :param compute_target: Optional, AzureML ComputeTarget or ComputeTarget name; DataDriftDetector will create one
                               if none specified
        :type compute_target: azureml.core.ComputeTarget or str
        :param frequency: Optional, how often the pipeline is run. Supports "Day", "Week" or "Month"
        :type frequency: str
        :param feature_list: Optional, whitelisted features to run the datadrift detection on. DataDriftDetector jobs
                             will run on all features if no feature_list is specified.
        :type feature_list: builtin.list[str]
        :param alert_config: Optional, configuration object for DataDriftDetector alerts
        :type alert_config: azureml.datadrift.AlertConfiguration
        :param drift_threshold: Optional, threshold to enable DataDriftDetector alerts on. Defaults to 0.2
        :type drift_threshold: float
        :param latency: Delay (hours) for data to appear in dataset
        :type latency: int
        :return: A DataDriftDetector object
        :rtype: azureml.datadrift.DataDriftDetector
        """
        workspace = ParameterValidator.validate_workspace(workspace)
        name = ParameterValidator.validate_name(name)
        baseline_dataset = ParameterValidator.validate_dataset(baseline_dataset)
        target_dataset = ParameterValidator.validate_timeseries_dataset(target_dataset)
        frequency = ParameterValidator.validate_frequency(frequency, dataset_based=True)
        feature_list = ParameterValidator.validate_feature_list(feature_list)
        drift_threshold = ParameterValidator.validate_drift_threshold(drift_threshold)
        compute_target = ParameterValidator.validate_compute_target(compute_target, workspace)
        alert_config = ParameterValidator.validate_alert_configuration(alert_config)
        latency = ParameterValidator.validate_latency(latency)

        logger = _TelemetryLogger.get_telemetry_logger('datadriftdetector.create_from_datasets')
        log_context = {'workspace_name': workspace.name, 'workspace_id': workspace._workspace_id,
                       'baseline_dataset': baseline_dataset.id, 'target_dataset': target_dataset.id,
                       'subscription_id': workspace.subscription_id, 'workspace_location': workspace.location}

        logger = _TelemetryLoggerContextAdapter(logger, log_context)
        _TelemetryLogger.log_event(DATADRIFT_CREATE_FROM_DATASET, **log_context)
        with _TelemetryLogger.log_activity(logger, activity_name="datadriftdetector.create_from_datasets") as logger:

            dd_client = DataDriftClient(workspace.service_context)

            try:
                temp_dd = DataDriftDetector._get_datadrift_by_name(workspace, name)
                if temp_dd:
                    msg = "DataDriftDetector with name {} already exists. Please use get_by_name() to " \
                          "retrieve it".format(name)
                    logger.error(msg)
                    raise KeyError(msg)
            except HttpOperationError as e:
                # DataDriftDetector object doesn't exist with specified name, creating...
                if e.response.status_code == 404:
                    logger.warning("DataDriftDetector with name: {} does not exist. Creating...".format(name))
                    pass
                else:
                    logger.error(e)

            if not compute_target:
                # Set to default workspace compute if it exists
                compute_target = DataDriftDetector._get_default_compute_target(workspace)

            if isinstance(compute_target, ComputeTarget):
                compute_target = compute_target.name

            if not drift_threshold:
                drift_threshold = DEFAULT_DRIFT_THRESHOLD

            # Ensure that datasets are saved to the workspace
            baseline_dataset._ensure_saved(workspace)
            target_dataset._ensure_saved(workspace)

            # Write object to service
            dto = CreateDataDriftDto(frequency=frequency,
                                     schedule_start_time=None,
                                     interval=1,
                                     alert_configuration=AlertConfiguration(
                                         email_addresses=alert_config.email_addresses)
                                     if alert_config else None,
                                     type=DATADRIFT_TYPE_DATASET,
                                     compute_target_name=compute_target,
                                     drift_threshold=drift_threshold,
                                     base_dataset_id=baseline_dataset.id,
                                     target_dataset_id=target_dataset.id,
                                     features=feature_list,
                                     job_latency=latency,
                                     name=name)
            client_dto = dd_client.create(dto, logger)
            DataDriftDetector._validate_client_dto(client_dto, logger)

            dd = DataDriftDetector(..., ..., ...)
            dd._initialize(workspace, client_dto)
            return dd

    @staticmethod
    def get(workspace, model_name, model_version):
        """Retrieve a unique DataDriftDetector object for a given workspace, model_name and model_version.

        :param workspace: Object that points to the workspace
        :type workspace: azureml.core.workspace.Workspace
        :param model_name: Name of model to run DataDriftDetector on
        :type model_name: str
        :param model_version: Version of model
        :type model_version: int
        :return: DataDriftDetector object
        :rtype: azureml.datadrift.DataDriftDetector
        """
        workspace = ParameterValidator.validate_workspace(workspace)
        model_name = ParameterValidator.validate_model_name(model_name)
        model_version = ParameterValidator.validate_model_version(model_version)

        logger = _TelemetryLogger.get_telemetry_logger('datadriftdetector.get')
        log_context = {'workspace_name': workspace.name, 'workspace_id': workspace._workspace_id,
                       'model_name': model_name, 'model_version': model_version,
                       'subscription_id': workspace.subscription_id, 'workspace_location': workspace.location}
        logger = _TelemetryLoggerContextAdapter(logger, log_context)
        _TelemetryLogger.log_event(DATADRIFT_GET, **log_context)
        with _TelemetryLogger.log_activity(logger, activity_name="get") as logger:
            logger.info("Getting DataDriftDetector object for: {} {} {}".format(workspace, model_name, model_version))
            return DataDriftDetector(workspace, model_name, model_version)

    @staticmethod
    def get_by_name(workspace, name):
        """Retrieve a unique DataDriftDetector object for a given workspace and name.

        :param workspace: Object that points to the workspace
        :type workspace: azureml.core.workspace.Workspace
        :param name: Unique name of the DataDriftDetector object
        :type name: str
        :return: DataDriftDetector object
        :rtype: azureml.datadrift.DataDriftDetector
        """
        workspace = ParameterValidator.validate_workspace(workspace)
        name = ParameterValidator.validate_name(name)

        logger = _TelemetryLogger.get_telemetry_logger('datadriftdetector.get_by_name')
        log_context = {'workspace_name': workspace.name, 'workspace_id': workspace._workspace_id,
                       'name': name, 'subscription_id': workspace.subscription_id,
                       'workspace_location': workspace.location}
        logger = _TelemetryLoggerContextAdapter(logger, log_context)
        _TelemetryLogger.log_event(DATADRIFT_GET_BY_NAME, **log_context)
        with _TelemetryLogger.log_activity(logger, activity_name="get_by_name") as logger:
            logger.info("Getting DataDriftDetector object with name: {} in workspace: {}".format(name, workspace))
            try:
                client_dto = DataDriftDetector._get_datadrift_by_name(workspace, name, logger)
            except HttpOperationError:
                error_msg = "Could not find DataDriftDetector with name: {}".format(name)
                logger.error(error_msg)
                raise KeyError(error_msg)
            dd = DataDriftDetector(..., ..., ...)
            dd._initialize(workspace, client_dto)

            return dd

    @staticmethod
    def list(workspace, model_name=None, model_version=None, baseline_dataset=None, target_dataset=None):
        """Get a list of DataDriftDetector objects given a workspace.

        For Model Based DataDriftDetectors, pass in `model_name` and/or `model_version`, for Dataset Based
        DataDriftDetectors, pass in ``baseline_dataset`` and/or ``target_dataset``. NOTE: Model Based optional
        parameters cannot be mixed with Dataset Based optional parameters. Passing in only workspace will return all
        DataDriftDetector objects, both Model Based and Dataset Based, from the workspace.

        :param workspace: Object that points to the workspace
        :type workspace: azureml.core.workspace.Workspace
        :param model_name: Optional, name of model to run DataDriftDetector on
        :type model_name: str
        :param model_version: Optional, version of model
        :type model_version: int
        :param baseline_dataset: Dataset to compare the target dataset against
        :type baseline_dataset: azureml.data.tabular_dataset.TabularDataset
        :param target_dataset: Dataset to run either adhoc or scheduled DataDrift jobs for. Must be Time Series
        :type target_dataset: azureml.data.tabular_dataset.TabularDataset
        :return: List of DataDriftDetector objects
        :rtype: :class:list(azureml.datadrift.DataDriftDetector)
        """
        workspace = ParameterValidator.validate_workspace(workspace)
        if model_name is not None:
            model_name = ParameterValidator.validate_model_name(model_name)
        if model_version is not None:
            model_version = ParameterValidator.validate_model_version(model_version)

        baseline_dataset = ParameterValidator.validate_dataset(baseline_dataset, none_ok=True)
        target_dataset = ParameterValidator.validate_dataset(target_dataset, none_ok=True)

        # Ensure Model Based and Dataset Based params are not arguments
        if model_name or model_version:
            if baseline_dataset or target_dataset:
                raise TypeError("Cannot have both Model Based and Dataset Based arguments")

        logger = _TelemetryLogger.get_telemetry_logger('datadriftdetector.list')
        log_context = {'workspace_name': workspace.name, 'workspace_id': workspace._workspace_id,
                       'model_name': model_name, 'model_version': model_version,
                       'subscription_id': workspace.subscription_id, 'workspace_location': workspace.location}
        if baseline_dataset:
            log_context['baseline_dataset'] = baseline_dataset.id
        if target_dataset:
            log_context['target_dataset'] = target_dataset.id
        logger = _TelemetryLoggerContextAdapter(logger, log_context)
        _TelemetryLogger.log_event(DATADRIFT_LIST, **log_context)
        with _TelemetryLogger.log_activity(logger, activity_name="list") as logger:
            try:
                dto_list = DataDriftDetector._get_datadrift_list(workspace, model_name=model_name,
                                                                 model_version=model_version,
                                                                 baseline_dataset=baseline_dataset,
                                                                 target_dataset=target_dataset, logger=logger)
            except HttpOperationError as e:
                logger.error(e.message)
                raise
            dd_list = []
            for client_dto in dto_list:
                dd = DataDriftDetector(..., ..., ...)
                dd._initialize(workspace, client_dto)
                dd_list.append(dd)
            return dd_list

    @staticmethod
    def _get_default_compute_target(workspace):
        """If the Workspace default compute target exists retrieve its name, or return the default compute target name.

        :param workspace: Object that points to the workspace
        :type workspace: azureml.core.workspace.Workspace
        :return: Compute target name
        :rtype: str
        """
        if workspace.get_default_compute_target('CPU'):
            return workspace.get_default_compute_target('CPU').name

        DataDriftDetector._create_aml_compute(workspace, DEFAULT_COMPUTE_TARGET_NAME)
        return DEFAULT_COMPUTE_TARGET_NAME

    @staticmethod
    def _get_datadrift_list(workspace, model_name=None, model_version=None, baseline_dataset=None, target_dataset=None,
                            services=None, logger=None, client=None):
        """Get list of DataDriftDetector objects from service.

        :param workspace: Object that points to the workspace
        :type workspace: azureml.core.workspace.Workspace
        :param model_name: Optional, name of model to run DataDriftDetector on
        :type model_name: str
        :param model_version: Optional, version of model
        :type model_version: int
        :param services: Optional, names of webservices
        :type services: builtin.list[str]
        :param baseline_dataset: Dataset to compare the target dataset against
        :type baseline_dataset: azureml.data.tabular_dataset.TabularDataset
        :param target_dataset: Dataset to run either adhoc or scheduled DataDrift jobs for. Must be Time Series
        :type target_dataset: azureml.data.tabular_dataset.TabularDataset
        :param logger: Activity logger for service call
        :type logger: datetime.datetime
        :param client: DataDriftDetector service client
        :type client: azureml.datadrift._restclient.DataDriftClient
        :return: List of DataDriftDetector objects
        :rtype: list(azureml.datadrift._restclient.models.DataDriftDto)
        """
        dd_client = client if client else DataDriftClient(workspace.service_context)

        baseline_dataset_id = baseline_dataset.id if baseline_dataset else None
        target_dataset_id = target_dataset.id if target_dataset else None

        return list(dd_client.list(model_name=model_name, model_version=model_version, services=services,
                                   base_dataset_id=baseline_dataset_id, target_dataset_id=target_dataset_id,
                                   logger=logger))

    @staticmethod
    def _get_datadrift_by_name(workspace, name, logger=None, client=None):
        """Get list of DataDriftDetector objects from service.

        :param workspace: Object that points to the workspace
        :type workspace: azureml.core.workspace.Workspace
        :param name: Unique name of the DataDriftDetector object
        :param logger: Activity logger for service call
        :type logger: datetime.datetime
        :param client: DataDriftDetector service client
        :type client: azureml.datadrift._restclient.DataDriftClient
        :return: List of DataDriftDetector objects
        :rtype: list(azureml.datadrift._restclient.models.DataDriftDto)
        """
        dd_client = client if client else DataDriftClient(workspace.service_context)

        return dd_client.get_by_name(name=name, logger=logger)

    @staticmethod
    def _create_aml_compute(workspace, name):
        """Create an aml compute using name.

        Create a new one.

        :param workspace: Object that points to the workspace
        :type workspace: azureml.core.workspace.Workspace
        :param name: the name of aml compute target
        :type name: str
        :return: Azure ML Compute target
        :rtype: azureml.core.compute.compute.AmlCompute
        """
        log_context = {'workspace_name': workspace.name, 'subscription_id': workspace.subscription_id,
                       'workspace_location': workspace.location}
        # TODO: De-provision compute if it's not run
        module_logger.info("creating new compute target: {}".format(name), extra={'properties': log_context})

        if name == Workspace.DEFAULT_CPU_CLUSTER_NAME:
            # Use AzureML default aml compute config
            aml_compute = AmlCompute.create(workspace,
                                            Workspace.DEFAULT_CPU_CLUSTER_NAME,
                                            Workspace.DEFAULT_CPU_CLUSTER_CONFIGURATION)
        else:
            provisioning_config = AmlCompute.provisioning_configuration(
                vm_size=DEFAULT_VM_SIZE,
                max_nodes=DEFAULT_VM_MAX_NODES
            )
            aml_compute = AmlCompute.create(workspace, name, provisioning_config)

        aml_compute.wait_for_completion(show_output=True)
        return aml_compute

    def run(self, target_date, services=None, compute_target=None, create_compute_target=False, feature_list=None,
            drift_threshold=None):
        """Run a single point in time data drift analysis.

        :param services: Optional, If Model Based, list of webservices to run DataDrift job on.
                         Not needed for Dataset Based DataDriftDetectors.
        :type services: builtin.list[str]
        :param target_date:  Target date of scoring data in UTC
        :type target_date: datetime.datetime
        :param compute_target: Optional, AzureML ComputeTarget or ComputeTarget name; DataDriftDetector will create one
                               if none specified
        :type compute_target: azureml.core.ComputeTarget or str
        :param create_compute_target: Optional, whether the DataDriftDetector API should automatically create an AML
                                      compute target. Default to False.
        :type create_compute_target: bool
        :param feature_list: Optional, whitelisted features to run the datadrift detection on
        :type feature_list: builtin.list[str]
        :param drift_threshold: Optional, threshold to enable DataDriftDetector alerts on
        :type drift_threshold: float
        :return: DataDriftDetector run
        :rtype: azureml.core.run.Run
        """
        target_date = ParameterValidator.validate_datetime(target_date)
        if services and self.drift_type == DATADRIFT_TYPE_DATASET:
            raise TypeError("This DataDriftDetector is {}, please remove the services parameter".format(
                self.drift_type))
        services = ParameterValidator.validate_services(services, none_ok=True)
        compute_target = ParameterValidator.validate_compute_target(compute_target, self.workspace,
                                                                    not_exist_ok=create_compute_target)
        feature_list = ParameterValidator.validate_feature_list(feature_list)
        drift_threshold = ParameterValidator.validate_drift_threshold(drift_threshold)
        _TelemetryLogger.log_event(DATADRIFT_RUN, **self._logger.context)
        with _TelemetryLogger.log_activity(self._logger, activity_name="run") as logger:
            if not compute_target:
                # Fallback to object's compute target
                compute_target = self.compute_target

            if not drift_threshold:
                # Fallback to object's drift threshold
                drift_threshold = self.drift_threshold

            if not feature_list:
                # Fallback to object's feature list
                feature_list = self.feature_list

            if not services:
                # Fallback to object's services
                services = self.services

            if isinstance(compute_target, str):
                compute_target = self._get_compute_target(compute_target_name=compute_target,
                                                          create_compute_target=create_compute_target, logger=logger)

            if isinstance(compute_target, ComputeTarget):
                compute_target = compute_target.name

            dto = CreateDataDriftRunDto(services=services,
                                        compute_target_name=compute_target,
                                        start_time=target_date.replace(tzinfo=timezone.utc).isoformat(),
                                        features=feature_list,
                                        drift_threshold=drift_threshold,
                                        run_type=RUN_TYPE_ADHOC)
            try:
                run_dto = self._client.run(self._id, dto, logger, api_version=PUBLICPREVIEW)
            except HttpOperationError as e:
                logger.error(e.message)
                raise

            exp = Experiment(self.workspace, run_dto.data_drift_id)
            run = Run(experiment=exp, run_id=run_dto.execution_run_id)
            return run

    def backfill(self, start_date, end_date, compute_target=None, create_compute_target=False):
        """Run a backfill job over a given specified start_date and end_date.

        See https://aka.ms/datadrift for details on data drift backfill runs. *NOTE*: Backfill is only supported on
        Dataset Based DataDriftDetector objects.

        :param start_date:  Date to start the backfill job on
        :type start_date: datetime.datetime
        :param end_date:  End date of backfill job, inclusive
        :type end_date: datetime.datetime
        :param compute_target: Optional, AzureML ComputeTarget or ComputeTarget name; DataDriftDetector will create one
                               if none specified
        :type compute_target: azureml.core.ComputeTarget or str
        :param create_compute_target: Optional, whether the DataDriftDetector API should automatically create an AML
                                      compute target. Default to False.
        :type create_compute_target: bool
        :return: DataDriftDetector run
        :rtype: azureml.core.run.Run
        """
        start_date, end_date = ParameterValidator.validate_start_date_end_date(start_date, end_date, self.frequency)

        if self.drift_type == DATADRIFT_TYPE_MODEL:
            raise TypeError("Cannot run backfill on Model Based DataDriftDetector, please use run().")
        compute_target = ParameterValidator.validate_compute_target(compute_target, self.workspace,
                                                                    not_exist_ok=create_compute_target)
        _TelemetryLogger.log_event(DATADRIFT_BACKFILL, **self._logger.context)
        with _TelemetryLogger.log_activity(self._logger, activity_name="backfill") as logger:
            if not compute_target:
                # Fallback to object's compute target
                compute_target = self.compute_target

            if isinstance(compute_target, str):
                compute_target = self._get_compute_target(compute_target_name=compute_target,
                                                          create_compute_target=create_compute_target, logger=logger)

            if isinstance(compute_target, ComputeTarget):
                compute_target = compute_target.name

            dto = CreateDataDriftRunDto(compute_target_name=compute_target,
                                        start_time=start_date.replace(tzinfo=timezone.utc).isoformat(),
                                        end_time=end_date.replace(tzinfo=timezone.utc).isoformat(),
                                        run_type=RUN_TYPE_BACKFILL)

            try:
                run_dto = self._client.run(self._id, dto, logger, api_version=PUBLICPREVIEW)
            except HttpOperationError as e:
                logger.error(e.message)
                raise

            exp = Experiment(self.workspace, run_dto.data_drift_id)
            run = Run(experiment=exp, run_id=run_dto.execution_run_id)
            return run

    def enable_schedule(self, create_compute_target=False):
        """Create a schedule to run either a Model Based or Dataset Based DataDriftDetector job.

        :param create_compute_target: Optional, whether the DataDriftDetector API should automatically create an AML
                                      compute target. Default to False.
        :type create_compute_target: bool
        """
        _TelemetryLogger.log_event(DATADRIFT_ENABLE_SCHEDULE, **self._logger.context)
        with _TelemetryLogger.log_activity(self._logger, activity_name="enable_schedule") as logger:
            # TODO: Add check for baseline dataset property being set
            compute_target = self._get_compute_target(self.compute_target.name, create_compute_target, logger)
            compute_target_type = compute_target.type
            if compute_target_type != COMPUTE_TARGET_TYPE_AML:
                raise AttributeError(
                    "Compute target {} must be of type {} while it is {}".format(
                        self.compute_target.name,
                        COMPUTE_TARGET_TYPE_AML,
                        compute_target_type))

            try:
                self._state = ScheduleState.Enabled.name
                dto = self._update_remote(logger)
                self._schedule_id = dto.schedule_id
                self._schedule_start = dto.schedule_start_time if dto.schedule_start_time else None
                self._state = dto.state

                schedule = Schedule.get(self.workspace, self._schedule_id)
                schedule._wait_for_provisioning(3600)

            except HttpOperationError or SystemError as e:
                if DATADRIFT_IN_PROGRESS_MSG not in e.message:
                    logger.error(
                        "Unable to enable the schedule in workspace: {}, error message: {}.".format(
                            self.workspace,
                            e.message))
                    raise
                logger.info("Enable task is still running, you may check the status by calling .get() and .state")

    def disable_schedule(self):
        """Disable a schedule for a specified model and web service."""
        _TelemetryLogger.log_event(DATADRIFT_DISABLE_SCHEDULE, **self._logger.context)
        with _TelemetryLogger.log_activity(self._logger, activity_name="disable_schedule") as logger:
            try:
                self._state = ScheduleState.Disabled.name
                self._update_remote(logger)

                schedule = Schedule.get(self.workspace, self._schedule_id)
                schedule._wait_for_provisioning(3600)

            except HttpOperationError or SystemError as e:
                if DATADRIFT_IN_PROGRESS_MSG not in e.message:
                    logger.error(
                        "Unable to disable the schedule with ID: {} in workspace: {}, error message: {}.".format(
                            self._schedule_id,
                            self.workspace,
                            e.message))
                    raise
                logger.info("Disable task is still running, you may check the status by calling .get() and .state")

    def get_output(self, start_time=None, end_time=None, run_id=None):
        """Get a tuple of the drift results and metrics for a specific DataDriftDetector in over a given time window.

        .. remarks::
            Given there are three run types, adhoc run, scheduled run and backfill run. This attribute will be used
            to retrieve corresponding results in different ways:

            * To retrieve adhoc run results, there is only one way: run_id should be a valid guid run id.
            * To retrieve scheduled runs and backfill runs' results, there are two different ways: assign a valid guid
                run id to run_id, or assign specific start_time and/or end_time while keeping run_id as None;
            * If run_id and start_time/end_time are not None in the same invoking, parameter validation exception
                will be thrown.

            Get a tuple of drift results and metrics for a time window between a given ``start_time`` and ``end_time``
            (inclusive) for a :class:`azureml.datadrift.datadriftdetector.DataDriftDetector`. If ``run_id`` is
            specified, the results and metrics returned will be for the specific adhoc run specified by the ``run_id``.
            **NOTE:** the ``start_time`` and ``end_time`` parameters cannot be inputted alongside the ``run_id``.
            It's possible that there are multiple results for the same target date (target date means target dataset
            start date for dataset based drift, or scoring date for model based drift). Therefore it's necessary to
            identify and handle duplicated results. For dataset based drift, if results are for the same target date,
            then they are duplicated results. For model based drift, if results are for the same target date and about
            the same service, then they are deuplicated results. The get_output attribute will dedup these duplicated
            result by one rule: always pick up the latest generated results.

            The get_output attribute can be used to retrieve all outputs or partial outputs of scheduled runs in a
            specific time range between 'start_tzime' and 'end_time' (boundary included). User can also limited to
            results of an individual adhoc 'run_id'.

            * Principle for filtering is "overlapping": as long as there is an overlap between the actual result time
                (Model Based: scoring date, Dataset Based: target dataset [start date, end date]) and the given
                [``start_time``, ``end_time``], that result will be picked up.

            * It's possible that there are multiple outputs for one target date if drift calculation was executed
                several times against that day. In this situation, only the latest output will be picked by default.
                If all outputs are needed for the same target date, 'daily_latest_only' should be set as False.

            * Model Based DataDriftDetectors will have a slightly different metrics schema than Dataset Based.
                For example, for Model Based results, it will look like:
            * Given there are multiple types of data drift instance, the result contents could be various.
                For example, for model based results, it will look like:

            .. code-block:: python

                results : [{'drift_type': 'ModelBased' or 'DatasetBased', 'service_name': 'service1',
                            'result':[{'has_drift': True, 'datetime': '2019-04-03', 'drift_threshold': 0.3,
                                       'model_name': 'modelName', 'model_version': 2}]}]
                metrics : [{'drift_type': 'ModelBased' or 'DatasetBased', 'service_name': 'service1',
                            'metrics': [{'schema_version': '0.1', 'datetime': '2019-04-03',
                                         'model_name': 'modelName', 'model_version': 2,
                                         'dataset_metrics': [{'name': 'datadrift_coefficient', 'value': 0.3453}],
                                         'column_metrics': [{'feature1': [{'name': 'datadrift_contribution',
                                                                           'value': 288.0},
                                                                          {'name': 'wasserstein_distance',
                                                                           'value': 4.858040000000001},
                                                                          {'name': 'energy_distance',
                                                                           'value': 2.7204799576545313}]}]}]}]

            While for Dataset Based results, it will look like:

            .. code-block:: python

                results : [{'drift_type': 'ModelBased' or 'DatasetBased',
                            'result':[{'has_drift': True, 'drift_threshold': 0.3,
                                       'start_date': '2019-04-03', 'end_date': '2019-04-04',
                                       'base_dataset_id': '4ac144ef-c86d-4c81-b7e5-ea6bbcd2dc7d',
                                       'target_dataset_id': '13445141-aaaa-bbbb-cccc-ea23542bcaf9'}]}]
                metrics : [{'drift_type': 'ModelBased' or 'DatasetBased',
                            'metrics': [{'schema_version': '0.1',
                                         'start_date': '2019-04-03', 'end_date': '2019-04-04',
                                         'baseline_dataset_id': '4ac144ef-c86d-4c81-b7e5-ea6bbcd2dc7d',
                                         'target_dataset_id': '13445141-aaaa-bbbb-cccc-ea23542bcaf9'
                                         'dataset_metrics': [{'name': 'datadrift_coefficient', 'value': 0.53459}],
                                         'column_metrics': [{'feature1': [{'name': 'datadrift_contribution',
                                                                           'value': 288.0},
                                                                          {'name': 'wasserstein_distance',
                                                                           'value': 4.858040000000001},
                                                                          {'name': 'energy_distance',
                                                                           'value': 2.7204799576545313}]}]}]}]

        :param start_time: Start time of results window in UTC, default is None, which means to pick up
                           the most recent 10th cycle's results.
        :type start_time: datetime.datetime, optional
        :param end_time: End time of results window in UTC, default is None, which indicates UTC current day.
        :type end_time: datetime.datetime, optional
        :param run_id: Optional, a specific run id
        :type run_id: int
        :return: Tuple of a list of drift results, and a list of individual dataset and columnar metrics
        :rtype: tuple(:class:list(), :class:list())
        """
        if run_id and (start_time or end_time):
            raise ValueError("Either run_id or start_time/end_time should be None.")

        start_time, end_time = self._get_valid_time_range(start_time=start_time, end_time=end_time)

        run_id = ParameterValidator.validate_run_id(run_id) if run_id is not None else run_id

        _TelemetryLogger.log_event(DATADRIFT_GET_OUTPUT, **self._logger.context)
        with _TelemetryLogger.log_activity(self._logger, activity_name="get_output") as logger:

            # try to refresh latest run time.
            dd_client = DataDriftClient(self.workspace.service_context)
            try:
                dto_list = list(dd_client.list(model_name=self.model_name,
                                               model_version=self.model_version,
                                               services=self.services,
                                               base_dataset_id=self._baseline_dataset_id,
                                               target_dataset_id=self._target_dataset_id,
                                               logger=self._logger))
            except HttpOperationError as e:
                logger.error(e.message)
                raise
            for d in dto_list:
                if d.id == self._id and hasattr(d, 'latest_run_time'):
                    self._latest_run_time = d.latest_run_time

            return _all_outputs(self, start_time, end_time, run_id)

    def update(self, services=..., compute_target=..., feature_list=..., schedule_start=..., alert_config=...,
               drift_threshold=...):
        r"""Update the schedule associated with the DataDriftDetector object.

        :param services: Optional, list of services to update
        :type services: builtin.list[str]
        :param compute_target: Optional, AzureML ComputeTarget or ComputeTarget name; DataDriftDetector will create one
                               if none specified
        :type compute_target: azureml.core.ComputeTarget or str
        :param feature_list: Whitelisted features to run the datadrift detection on
        :type feature_list: builtin.list[str]
        :param schedule_start: Start time of data drift schedule in UTC
        :type schedule_start: datetime.datetime
        :param alert_config: Optional, configuration object for DataDriftDetector alerts
        :type alert_config: azureml.datadrift.AlertConfiguration
        :param drift_threshold: Threshold to enable DataDriftDetector alerts on
        :type drift_threshold: float
        :return: self
        :rtype: azureml.datadrift.DataDriftDetector
        """
        _TelemetryLogger.log_event(DATADRIFT_UPDATE, **self._logger.context)
        with _TelemetryLogger.log_activity(self._logger, activity_name="update") as logger:
            if services is not ...:
                services = ParameterValidator.validate_services(services)
                self._services = services
            if compute_target is not ...:
                compute_target = ParameterValidator.validate_compute_target(compute_target, self.workspace)
                if not compute_target:
                    self._compute_target_name = self._get_default_compute_target(self.workspace)
                elif isinstance(compute_target, ComputeTarget):
                    self._compute_target_name = compute_target.name
                else:
                    self._compute_target_name = compute_target
            if feature_list is not ...:
                self._feature_list = ParameterValidator.validate_feature_list(feature_list)
            if schedule_start is not ...:
                self._schedule_start = ParameterValidator.validate_datetime(schedule_start)
            if alert_config is not ...:
                self._alert_config = ParameterValidator.validate_alert_configuration(alert_config)
            if drift_threshold is not ...:
                self._drift_threshold = ParameterValidator.validate_drift_threshold(drift_threshold)
                if not self._drift_threshold:
                    self._drift_threshold = DEFAULT_DRIFT_THRESHOLD

            self._update_remote(logger)
            return self

    def _update_remote(self, logger):
        """Update the DataDriftDetector entry in the service database.

        :param logger: Activity logger for service call
        :type logger: datetime.datetime
        :return: DataDriftDetector data transfer object
        :rtype: logging.Logger
        """
        dto = UpdateDataDriftDto(compute_target_name=self._compute_target_name,
                                 alert_configuration=AlertConfiguration(
                                     email_addresses=self.alert_config.email_addresses)
                                 if self.alert_config else None,
                                 services=self._services,
                                 features=self._feature_list,
                                 drift_threshold=self._drift_threshold,
                                 state=self._state, )
        client_dto = self._client.update(self._id, dto, logger, api_version=PUBLICPREVIEW)
        DataDriftDetector._validate_client_dto(client_dto, logger)
        return client_dto

    def _get_compute_target(self, compute_target_name=None, create_compute_target=False, logger=None):
        """Get compute target.

        :type compute_target_name: str
        :param create_compute_target: if or not or create a aml compute target if not existing
        :type create_compute_target: boolean
        :param compute_target_name: Optional, AzureML ComputeTarget name, creates one if none is specified
        :type compute_target_name: str
        :param logger: Optional, Datadrift logger
        :type logger: logging.LoggerAdapter
        :return: ComputeTarget
        :rtype: azureml.core.compute.ComputeTarget
        """
        # If any of the params below are None, this is a schedule run so default to the DataDriftDetector object's args
        if compute_target_name is None:
            compute_target_name = self._compute_target_name
        if logger is None:
            logger = self._logger

        try:
            compute_target = ComputeTarget(self.workspace, compute_target_name)
            return compute_target

        except ComputeTargetException as e:
            # get the aml compute target or create if it is not available and create_compute_target is True
            if create_compute_target:
                return self._create_aml_compute(self.workspace, compute_target_name)
            else:
                error_message = "compute target {} is not available." \
                                "Use create_compute_target=True to allow creation of a new compute target." \
                    .format(compute_target_name)
                logger.error(error_message)
                raise ComputeTargetException(error_message) from e

    @staticmethod
    # this attribute is also use in server side. (datadrift_run.py, _generate_script.py, msdcuration_run.py ...)
    # keep it to be compatible and call _get_metrics_path() for actual execution.
    def _get_metrics_path(model_name, model_version, service,
                          target_date=None, drift_type=DATADRIFT_TYPE_MODEL, datadrift_id=None):
        """Get the metric path for a given model version, instance target date and frequency of diff.

        :param model_name: Model name
        :type model_name: str
        :param model_version: Model version
        :type model_version: int
        :param service: Service name
        :type service: str
        :param target_date: Diff instance start time. If none datetime portion is omitted.
        :type target_date: datetime.datetime
        :return: Relative paths to metric on datastore (model base and general)
        :rtype: str
        """
        return _get_metrics_path(model_name, model_version, service, target_date, drift_type, datadrift_id)

    def _get_date_for_x_cycles(self, base_date, cycles, go_back):
        """To retrieve start or end date of given cycles.

        By default get_output and show will always return x cycles results if start_time or end_time is not inputted.
        Currently x is defined as 10, which means:
        If both start time and end time are not provided, then end time is today, start time is end time- 10 cycles;
        If only start time provided, then the end time should be start + 10 cycles;
        If only end time provided, then the start time should be end - 10 cycles;

        :param base_date: base date to calculate + or - x cycles.
        :param go_back: if to calculate start time, then go_back should be set to true to do minus x cycles.
        :return: calculated x cycles start or end date
        """
        base_date = base_date if base_date else datetime.utcnow().date()
        step = (0 - cycles) if go_back is True else cycles
        if self.frequency == 'Day':
            target_date = base_date + timedelta(days=step)
        elif self.frequency == 'Week':
            target_date = base_date + timedelta(weeks=step)
        elif self.frequency == 'Month':
            target_date = base_date + relativedelta(months=step)
        else:
            raise ValueError("Property frequency is invalid or not defined.")
        return datetime(target_date.year, target_date.month, target_date.day)

    def _get_valid_time_range(self, start_time=None, end_time=None):
        """Calculate time range for result retrieving or graph showing.

        :param start_time: start time input to get_output or show API.
        :param end_time: end time input to get_output or show API.
        :return: calculated time range
        """
        start_time_valid = ParameterValidator.validate_datetime(start_time) if start_time \
            else self._get_date_for_x_cycles(base_date=end_time, cycles=DEFAULT_LOOKBACK_CYCLES, go_back=True)

        end_time_valid = ParameterValidator.validate_datetime(end_time) if end_time \
            else self._get_date_for_x_cycles(base_date=start_time_valid, cycles=DEFAULT_LOOKBACK_CYCLES, go_back=False)

        return start_time_valid, end_time_valid

    def show(self, start_time=None, end_time=None):
        """Show data drift trend in given time range.

        By default it will show the most recent 10 cycles. For example, if frequency is day, then it will be the most
        recent 10 days, if frequency is week, then it will be the most recent 10 weeks.

        :param start_time: Optional, start of presenting time window in UTC, default is None, which means to pick up
                           the most recent 10th cycle's results.
        :type start_time: datetime.datetime
        :param end_time: Optional, end of presenting data time window in UTC, default is None, means UTC current day.
        :type end_time: datetime.datetime
        :return: diction of all figures. Key is service_name
        :rtype: dict()
        """
        start_time_valid, end_time_valid = self._get_valid_time_range(start_time=start_time, end_time=end_time)

        _TelemetryLogger.log_event(DATADRIFT_SHOW, **self._logger.context)

        return _show(self, start_time_valid, end_time_valid)

    @staticmethod
    def _validate_client_dto(datadriftdto, logger):
        if datadriftdto is not None and datadriftdto.alert_configuration is not None and \
                datadriftdto.alert_configuration.email_addresses is not None \
                and len(datadriftdto.alert_configuration.email_addresses) > 0:
            # this means alert config is supposed to be set.
            if datadriftdto.alert_id is None:
                warnings.warn("Alert has not been setup for data-drift with model {} and version {}.\n".
                              format(datadriftdto.model_name, datadriftdto.model_version))
                if logger is not None:
                    logger.info("Alert has not been setup for data-drift with model {} and version {}.\n".
                                format(datadriftdto.model_name, datadriftdto.model_version))
