import os
import boto3
import sys 
sys.path.append("..")
from DAO.AppointmentDAO import AppointmentDAO
from aws_helper.dynamoDB import update_item_db, scan_items_db, put_item_db

region = os.environ["region"]
appointment_table = os.environ["appointment_table"]
class AppointmentDAOimpl(AppointmentDAO):
   
    def __init__(self) -> None:
        self.appointmentTable = boto3.resource("dynamodb", region).Table(appointment_table)
        self.appointments = {}
    #override
    def getAllAppointments(self):
        self.appointments = scan_items_db(self.appointmentTable)
        return self.appointments

    #override
    def getAppointment(self, AppointmentId):
        self.appointments = scan_items_db(self.appointmentTable)
        for Appointment in self.appointments:
            if Appointment.get("appointmentId") == AppointmentId:
                return Appointment
        return None
    
    #override
    def updateAppointment(self, appointmentId, fileds: dict):
        try:
            for key in fileds:
                update_item_db(self.appointmentTable, "appointmentId", appointmentId, key, fileds.get(key))
            return True
        except Exception as e:
            return str(e)

    #override
    def deleteappointment(self, appointmentId):
        return super().deleteappointment(appointmentId)
    
    # Override
    def addAppointment(self, appointmentItem):
        put_item_db(self.appointmentTable, appointmentItem)
        return True

    def getAppointmentbycustomerId(self, userId):
        self.appointments = scan_items_db(self.appointmentTable)
        list = []
        for appointment in self.appointments:
            if appointment.get("userId") == userId:
                list.append(appointment)
        if list:
            return list
        
        return None

    def getAppointmentbyclinicId(self, clinicId):
        self.appointments = scan_items_db(self.appointmentTable)
        list = []
        for appointment in self.appointments:
            if appointment.get("clinicId") == clinicId:
                list.append(appointment)
        if list:
            return list
        
        return None