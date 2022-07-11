from entities.patient import Patient
import pandas as pd


class PatientList:
    """
        Class to define a list of patients
    """
    list_patients = []
    file_path = "model/data.csv"

    def __init__(self):
        self.df_patients = pd.read_csv(
            PatientList.file_path).drop_duplicates('patient_id')
        for _, row in self.df_patients.iterrows():
            PatientList.list_patients.append(
                Patient(row['patient_id'], row['patient_name'], row['patient_age'], row['patient_gender']))
