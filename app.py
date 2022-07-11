from model.doctor_list import DoctorList
from model.appointment_list import AppointmentList
from controller.appointment_controller import AppointmentController
from flask import Flask
from view.flask_wrapper import FlaskAppWrapper
from model.patient_list import PatientList
from controller.doctor_controller import DoctorController
from controller.patient_controller import PatientController

flask_app = Flask(__name__)

app = FlaskAppWrapper(flask_app)

dl = DoctorList()
pl = PatientList()
al = AppointmentList()
ac = AppointmentController()
dc = DoctorController()
pc = PatientController()


app.add_endpoint('/api/add',
                 'add_app', ac.create_appointment, methods=['POST'])

app.add_endpoint('/api/cancel',
                 'cancel_app', ac.cancel_appointment, methods=['DELETE'])

app.add_endpoint('/api/get',
                 'get_doc_appointments', ac.get_appointments)

app.add_endpoint('/api/all', 'get_all_appointments', ac.get_all_appointments)

# extra endpoint to fetch via ID
app.add_endpoint('/api/get_by_id', 'get_apps_by_id', ac.get_appointments_by_id)

# get doctor details by ID
app.add_endpoint('/api/get/doctor', 'get_doc_by_id', dc.get_doctor_details)

# add doctor
app.add_endpoint('/api/add/doctor', 'add_doc',
                 dc.create_doctor, methods=['POST'])

# delete doctor by ID
app.add_endpoint('/api/delete/doctor', 'delete_doctor',
                 dc.delete_doctor, methods=['DELETE'])

# get patient details by ID
app.add_endpoint('/api/get/patient', 'get_patient_by_id',
                 pc.get_patient_details)

# add patient
app.add_endpoint('/api/add/patient', 'add_patient',
                 pc.create_patient, methods=['POST'])

# delete patient by ID
app.add_endpoint('/api/delete/patient', 'delete_patient',
                 dc.delete_doctor, methods=['DELETE'])

# view all doctors
app.add_endpoint('/api/get/doctors', 'get_all_docs', dc.get_all_doctors)

# view all patients
app.add_endpoint('/api/get/patients', 'get_all_patients', pc.get_all_patients)


if __name__ == "__main__":
    app.run(debug=True)
