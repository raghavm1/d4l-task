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
