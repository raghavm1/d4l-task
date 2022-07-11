from flask import request
from flask import jsonify
from entities import appointment
from model.appointment_list import AppointmentList
from model.doctor_list import DoctorList
from entities.doctor import Doctor
import uuid


class DoctorController:
    def get_all_doctors(self):
        """
            Get details of all doctors
        """
        return jsonify([doctor.to_dict() for doctor in DoctorList.list_docs])

    def get_doctor_details(self):
        """
            Pass in the doctor ID and get the doctor details
        """
        id = request.args.get("id")
        return jsonify([doctor for doctor in DoctorList.list_docs if id == doctor.doctor_id][0].to_dict())

    def create_doctor(self):
        """
            Create a new doctor detail
        """
        name = request.args.get("name")
        DoctorList.list_docs.append(
            Doctor(doctor_name=name, doctor_id=uuid.uuid1()))
        return "Success"

    def delete_doctor(self):
        """
            Delete doctor details
        """
        id = request.args.get("id")
        for doctor in DoctorList.list_docs:
            if doctor.doctor_id == id:
                AppointmentList.list_appointments = [
                    appointment for appointment in AppointmentList.list_appointments if appointment.doctor_id != id]
                DoctorList.list_docs.remove(doctor)
                return "Success"
        return "Doctor not found"
