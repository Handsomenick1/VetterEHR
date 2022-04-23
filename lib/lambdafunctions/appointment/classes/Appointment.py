import uuid
import json
from appointment.constants.AppointmentStatus import AppointmentStatus

class Appointment:
    def __init__(self, list_info) -> None:
        self.id = list_info["appointmentId"]
        self.clinicId = list_info["clinicId"]
        self.customerId = list_info["customerId"]
        self.appointmentDate = list_info["appointmentDate"]
        self.doctorId = "N/A"
        self.status = AppointmentStatus.UNCONFIRM.value
        self.reason = list_info["reason"]

    def getId(self):
        return self.id
    
    def getclinicId(self):
        return self.clinicId

    def getcustomerId(self):
        return self.customerId

    def getappointmentDate(self):
        return self.appointmentDate

    def getreason(self):
        return self.reason
    
    def getdoctorId(self):
        return self.doctorId

    def getstatus(self):
        return self.status
    
    def setdoctorId(self, doctorId):
        self.doctorId = doctorId
        return True
    
    def setstatus(self, appointmentstatus):
        self.status = appointmentstatus
        return True
        
    def getAppointmentJson(self):
        return json.dumps({
            "appointmentId" : self.getId(),
            "clinicId" : self.getclinicId(),
            "customerId" : self.getcustomerId(),
            "appointmentDate" : self.getappointmentDate(),
            "doctorId" : self.getdoctorId(),
            "appointmentStatus" : self.getstatus(),
            "reason" : self.getreason()
        })  

    def getAppointmentInfo(self):
        return {
            "appointmentId" : self.getId(),
            "clinicId" : self.getclinicId(),
            "customerId" : self.getcustomerId(),
            "appointmentDate" : self.getappointmentDate(),
            "doctorId" : self.getdoctorId(),
            "appointmentStatus" : self.getstatus(),
            "reason" : self.getreason()
        }