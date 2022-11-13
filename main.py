from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from sensor.pipeline import training_pipeline
from sensor.pipeline.training_pipeline import TrainPipeline
from sensor.utils.main_utils import read_yaml_file
import os

env_file_path=os.path.join(os.getcwd(),"env.yaml")

def set_env_variable(env_file_path):
    if os.getenv('MONGO_DB_URL',None) is None:
        env_config = read_yaml_file(env_file_path)
        os.environ['MONGO_DB_URL']=env_config['MONGO_DB_URL']


if __name__ == '__main__':
    print("Check#1 - MongoDB Connection Test")
    # mongodb_client = MongoDBClient()
    #print("collection name:",mongodb_client.database.list_collection_names())


    print("\nCheck#2 - DataIngestion Pipeline Connection")
    training_pipeline_config = TrainingPipelineConfig()
    data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
    print(data_ingestion_config.__dict__)

    print("\nCheck#3 - Training Pipeline Flow Testing")
    training_pipeline = TrainPipeline()
    print('...TrainPipeline initialized')
    training_pipeline.run_pipeline()
    print('...Pipeline ran successfully')