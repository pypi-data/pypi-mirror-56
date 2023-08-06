# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Model Serving Dataset."""
import os
from ._utils.parameter_validator import ParameterValidator
from azureml.core import Dataset
from azureml.datadrift._utils.constants import CURATION_COL_NAME_TIMESTAMP_INPUTS

EXPORT_FOLDER = "export"
EXPORT_FILENAME = "msd.csv"
EXPORT_PATH = os.path.join(EXPORT_FOLDER, EXPORT_FILENAME)

DATASET_PREFIX = "ModelServingDataset-"

TIMESTAMP_COLUMN = "$Timestamp_Inputs"


class ModelServingDataset:
    """Class represent model serving dataset."""

    def __init__(self, workspace):
        """Constructor.

        :param workspace: workspace of the model serving dataset.
        :type workspace: Workspace
        """
        self.workspace = workspace

    def __repr__(self):
        """Return the string representation of a ModelServingDataset object.

        :return: ModelServingDataset object string
        :rtype: str
        """
        return str(self.__dict__)

    def export_to_csv(self, start_time, end_time):
        """Export model serving dataset to local csv.

        :param start_time: the start time you want to export in UTC
        :type start_time: datetime.datetime
        :param end_time: the end time you want to export in UTC
        :type end_time: datetime.datetime
        :return: relative path of the exported csv file.
        :rtype: str
        """
        start_time = ParameterValidator.validate_datetime(start_time)
        end_time = ParameterValidator.validate_datetime(end_time)

        dataset = Dataset.get_by_name(self.workspace, DATASET_PREFIX + self.workspace._workspace_id.split('-')[0])
        ds = dataset.with_timestamp_columns(fine_grain_timestamp=CURATION_COL_NAME_TIMESTAMP_INPUTS)
        ds = ds.time_between(start_time=start_time, end_time=end_time)
        df = ds.to_pandas_dataframe()
        os.makedirs(EXPORT_FOLDER, exist_ok=True)
        df.to_csv(EXPORT_PATH, index=False)

        return EXPORT_PATH
