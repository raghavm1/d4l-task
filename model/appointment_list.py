from entities.appointment import Appointment
from datetime import datetime
import pandas as pd

from model.doctor_list import DoctorList
from model.patient_list import PatientList


class AppointmentList:
    """
        Class to define a list of appointments
    """
    list_appointments = []
    file_path = 'model/data.csv'

    def __init__(self):
        self.df_appointments = pd.read_csv(
            AppointmentList.file_path)
        for _, row in self.df_appointments.iterrows():
            AppointmentList.list_appointments.append(
                Appointment(row['appointment_id'], row['doctor_id'], row['patient_id'], datetime.strptime(row['appointment_datetime'], ' %d%m%Y %H:%M:%S')))

    # def get_appointments(self, name, date, entity_type):
    #     """
    #         Function to get appointments for a given entity
    #     """
    #     datetime_object = date
    #     if(type(date) == str):
    #         datetime_object = datetime.strptime(date, '%Y-%m-%d')

    #     id = ''

    #     if(entity_type == 'doctor'):
    #         id = [
    #             doctor.doctor_id for doctor in DoctorList.list_docs if doctor.doctor_name == name][0]
    #         appointments = [appointment for appointment in AppointmentList.list_appointments if appointment.doctor_id ==
    #                         id and appointment.time.date() == datetime_object.date()]
    #     else:
    #         id = [
    #             patient.patient_id for patient in PatientList.list_patients if patient.patient_name == name][0]

    #         appointments = [appointment for appointment in AppointmentList.list_appointments if appointment.patient_id ==
    #                         id and appointment.time.date() == datetime_object.date()]
    #     return appointments
