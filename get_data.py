# This script is created to populate data in the mongo db 
# we have used the csv file as input to avoid data generation cost

# files created to run this script
    # env.yaml - localhost connection string for mongodb
    # aps_failure_training_set1.csv - csv file containing the data
    # added 'save csv' function in sensor/data_access/sensor_data.py
file_path="aps_failure_training_set1.csv"
from sensor.data_access.sensor_data import SensorData
from sensor.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from main import set_env_variable
import os

if __name__=='__main__':
    data_file_path="aps_failure_training_set1.csv"
    env_file_path='env.yaml'
    set_env_variable(env_file_path)
    sd = SensorData()
    print("LIST COLLECTIONS", sd.mongo_client.database.list_collection_names())
    if DATA_INGESTION_COLLECTION_NAME in sd.mongo_client.database.list_collection_names():
        print("DATA_INGESTION_COLLECTION_NAME::", DATA_INGESTION_COLLECTION_NAME)
        result = sd.mongo_client.database[DATA_INGESTION_COLLECTION_NAME].drop()
        print("SENSOR DATABASE DROPPED!", result)
    sd.save_csv_file(file_path=data_file_path,collection_name=DATA_INGESTION_COLLECTION_NAME)
    print(f"New Data Saved Into MongoDB table {DATA_INGESTION_COLLECTION_NAME}")
