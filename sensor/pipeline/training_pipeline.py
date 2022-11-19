"""
This script defines the structure of Training pipeline. A pipeline is comprised on multiple components.
Each components translates some inputs to outputs. We had defined separate class methods to perform
the various tasks.
"""
from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig, ModelPusherConfig
from sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact, ModelPusherArtifact
from sensor.exception import SensorException
import sys, os
from sensor.logger import logging
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation
from sensor.components.model_pusher import ModelPusher

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

    def start_data_transformation(self, data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
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

    def start_model_trainer(self, data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except  Exception as e:
            raise  SensorException(e,sys) 

    def start_model_evaluation(self,data_validation_artifact:DataValidationArtifact,
                                 model_trainer_artifact:ModelTrainerArtifact,
                                ):
        try:
            model_eval_config = ModelEvaluationConfig(self.training_pipeline_config)
            model_eval = ModelEvaluation(model_eval_config, data_validation_artifact, model_trainer_artifact)
            model_eval_artifact = model_eval.initiate_model_evaluation()
            return model_eval_artifact
        except  Exception as e:
            raise  SensorException(e,sys)

    def start_model_pusher(self,model_eval_artifact:ModelEvaluationArtifact):
            try:
                model_pusher_config = ModelPusherConfig(training_pipeline_config=self.training_pipeline_config)
                model_pusher = ModelPusher(model_pusher_config, model_eval_artifact)
                model_pusher_artifact = model_pusher.initiate_model_pusher()
                return model_pusher_artifact
            except  Exception as e:
                raise  SensorException(e,sys)

    def run_pipeline(self):
        try:
            print("......Inside run pipeline function")
            data_ingestion_artifact = self.start_data_ingestion()
            print("1.........data INGESTION step has finished")
            data_validation_artifact = self.start_data_validaton(data_ingestion_artifact=data_ingestion_artifact)
            print("2.........data VALIDATION step has finished")
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            print("3.........data TRANSFORMATION step has finished")
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
            print("4.........data TRAINING step has finished")
            # In model evaluation phase we compare the new model with existing model in the production
            # If the new model is not performing better than existing above a given threshold
            # we reject the new model
            # Deploying models has a certain cost associated with it, so we only deploy the new models
            # if it is going to give us significant improvement.
            model_eval_artifact = self.start_model_evaluation(data_validation_artifact, model_trainer_artifact) # Evaluation is done on the results generated during model training
            print("5.........data evaluation step has finished")
            if not model_eval_artifact.is_model_accepted:
                raise Exception("Trained model is not better than the best model")
            model_pusher_artifact = self.start_model_pusher(model_eval_artifact)
            print("6.........model PUSHER step has finished")
        except Exception as e:
            raise SensorException(e, sys)

 
if __name__ == '__main__':

    training_pipeline_config = TrainingPipelineConfig()
    print(training_pipeline_config)
