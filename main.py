from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from sensor.pipeline import training_pipeline
from sensor.pipeline.training_pipeline import TrainPipeline
from sensor.utils.main_utils import read_yaml_file
import os
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from sensor.ml.model.estimator import ModelResolver,TargetValueMapping
from sensor.utils.main_utils import load_object
import pandas as pd

# logging and exception handling
from sensor.logger import logging

# API libraries
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as app_run
from sensor.constant.application import APP_HOST, APP_PORT

env_file_path=os.path.join(os.getcwd(),"env.yaml")

def set_env_variable(env_file_path):
    if os.getenv('MONGO_DB_URL',None) is None:
        env_config = read_yaml_file(env_file_path)
        os.environ['MONGO_DB_URL']=env_config['MONGO_DB_URL']

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainPipeline()
        # We don't want to run a duplicate pipeline if one is already running
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        
        # Start training pipeline
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.get("/predict")
async def predict_route():
    try:
        #get data from user csv file
        #conver csv file to dataframe

        # for demo we are using already generated CSV file
        df=pd.read_csv("aps_failure_training_set1.csv")
        # set model directory path
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)

        # Give an error if no model is present
        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        
        # otherwise, read the path (directory location) of present model
        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)
        
        #decide how to return file to user.
        
    except Exception as e:
        raise Response(f"Error Occured! {e}")

def main():
    try:
        set_env_variable(env_file_path)
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
    except Exception as e:
        print(e)
        logging.exception(e)



if __name__ == '__main__':
    app_run(app, host='0.0.0.0', port=8080)