from controller.appointment_controller import AppointmentController
from model.appointment_list import AppointmentList
from model.doctor_list import DoctorList
#from model.patient_list import PatientList

# AL = AppointmentList()
# AL.print_all_appointments()

dl = DoctorList()
al = AppointmentList()
dl.print_doctor_details('D1')

ac = AppointmentController()


ac.cancel_appointment(doctor_name='D1Name',
                      date='2018-03-08', time='09:00:00')
for app in AppointmentList.list_appointments:
    print(app.to_dict())

ac.create_appointment(doctor_name='D1Name', time="09:00:00",
                      date="2022-07-10", patient_name='P1Name')

print("\n\n")
for app in AppointmentList.list_appointments:
    print(app.to_dict())
