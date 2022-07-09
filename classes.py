"""
    This module is to define classes which are entities for the case study.
"""


import pandas as pd
from datetime import datetime
import datetime as dt_time
import logging


# class DoctorList:
#     """
#         Class to define a list of doctors
#     """
#     list_docs = []

#     file_path = '../data/doctors.csv'
#     def __init__(self, df_doctors):
#         self.df_doctors = df_doctors
#         self.doctors = []
#         for _, row in df_doctors.iterrows():
#             self.doctors.append(Doctor(row['id'], row['name']))


# class PatientList:
#     """
#         Class to define a list of patients
#     """
#     Patient_list = []

#     def __init__(self, patients):
#         self.df_patients = df_patients
#         self.patients = []
#         for _, row in df_patients.iterrows():
#             self.patients.append(
#                 Patient(row['id'], row['name'], row['birth_date'], row['gender']))


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

    def __init__(self, doctor_id, patient_id, time) -> None:
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.time = time

    def to_dict(self):
        """
            This function aids in the creation of a dataframe
        """
        return {
            'doctor_id': self.doctor_id,
            'patient_id': self.patient_id,
            'appointment_datetime': self.time
        }


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
    global appointments
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
        for _, row in doctor_apps.iterrows():
            if(row['appointment_datetime'] - datetime_object < dt_time.timedelta(minutes=60)):
                logging.error(
                    "Doctor is not available on the given date and time")
                return False
    if(len(patient_apps) > 0):
        for _, row in patient_apps.iterrows():
            if(row['appointment_datetime'] - datetime_object < dt_time.timedelta(minutes=60)):
                logging.error(
                    "Patient is not available on the given date and time")
                return False

    appointment_id = 'A' + doctor_id + patient_id + \
        datetime_object.strftime('%y%m%d%H')
    appointments.append(Appointment(doctor_id, patient_id, datetime_object))
    df_appointments = df_appointments.append(
        {'doctor_id': doctor_id, 'patient_id': patient_id, 'appointment_id': appointment_id, 'appointment_datetime': datetime_object}, ignore_index=True)
    return True


def cancel_appointment(doctor_name=None, patient_name=None, date=None, time=None):
    """
        Function to cancel an appointment
    """
    global df_appointments
    global df_doctors
    global df_patients
    global appointments
    global doctors

    datetime_string = date + time
    datetime_object = datetime.strptime(datetime_string, '%Y-%m-%d%H:%M:%S')
    if(doctor_name is None and patient_name is None):
        logging.error("Invalid appointment details")
        return False

    if(doctor_name is not None):
        try:
            doctor_id = [
                doc.doctor_id for doc in doctors if doc.doctor_name == doctor_name][0]
            print(doctor_id)
            doctor_id = df_doctors[df_doctors['name']
                                   == doctor_name]['id'].values[0]
        except:
            logging.error(' Doctor not found')
            return False
        same_day_apps = get_appointments(
            doctor_name, date, 'doctor')

        if(len(same_day_apps) == 0):
            logging.error("No appointments found")
            return False
        for _, row in same_day_apps.iterrows():
            if(row['appointment_datetime'].strftime('%H:%M:%S') == time):
                df_appointments = df_appointments[df_appointments['appointment_id']
                                                  != row['appointment_id']]
                return True
        logging.error("No appointments found")
        return False
    elif(patient_name is not None):
        try:
            patient_id = df_patients[df_patients['name']
                                     == patient_name]['id'].values[0]
        except:
            logging.error(' Patient not found')
            return False
        same_day_apps = get_appointments(
            patient_name, date, 'patient')
        if(len(same_day_apps) == 0):
            logging.error("No appointments found")
            return False

        appointments = [appointment for appointment in appointments if appointment.time != datetime_object and (
            (appointment.doctor_id != doctor_id if doctor_id != None else False) or (appointment.patient_id != patient_id if patient_id != None else False))]

        for _, row in same_day_apps.iterrows():
            if(row['appointment_datetime'].strftime('%H:%M:%S') == time):
                df_appointments = df_appointments[df_appointments['appointment_id']
                                                  != row['appointment_id']]
                return True
        logging.error("No appointments found")
        return False


if __name__ == '__main__':

    df = read_from_csv('./data.csv')

    patients = []
    doctors = []
    appointments = []

    df_people = pd.DataFrame(
        columns=['patient_id', 'patient_name', 'patient_age', 'patient_gender'])
    df_doctors = pd.DataFrame(columns=['id', 'name'])

    for index, row in df.iterrows():
        patients.append(Patient(row['patient_id'], row['patient_name'],
                                row['patient_age'], row['patient_gender']))
        doctors.append(Doctor(row['doctor_id'], row['doctor_name']))
        appointments.append(Appointment(
            row['doctor_id'], row['patient_id'], row['appointment_datetime']))
    print([doc.doctor_id for doc in doctors])
    df_patients = pd.DataFrame.from_records(
        [patient.to_dict() for patient in patients])
    df_doctors = pd.DataFrame.from_records(
        [doctor.to_dict() for doctor in doctors])
    df_appointments = pd.DataFrame.from_records(
        [appointment.to_dict() for appointment in appointments])

   # print(get_appointments('D1Name', "2018-03-08", 'doctor'))

    if(create_appointment('P3Name', 'D1Name', '2022-04-03',
                          '15:00:00', df_doctors, df_patients)):
        print("Appointment created")

    if(create_appointment('P3Name', 'D1Name', '2022-04-03',
                          '14:00:00', df_doctors, df_patients)):
        print("Appointment created")
    print(get_appointments('D1Name', "2022-04-03", 'doctor'))
    if(cancel_appointment('D1Name', None, "2022-04-03", '15:00:00')):
        print("Appointment cancelled")
    print(get_appointments('D1Name', "2022-04-03", 'doctor'))
