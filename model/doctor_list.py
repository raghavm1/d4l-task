from pydoc import Doc
from entities.doctor import Doctor
import pandas as pd


class DoctorList:
    """
        Class to define a list of doctors
    """
    list_docs = []

    file_path = 'model/data.csv'

    def __init__(self):
        self.df_docs = pd.read_csv(
            DoctorList.file_path).drop_duplicates('doctor_id')
        for _, row in self.df_docs.iterrows():
            DoctorList.list_docs.append(
                Doctor(row['doctor_id'], row['doctor_name']))
