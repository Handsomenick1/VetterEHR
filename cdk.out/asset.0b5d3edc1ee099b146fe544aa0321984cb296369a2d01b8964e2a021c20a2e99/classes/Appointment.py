import uuid
import json

class Appointment:
    def __init__(self, list_info) -> None:
        self.id = list_info["appointmentId"]
        self.clinicId = list_info["clinicId"]
        self.customerId = list_info["customerId"]
        self.appointmentDate = list_info["appointmentDate"]
        self.doctorId = "N/A"
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

    def setdoctorId(self, doctorId):
        self.doctorId = doctorId
        return True
    

    def getAmenitiesInfoJson(self):
        return json.dumps({
            "appointmentId" : self.getId(),
            "clinicId" : self.getclinicId(),
            "customerId" : self.getcustomerId(),
            "appointmentDate" : self.getappointmentDate(),
            "doctorId" : self.getdoctorId(),
            "reason" : self.getreason()
        })  

    def getAmenitiesInfo(self):
        return {
            "appointmentId" : self.getId(),
            "clinicId" : self.getclinicId(),
            "customerId" : self.getcustomerId(),
            "appointmentDate" : self.getappointmentDate(),
            "doctorId" : self.getdoctorId(),
            "reason" : self.getreason()
        }