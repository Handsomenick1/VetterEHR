import sys 
sys.path.append("..")
import enum

class AppointmentStatus(enum.Enum):
    UNCONFIRM = "UNCONFIRM"
    CONFIRM = "CONFIRMED"
    CANCEL = "CANCELED"