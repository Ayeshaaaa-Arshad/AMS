class AppointmentDateException(Exception):
    def __init__(self, message="Appointment date cannot be in the past."):
        self.message = message
        super().__init__(self.message)
