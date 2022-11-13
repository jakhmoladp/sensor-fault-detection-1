"""
This script defines the structure of Training pipeline. A pipeline is comprised on multiple components.
Each components translates some inputs to outputs. We had defined separate class methods to perform
the various tasks.
"""
from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from sensor.exception import SensorException
import sys, os
from sensor.logger import logging
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer


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

    def start_data_transformation(self, data_validation_artifact):
        """
        Include steps to transform the data and create inputs before sending to ML model.
        """
        try:
            # read the data transformation configurations from schema.yaml file
            data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
            
            # Create object of DataTransformation class
            # data transformation requires two inputs - data validation artificats i.e. report.yaml file
            # that contains the validation result of each data column
            data_transformation = DataTransformation(
                data_validation_artifact,
                data_transformation_config
            )
            # initiate data transformation
            data_transformation_artifact =  data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys)  

    def start_model_trainer(self, data_transformation_artifact):
        try:
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except  Exception as e:
            raise  SensorException(e,sys) 

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
            data_validation_artifact = self.start_data_validaton(data_ingestion_artifact=data_ingestion_artifact)
            print(".........data validation step has finished")
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            print(".........data transformation step has finished")
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
            print(".........data training step has finished")
        except Exception as e:
            raise SensorException(e, sys)

 
if __name__ == '__main__':

    training_pipeline_config = TrainingPipelineConfig()
    print(training_pipeline_config)
