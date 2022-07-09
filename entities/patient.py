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
