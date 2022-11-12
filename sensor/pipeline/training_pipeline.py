"""
This script defines the structure of Training pipeline. A pipeline is comprised on multiple components.
Each components translates some inputs to outputs. We had defined separate class methods to perform
the various tasks.
"""
from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sensor.exception import SensorException
import sys, os
from sensor.logger import logging
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation

class TrainPipeline:
    
    def __init__(self):
        training_pipeline_config = TrainingPipelineConfig()
        self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        self.training_pipeline_config = training_pipeline_config

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("Starting data ingestion")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingestion Completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def start_data_validaton(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            # Read the configuration details for validation (directories for failed/passed validation, drift reports, etc.)
            # Initialize the validation config object using the config details, this will set the variable values with config details
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)

            # perform the data validation by passing data_validation configuration 
            # and the validation artifacts
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config = data_validation_config
            )

            data_validation_artifact = data_validation.initiate_data_validation()
            return data_validation_artifact
        except  Exception as e:
            raise  SensorException(e,sys)

    def start_data_transformation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)  

    def start_model_trainer(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)  

    def start_model_evaluation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)  

    def run_pipeline(self):
        try:
            print("......Inside run pipeline function")
            data_ingestion_artifact = self.start_data_ingestion()
            print(".........data ingestion step has finished")
            data_validation_artifact=self.start_data_validaton(data_ingestion_artifact=data_ingestion_artifact)
            print(".........data validation step has finished")
        except Exception as e:
            raise SensorException(e, sys)

 
if __name__ == '__main__':

    training_pipeline_config = TrainingPipelineConfig()
    print(training_pipeline_config)
