"""
    This module is to define classes which are entities for the case study.
"""


from matplotlib.pyplot import get
import pandas as pd
from datetime import datetime
import logging


class Patient:
    """
        Class created for Patient entity
    """

    def __init__(self, patient_id, patient_name, patient_age, patient_gender) -> None:
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.patient_age = patient_age
        self.patient_gender = patient_gender

    def to_dict(self):
        """
            This function aids in the creation of a dataframe
        """
        return {
            'id': self.patient_id,
            'name': self.patient_name,
            'age': self.patient_age,
            'gender': self.patient_gender
        }


class Doctor:
    """
        Class created for Doctor entity
    """

    def __init__(self, doctor_id, doctor_name) -> None:
        self.doctor_id = doctor_id
        self.doctor_name = doctor_name

    def to_dict(self):
        """
            This function aids in the creation of a dataframe
        """
        return {
            'id': self.doctor_id,
            'name': self.doctor_name,
        }


class Appointment:
    """
        Class created for defining the appointment relation
    """

    def __init__(self, doctor, patient, time) -> None:
        self.doctor = doctor
        self.patient = patient
        self.time = time


def read_from_csv(path: str):
    """
        Function to read from csv file
    """
    df = pd.read_csv(path)

    df['appointment_datetime'] = df['appointment_datetime'].apply(
        lambda x: datetime.strptime(x, ' %d%m%Y %H:%M:%S'))

    return df


def get_appointments(name, date, entity_type):
    """
        Function to get appointments for a given entity
    """
    global df_appointments
    global df_doctors
    global df_patients

    datetime_object = date
    if(type(date) == str):
        datetime_object = datetime.strptime(date, '%Y-%m-%d')

    id = ''
    if(entity_type == 'doctor'):
        id = df_doctors[df_doctors['name'] == name]['id'].values[0]
    else:
        id = df_patients[df_patients['name'] == name]['id'].values[0]

    appointments = df_appointments[(df_appointments['{}_id'.format(entity_type)] == id) & (
        df_appointments['appointment_datetime'].dt.date == datetime_object.date())]
    return appointments


def validate_appointment():
    """
        Function to validate an appointment
    """
    pass


def create_appointment(patient_name, doctor_name, date, time, df_doctor, df_patient):
    """
        Function to create an appointment
    """
    global df_appointments
    global df_doctors
    global df_patients
    # Return error on invalid appointment time (i.e. at 3PM or beyond 4PM)
    if(datetime.strptime(time, "%H:%M:%S").time() > datetime.strptime("15:00:00", "%H:%M:%S").time() or datetime.strptime(time, "%H:%M:%S").time() < datetime.strptime("08:00:00", "%H:%M:%S").time()):
        logging.error(
            "Invalid appointment time: Doctors are available only from 8AM till 4PM")
        return False

    # First, check if the given date and time checks out for the doctor
    datetime_string = date + time
    datetime_object = datetime.strptime(datetime_string, '%Y-%m-%d%H:%M:%S')

    try:
        doctor_id = df_doctors[df_doctor['name']
                               == doctor_name]['id'].values[0]
    except:
        logging.error(' Doctor not found')
        return False

    try:
        patient_id = df_patients[df_patient['name']
                                 == patient_name]['id'].values[0]
    except:
        logging.error(' Patient not found')
        return False

    # Check if the doctor is available on the given date and time
    doctor_apps = get_appointments(
        doctor_name, datetime_object, 'doctor')
    patient_apps = get_appointments(
        patient_name, datetime_object, 'patient')

    if(len(doctor_apps) > 0):
        doctor_apps = doctor_apps.sort_values(by='appointment_datetime')

    appointment_id = 'A' + doctor_id + patient_id + \
        datetime_object.strftime('%y%m%d%H')
    df_appointments = df_appointments.append(
        {'doctor_id': doctor_id, 'patient_id': patient_id, 'appointment_id': appointment_id, 'appointment_datetime': datetime_object}, ignore_index=True)
    return True


if __name__ == '__main__':

    df = read_from_csv('./data.csv')

    patients = []
    doctors = []
    df_people = pd.DataFrame(
        columns=['patient_id', 'patient_name', 'patient_age', 'patient_gender'])
    df_doctors = pd.DataFrame(columns=['id', 'name'])

    for index, row in df.iterrows():
        patient = Patient(row['patient_id'], row['patient_name'],
                          row['patient_age'], row['patient_gender'])
        patients.append(patient)
        doctor = Doctor(row['doctor_id'], row['doctor_name'])
        doctors.append(doctor)
    df_patients = pd.DataFrame.from_records(
        [patient.to_dict() for patient in patients])
    df_doctors = pd.DataFrame.from_records(
        [doctor.to_dict() for doctor in doctors])
    df_appointments = df.drop(['doctor_name', 'patient_name',
                               'patient_gender', 'patient_age'], axis=1)

    print(get_appointments('D1Name', "2018-03-08", 'doctor'))

    # if(create_appointment('P3Name', 'D1Name', '2022-04-03',
    #                       '15:00:00', df_doctors, df_patients)):
    #     print("Appointment created")
