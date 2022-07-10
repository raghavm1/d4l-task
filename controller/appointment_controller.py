from datetime import datetime
from model.doctor_list import DoctorList
from model.patient_list import PatientList
from model.appointment_list import AppointmentList
from entities.appointment import Appointment
import datetime as dt_time
import logging


class AppointmentController:
    def get_appointments(self, name, date, entity_type):
        """
            Function to get appointments for a given entity
        """
        datetime_object = date
        if(type(date) == str):
            datetime_object = datetime.strptime(date, '%Y-%m-%d')

        id = ''

        if(entity_type == 'doctor'):
            id = [
                doctor.doctor_id for doctor in DoctorList.list_docs if doctor.doctor_name == name][0]
            appointments = [appointment for appointment in AppointmentList.list_appointments if appointment.doctor_id ==
                            id and appointment.time.date() == datetime_object.date()]
        else:
            id = [
                patient.patient_id for patient in PatientList.list_patients if patient.patient_name == name][0]

            appointments = [appointment for appointment in AppointmentList.list_appointments if appointment.patient_id ==
                            id and appointment.time.date() == datetime_object.date()]
        return appointments

    def create_appointment(self, date, time, doctor_name, patient_name):
        """
            Function to create an appointment
        """
        # Return error on invalid appointment time (i.e. at 3PM or beyond 4PM)
        if(datetime.strptime(time, "%H:%M:%S").time() > datetime.strptime("15:00:00", "%H:%M:%S").time() or datetime.strptime(time, "%H:%M:%S").time() < datetime.strptime("08:00:00", "%H:%M:%S").time()):
            logging.error(
                "Invalid appointment time: Doctors are available only from 8AM till 4PM")
            return False

        # First, check if the given date and time checks out for the doctor
        datetime_string = date + time
        datetime_object = datetime.strptime(
            datetime_string, '%Y-%m-%d%H:%M:%S')

        try:
            list_of_doctors = DoctorList().list_docs

            doctor_id = [
                doctor.doctor_id for doctor in list_of_doctors if doctor.doctor_name == doctor_name][0]
        except:
            logging.error(' Doctor not found')
            return False

        try:
            list_of_patients = PatientList().list_patients

            patient_id = [
                patient.patient_id for patient in list_of_patients if patient.patient_name == patient_name][0]
        except:
            logging.error(' Patient not found')
            return False

        doctor_apps = self.get_appointments(
            doctor_name, datetime_object, 'doctor')
        patient_apps = self.get_appointments(
            patient_name, datetime_object, 'patient')

        if(len(doctor_apps) > 0):
            for d_app in doctor_apps:
                if(d_app.appointment_datetime - datetime_object < dt_time.timedelta(minutes=60)):
                    logging.error(
                        "Doctor is not available on the given date and time")
                    return False
        if(len(patient_apps) > 0):
            for p_app in patient_apps.iterrows():
                if(p_app.appointment_datetime - datetime_object < dt_time.timedelta(minutes=60)):
                    logging.error(
                        "Patient is not available on the given date and time")
                    return False

        appointment_id = 'A' + doctor_id + patient_id + \
            datetime_object.strftime('%y%m%d%H')
        AppointmentList.list_appointments.append(Appointment(appointment_id,
                                                             doctor_id, patient_id, datetime_object))
        return True

    def cancel_appointment(self, doctor_name=None, patient_name=None, date=None, time=None):
        """
            Function to cancel an appointment
        """

        datetime_string = date + time
        datetime_object = datetime.strptime(
            datetime_string, '%Y-%m-%d%H:%M:%S')
        if(doctor_name is None and patient_name is None):
            logging.error("Invalid appointment details")
            return False

        if doctor_name is not None:

            try:
                list_docs = DoctorList.list_docs
                doctor_id = [
                    doc.doctor_id for doc in list_docs if doc.doctor_name == doctor_name][0]
            except:
                logging.error(' Doctor not found')
                return False

            same_day_apps = self.get_appointments(
                doctor_name, date, 'doctor')
            if not same_day_apps:
                logging.error("No appointments found")
                return False

            for app in same_day_apps:
                if app.time.strftime('%H:%M:%S') == time:
                    AppointmentList.list_appointments.remove(app)
                    return True
            logging.error("No appointments found")
            return False

        elif patient_name is not None:
            try:
                list_patients = PatientList.list_patients
                patient_id = [
                    patient.id for patient in list_patients if patient.patient_name == patient_name][0]
            except:
                logging.error(' Patient not found')
                return False

            same_day_apps = self.get_appointments(
                patient_name, date, 'patient')
            if not same_day_apps:
                logging.error("No appointments found")
                return False

            for app in same_day_apps:
                if app.appointment_datetime.strftime('%H:%M:%S') == time:
                    AppointmentList.list_appointments.remove(app)
                    return True

            logging.error("No appointments found")
            return False
