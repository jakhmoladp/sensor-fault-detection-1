from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig

if __name__ == '__main__':
    print("Check#1 - MongoDB Connection Test")
    mongodb_client = MongoDBClient()
    print("collection name:",mongodb_client.database.list_collection_names())


    print("Check#2 - DataIngestion Pipeline Connection")
    training_pipeline_config = TrainingPipelineConfig()
    data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
    print(data_ingestion_config.__dict__)