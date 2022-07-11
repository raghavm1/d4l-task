from flask import request
from flask import jsonify
from entities import appointment
from model.appointment_list import AppointmentList
from model.patient_list import PatientList
from entities.patient import Patient
import uuid


class PatientController:
    def get_all_patients(self):
        """
            Get details of all doctors
        """
        return jsonify([patient.to_dict() for patient in PatientList.list_patients])

    def get_patient_details(self):
        """
            Pass in the patient ID and get the patient details
        """
        id = request.args.get("id")
        return jsonify([patient for patient in PatientList.list_patients if id == patient.patient_id][0].to_dict())

    def create_patient(self):
        """
            Create a new doctor detail
        """
        name = request.args.get("name")
        gender = request.args.get("gender")
        age = request.args.get("age")

        PatientList.list_patients.append(
            Patient(patient_name=name, patient_id=uuid.uuid1(), patient_gender=gender, patient_age=age))

    def delete_doctor(self):
        """
            Delete doctor details
        """
        id = request.args.get("id")
        for patient in PatientList.list_patients:
            if patient.patient_id == id:
                AppointmentList.list_appointments = [
                    appointment for appointment in AppointmentList.list_appointments if appointment.patient_id != id]
                PatientList.list_patients.remove(patient)
                return "Success"
        return "Patient not found"
