from model.doctor_list import DoctorList
from model.appointment_list import AppointmentList
from controller.appointment_controller import AppointmentController
from flask import Flask
from view.flask_wrapper import FlaskAppWrapper
from model.patient_list import PatientList
flask_app = Flask(__name__)

app = FlaskAppWrapper(flask_app)

dl = DoctorList()
pl = PatientList()
al = AppointmentList()
ac = AppointmentController()


app.add_endpoint('/api/add',
                 'add_app', ac.create_appointment)

app.add_endpoint('/api/cancel',
                 'cancel_app', ac.cancel_appointment)

app.add_endpoint('/api/get',
                 'get_doc_appointments', ac.get_appointments)

app.add_endpoint('/api/all', 'get_all_appointments', ac.get_all_appointments)

if __name__ == "__main__":
    app.run(debug=True)
