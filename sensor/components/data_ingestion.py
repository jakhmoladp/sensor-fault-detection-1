from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity.config_entity import DataIngestionConfig
from sensor.entity.artifact_entity import DataIngestionArtifact
import sys, os
from pandas import DataFrame
from sensor.data_access.sensor_data import SensorData

class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise SensorException(e, sys)

    def export_data_into_feature_store(self) -> DataFrame:
        """
        Import mongodb collection record as dataframe
        """
        try:
            logging.info("Importing Data from MongoDB to DataFrame")
            # initialize the sensor data class (mongo db connection attributes)
            sensor_data = SensorData()
            # import the data from the required collection (table) from mongo db
            dataframe = sensor_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            # once data is imported, we need to save it.
            # we'll save the feature data in the feature store directory
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            print("Feature Store File Path: --> ", feature_store_file_path)

            # Create folders
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe


        except Exception as e:
            raise SensorException(e, sys)

    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        """
        Split the feature store data into train and test sets
        """
        pass
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            dataframe = self.export_data_into_feature_store()
            self.split_data_as_train_test(dataframe)
        except Exception as e:
            raise SensorException(e, sys)
