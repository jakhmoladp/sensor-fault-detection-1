from dataclasses import dataclass

"""Data Class allows the initialization of class without using __init__ function.
Example: DataIngestionArtifact(train_path, test_path)

"""
@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str