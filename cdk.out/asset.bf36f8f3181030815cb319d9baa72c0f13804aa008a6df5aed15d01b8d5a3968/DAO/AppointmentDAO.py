from abc import ABC, abstractmethod

class AppointmentDAO(ABC):
    @abstractmethod
    def getAllappointments(self):
        pass
    @abstractmethod
    def getappointment(self, appointmentId):
        pass
    @abstractmethod
    def updateappointment(self, appointmentId, filed: dict):
        pass
    @abstractmethod
    def deleteappointment(self, appointmentId):
        pass
    @abstractmethod
    def addappointment(self, appointmentItem):
        pass