from django.db import models
from datetime import date

# Create your models here.

class login(models.Model):
    logid = models.AutoField(primary_key=True)
    username = models.CharField("username",max_length=100)
    password =  models.CharField("password",max_length=100)
    role=models.CharField('role',max_length=10)
    #logid,username,password,role
    
class user(models.Model):
    User_id= models.AutoField(primary_key=True)
    User_name=models.CharField("uname", max_length=200)
    User_address=models.CharField("address", max_length=200)
    User_email=models.CharField("email", max_length=100)
    User_phone=models.CharField("phone", max_length=100)
    User_alt_No=models.CharField("altno", max_length=200)
    User_status=models.CharField("status", max_length=200)
    Log_id=models.ForeignKey(login, on_delete=models.CASCADE, null=True)
#User_id,User_name,User_address,User_email,User_phone,User_alt_No,Log_id,User_status

class Staff(models.Model):
   Staff_id= models.AutoField(primary_key=True)
   Staff_name= models.CharField("Name",max_length=100)
   Staff_address = models.CharField("Staff_address", max_length=500)
   Staff_email = models.EmailField("Staff_email", max_length=200)
   Staff_phone=models.CharField("Staff_phone",max_length=100)
   Staff_qualification = models.CharField("Staff_qualification", max_length=200)
   Staff_designation = models.CharField("Staff_designation", max_length=100)
   Staff_experience = models.CharField("Staff_experience", max_length=100)
   Staff_photo = models.FileField("Staff_photo", max_length=1000,upload_to='images/')
   Staff_status=models.CharField("Staff_status",max_length=50,default="")
   Staff_logid=models.ForeignKey(login, on_delete=models.CASCADE, null=True)
   
   def __str__(self):
        return self.staff_name
   def get_appointments_today(self):
        today = date.today()
        return op_ticket.objects.filter(Staff=self, op_date=str(today))


class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField("Name", max_length=100)
    doctors = models.ManyToManyField(Staff, related_name='departments')

    def __str__(self):
        return self.department_name
#Staff_id,Staff_name,Staff_address,Staff_email,Staff_phone,Staff_qualification, Staff_designation,Staff_experience,Staff_photo,Staff_status,Staff_logid

class op_ticket(models.Model):
    op_id = models.AutoField(primary_key=True)
    op_date = models.CharField("date", max_length=100)
    op_status = models.CharField("status", max_length=100)
    User = models.ForeignKey(user, on_delete=models.CASCADE, null=True)
    op_type = models.CharField("type", max_length=100)
    op_no = models.CharField("op_no", max_length=100)  # Add the op_no field
    Staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    def save(self, *args, **kwargs):
        if not self.pk:
            # Generate a new op_no for new records
            last_op = op_ticket.objects.order_by('-op_id').first()
            if last_op:
                self.op_no = str(int(last_op.op_no) + 1)
            else:
                self.op_no = '1'
        super().save(*args, **kwargs)

#op_id,op_date,op_no,op_status,User,op_type

class record(models.Model):
    record_id= models.AutoField(primary_key=True)
    op=models.ForeignKey(op_ticket, on_delete=models.CASCADE, null=True)
    User=models.ForeignKey(user, on_delete=models.CASCADE, null=True)
    record_detail=models.CharField("record",max_length=100)
    record_date=models.CharField("date",max_length=100)

#record_id,op,User,record_detail,record_date

class Complaint(models.Model):
    Complaint_id= models.AutoField(primary_key=True)
    Complaint_subject= models.CharField("subject", max_length=100)
    Complaint_message= models.CharField("message", max_length=500)
    Complaint_date= models.CharField("date", max_length=100)
    Complaint_reply= models.CharField("replay", max_length=500)
    User_id =models.ForeignKey(user, on_delete=models.CASCADE, null=True)
    
class Room(models.Model):
    room_number = models.CharField(max_length=100, unique=True)
    floor = models.IntegerField()
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Room {self.room_number}, Floor {self.floor}"


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.patient_name
    
class CaseSheet(models.Model):
    casesheet_id = models.AutoField(primary_key=True)
    patient = models.CharField(max_length=100)
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    symptoms = models.TextField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    status = models.CharField(max_length=100, default="added")
    admit = models.BooleanField(default=False)   # Add the admit field
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Case Sheet #{self.casesheet_id} - {self.patient}"

class Prescription(models.Model):
    casesheet = models.ForeignKey(CaseSheet, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)

    def __str__(self):
        return f"Prescription for Case Sheet #{self.casesheet.casesheet_id}"


#Complaint_id,Complaint_subject,Complaint_message,Complaint_date,Complaint_reply,User_id


