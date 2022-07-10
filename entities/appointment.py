class Appointment:
    """
        Class created for defining the appointment relation
    """

    def __init__(self, appointment_id, doctor_id, patient_id, time) -> None:
        self.appointment_id = appointment_id
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.time = time

    def to_dict(self):
        """
            This function aids in the creation of a dataframe
        """
        return {
            'appointment_id': self.appointment_id,
            'doctor_id': self.doctor_id,
            'patient_id': self.patient_id,
            'appointment_datetime': self.time
        }
