from entities.appointment import Appointment
from datetime import datetime
import pandas as pd


class AppointmentList:
    """
        Class to define a list of appointments
    """
    list_appointments = []
    file_path = 'model/data.csv'

    def __init__(self):
        self.df_appointments = pd.read_csv(
            AppointmentList.file_path).drop_duplicates('appointment_id')
        for _, row in self.df_appointments.iterrows():
            AppointmentList.list_appointments.append(
                Appointment(row['appointment_id'], row['doctor_id'], row['patient_id'], row['appointment_datetime']))

    def get_appointments(self, name, date, entity_type):
        """
            Function to get appointments for a given entity
        """
        datetime_object = date
        if(type(date) == str):
            datetime_object = datetime.strptime(date, '%Y-%m-%d')

        id = ''

        if(entity_type == 'doctor'):
            id = [appointment.id for appointment in AppointmentList.list_appointments if appointment.doctor_id == name][0]
        else:
            id = [appointment.id for appointment in AppointmentList.list_appointments if appointment.patient_id == name][0]

        appointments = [appointment for appointment in AppointmentList.list_appointments if appointment.id ==
                        id and appointment.appointment_datetime.date() == datetime_object.date()]

        return appointments
