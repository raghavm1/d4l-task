from datetime import datetime
from html import entities
from model.doctor_list import DoctorList
from model.patient_list import PatientList
from model.appointment_list import AppointmentList
from entities.appointment import Appointment
import datetime as dt_time
from flask import jsonify
from flask import request


class AppointmentController:

    def appointment_handler(self, name, date, entity_type):
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

    def get_appointments(self):
        """
            Function to get appointments for a given entity
        """
        name = request.args.get('name')
        date = request.args.get('date')
        entity_type = request.args.get('entity_type')
        return jsonify([app.to_dict() for app in self.appointment_handler(name, date, entity_type)])

    def create_appointment(self):
        """
            Function to create an appointment
        """
        date = request.args.get('date')
        time = request.args.get('time')
        doctor_name = request.args.get('doctor_name')
        patient_name = request.args.get('patient_name')
        # Return error on invalid appointment time (i.e. at 3PM or beyond 4PM)
        if(datetime.strptime(time, "%H:%M:%S").time() > datetime.strptime("15:00:00", "%H:%M:%S").time() or datetime.strptime(time, "%H:%M:%S").time() < datetime.strptime("08:00:00", "%H:%M:%S").time()):
            return "Invalid appointment time: Doctors are available only from 8AM till 4PM"

        # First, check if the given date and time checks out for the doctor
        datetime_string = date + time
        datetime_object = datetime.strptime(
            datetime_string, '%Y-%m-%d%H:%M:%S')

        try:
            list_of_doctors = DoctorList().list_docs

            doctor_id = [
                doctor.doctor_id for doctor in list_of_doctors if doctor.doctor_name == doctor_name][0]
        except:
            return 'Doctor not found'

        try:
            list_of_patients = PatientList().list_patients

            patient_id = [
                patient.patient_id for patient in list_of_patients if patient.patient_name == patient_name][0]
        except:
            return 'Patient not found'

        doctor_apps = self.appointment_handler(
            doctor_name, datetime_object, 'doctor')
        patient_apps = self.appointment_handler(
            patient_name, datetime_object, 'patient')

        if(len(doctor_apps) > 0):
            for d_app in doctor_apps:
                if(abs(d_app.time - datetime_object) < dt_time.timedelta(minutes=60)):
                    return "Doctor is not available on the given date and time"
        if(len(patient_apps) > 0):
            for p_app in patient_apps:
                if(abs(p_app.time - datetime_object) < dt_time.timedelta(minutes=60)):
                    return "Patient is not available on the given date and time"

        appointment_id = 'A' + doctor_id + patient_id + \
            datetime_object.strftime('%y%m%d%H')
        AppointmentList.list_appointments.append(Appointment(appointment_id,
                                                             doctor_id, patient_id, datetime_object))
        return str(True)

    def cancel_appointment(self):
        """
            Function to cancel an appointment
        """
        doctor_name = request.args.get("doctor_name")
        patient_name = request.args.get("patient_name")
        time = request.args.get("time")
        date = request.args.get("date")
        if(doctor_name is None and patient_name is None):
            return "Invalid appointment details"

        if doctor_name is not None:

            try:
                list_docs = DoctorList.list_docs
                doctor_id = [
                    doc.doctor_id for doc in list_docs if doc.doctor_name == doctor_name][0]
            except:
                return 'Doctor not found'

            same_day_apps = self.appointment_handler(
                doctor_name, date, 'doctor')
            if not same_day_apps:
                return "No appointments found"

            for app in same_day_apps:
                if app.time.strftime('%H:%M:%S') == time:
                    AppointmentList.list_appointments.remove(app)
                    return str(True)
            return "No appointments found"

        elif patient_name is not None:
            try:
                list_patients = PatientList.list_patients
                patient_id = [
                    patient.id for patient in list_patients if patient.patient_name == patient_name][0]
            except:
                return 'Patient not found'

            same_day_apps = self.appointment_handler(
                patient_name, date, 'patient')
            if not same_day_apps:
                return "No appointments found"

            for app in same_day_apps:
                if app.appointment_datetime.strftime('%H:%M:%S') == time:
                    AppointmentList.list_appointments.remove(app)
                    return str(True)

            return "No appointments found"

    def get_all_appointments(self):
        return jsonify([appointment.to_dict() for appointment in AppointmentList.list_appointments])
