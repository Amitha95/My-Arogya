from django.shortcuts import render,redirect,get_object_or_404
import datetime
from datetime import date
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from .models import user as usr,login as log,Staff as stf,Complaint as comp,op_ticket as op,record as rd,Department as dept,Patient,Room,CaseSheet as case,Prescription
from django.core.mail import send_mail
from django.http import JsonResponse
# Create your views here.
def index(request):
    msg=request.GET.get("msg",'')
    if(request.session.get('role', ' ')=="admin"):
        response = redirect('/admin')
        return response
    elif(request.session.get('role', ' ')=="staff"):
        response = redirect('/staff')
        return response
    else:
        return render(request,"index.html",{"msg":msg})
def admin(request):
    if(request.session.get('role', ' ')=="admin"):
        return render(request,"adminhome.html")
    else:
        response = redirect('/index'+"?msg=session expired login again")
        return response
def staff(request):
    if(request.session.get('role', ' ')=="staff"):
        return render(request,"staffhome.html")
    else:
        response = redirect('/index'+"?msg=session expired login again")
        return response

def user(request):
    if(request.session.get('role', ' ')=="user"):
        return render(request,"userhome.html")
    else:
        response = redirect('/index'+"?msg=session expired login again")
        return response

def Login(request):
    if request.POST:
        user = request.POST["username"]
        password = request.POST["password"]
        try:
            data = log.objects.get(username=user, password=password)
            if (data.role == "admin"):
                request.session['username'] = data.username
                request.session['role'] = data.role
                request.session['id'] = data.logid
                response = redirect('/admin')
                return response
            elif (data.role == "staff"):
                request.session['username'] = data.username
                request.session['role'] = data.role
                request.session['id'] = data.logid
                response = redirect('/staff')
                return response
            elif (data.role == "user"):
                request.session['username'] = data.username
                request.session['role'] = data.role
                request.session['id'] = data.logid
                response = redirect('/user')
                return response
            else:
                return render(request, "index.html", {"msg": "invalid account Details"})
        except:
            return render(request, "index.html", {"msg": "invalid user name or password "})
    else:
        response = redirect('/index')
        return response

def Profile(request):
    msg=""
    ids=request.session["id"]
    if request.POST:
        if request.session["role"] =="staff":
            t2 = request.POST["t2"]
            t3 = request.POST["t3"]
            t4 = request.POST["t4"]
            stf.objects.filter(Staff_logid=ids).update(Staff_address=t2,Staff_email=t3,Staff_phone=t4)
        
    
    if request.session["role"] =="staff":
        data1=stf.objects.get(Staff_logid=ids)
        returnpage="StaffProfile.html"
    else:
        response = redirect('/index'+"?msg=session expired login again")
        return response
    return render(request,returnpage,{"msg":msg,"data":data1})
def userreg(request):
    if request.POST:
        User_name=request.POST["User_name"]
        User_address=request.POST["User_address"]
        User_email=request.POST["User_email"]
        User_phone=request.POST["User_phone"]
        User_alt_No=request.POST["User_alt_No"]
        username=request.POST["username"]
        password=request.POST["password"]
        log.objects.create(username=username,password=password,role="user")
        data=log.objects.last()
        usr.objects.create(Log_id=data,User_name=User_name,User_address=User_address,User_email=User_email,User_phone=User_phone,User_alt_No=User_alt_No,User_status="approved")
        response=redirect('/index')
        return response

def Appoint_Staff(request):
    msg=""
    if request.POST:
        t1 = request.POST["t1"]
        t2 = request.POST["t2"]
        t3 = request.POST["t3"]
        t4 = request.POST["t4"]
        t5 = request.POST["t5"]
        t6=",".join(request.POST.getlist('t6'))
        
        t7 = request.POST["t7"]
        t8 = request.FILES["t8"]
        fs = FileSystemStorage()
        fnm=fs.save(t8.name, t8)
        t9 = request.POST["t9"]
        t10 = request.POST["t10"]
        log.objects.create(username=t9, password=t10, role="staff")
        data=log.objects.last()
        stf.objects.create(Staff_name=t1,Staff_address=t2,Staff_email=t3,Staff_phone=t4,Staff_qualification=t6, Staff_designation=t5,Staff_experience=t7,Staff_photo=fnm,Staff_status="approved",Staff_logid=data)
        msg="updated successfuly"
        subject = "Archana Hospital"
        message = f"Greeting from Archana Hospital,\n you can joing our website through this username & password \n your Username: {t9}\nPassword: {t10}"
        from_email = "amithaabhay@gmail.com"  # Replace with your email address
        recipient_list = [t3]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        #return HttpResponse(t6)
    else:    
        msg = ""
    data1=stf.objects.all()
    return render(request,"Add_staff.html",{"msg":msg,"data":data1}) 

def regOp(request):
    data = stf.objects.all()
    datad = dept.objects.all()
    
    if request.method == "POST":
        t2 = request.POST["t2"]  # date
        t3 = request.POST["t3"]  # type e.g., ortho
        
        # Retrieve selected doctor and department
        doctor_id = request.POST["doctor"]
        department_id = request.POST["department"]
        doctor = stf.objects.get(pk=doctor_id)
        department = dept.objects.get(pk=department_id)
        
        top = op.objects.filter(op_type=t3, op_date=t2).count()
        nop = top + 1
        logid = request.session['id']
        logdata = usr.objects.get(Log_id=logid)
        
        # Create the op object with doctor, department, and other details
        op.objects.create(op_date=t2, op_no=str(nop), op_status="waiting", op_type=t3, User=logdata, Staff=doctor, department=department)
        
    else:
        nop = int(op.objects.latest('op_id').op_no) + 1 if op.objects.exists() else 1
    
    return render(request, "regop.html", {"op_no": nop, "data": data, "datad": datad})


def fetch_doctors(request):
    department_id = request.GET.get('department_id')

    if department_id:
        doctors = stf.objects.filter(departments__department_id=department_id)
        data = [{'id': doctor.Staff_id, 'Staff_name': doctor.Staff_name} for doctor in doctors]
        print("Doctors:", data)
        return JsonResponse({'doctors': data})

    return JsonResponse({'doctors': []})

def appointment_list(request):
    appointments = op.objects.filter(op_status="waiting").all()
    return render(request, 'appoinment_list.html',{'appointments': appointments})

def accept_appointment(request, op_id):
    # Retrieve the appointment object
    appointment = op.objects.get(op_id=op_id)

    # Update the appointment status to "Accepted"
    appointment.op_status = "Accepted"
    appointment.save()

    return redirect('appointment_list')  # Redirect to the appointment details page

def reject_appointment(request, op_id):
    # Retrieve the appointment object
    appointment = op.objects.get(op_id=op_id)

    # Update the appointment status to "Rejected"
    appointment.op_status = "Rejected"
    appointment.save()

    return redirect('appointment_list')  # Redirect to the appointment details page

def user_panel_view(request):
    appointments = op.objects.all()
    return render(request, 'appoinment_details.html', {'appointments': appointments})

def add_department(request):
    if request.method == 'POST':
        department_name = request.POST['department_name']
        selected_doctors = request.POST.getlist('doctors[]')

        department = dept.objects.create(department_name=department_name)
        department.save()  # Save the department before adding doctors

        for doctor_id in selected_doctors:
            doctor = stf.objects.get(pk=doctor_id)
            department.doctors.add(doctor)

        # You can perform additional actions or render a success message here

    doctors = stf.objects.all()

    context = {
        'doctors': doctors,
    }

    return render(request, 'select_doctors.html', context)


def department_list(request):
    departments = dept.objects.all()
    return render(request, 'department_list.html', {'departments': departments})

def oplist(request):
    data=op.objects.all()
    return render(request,"oplist.html",{"data":data})

def delete_staff(request):
    stf.objects.filter(Staff_id=request.GET["id"]).delete()
    response = redirect('/List_Staff')
    return response
def List_Staff(request):
    msg = ""
    data1=stf.objects.all()
    return render(request,"List_staff.html",{"msg":msg,"data":data1}) 

def profileeditcandid(request):
    t1=request.GET["t1"]
    data=stf.objects.get(Staff_id=t1)
    return render(request,"profileeditscandid.html",{"d":data})

def profileeditscandid(request):
    t1=request.GET["t1"]
    name=request.POST["n1"]
    addr=request.POST["addr"]
    phone=request.POST["phone"]
    mail=request.POST["mail"]
    lastqua=request.POST["lastqua"]
    exp=request.POST["exp"]
    toexp=request.POST["toexp"]
    stf.objects.filter(Staff_id=t1).update(Staff_name=name,Staff_address=addr, Staff_phone=phone,Staff_email=mail,
    Staff_qualification=lastqua,Staff_designation=exp,Staff_experience=toexp)
    response = redirect("List_Staff")
    return response


def Logout(request):
    try:
        del request.session['id']
        del request.session['role']
        del request.session['username']
        response = redirect("/index?id=logout")
        return response
    except:
        response = redirect("/index?id=logout")
        return response
def complaintsrply(request):
        msg=""
        #datax=usr.objects.get(Log_id=request.session["id"])
        if request.POST:
                t1 = request.POST["t1"]
                t2 = request.POST["t2"]
                
                msg="updated sucessfully"
                comp.objects.filter(Complaint_id=t1).update(Complaint_reply=t2)
        data1=comp.objects.all()
        return render(request, "Answer_Queries.html",{"msg":msg,"data":data1})
def All_Users(request):
    msg=""
    data=usr.objects.all()
    return render(request,"All_Users.html",{"msg":msg,"data":data}) 
def remove_usr(request):
    usr.objects.filter(User_id=request.GET["id"]).delete()
    response = redirect('/All_Users')
    return response


def Privacy(request):
    msg=""
    if request.POST:
        t1=request.POST["t1"]
        t2=request.POST["t2"]
        id=request.session["id"]
        data=log.objects.get(logid=id)
        if data.password==t1:
            msg="sucessfully updated"
            log.objects.filter(logid=id).update(password=t2)
        else:
            msg="invalid current password"

    returnpage="admin.html"
    if(request.session.get('role', ' ')=="staff"):
        returnpage="staff.html"
    return render(request, "privacy.html",{"role":returnpage,"msg":msg})

def ops(request):
    msg=""
    t1=request.POST.get("t1",'')
    t2=request.POST.get("t2",'')
    
    if t1 != "" and t2 != "" :
        v=datetime.datetime.strptime(t2,"%Y-%m-%d").date()
        vu=str(v.strftime("%d-%m-%Y"))
        data=op.objects.filter(op_type=t1,op_date=vu,op_status="waiting").all()
    elif t1 != "" :
        data=op.objects.filter(op_type=t1,op_status="waiting").all()
    elif t2 != "" :
        v=datetime.datetime.strptime(t2, "%Y-%m-%d").date()
        vu=str(v.strftime("%d-%m-%Y"))
        data=op.objects.filter(op_date=vu,op_status="waiting").all()
    else:
        data=op.objects.filter(op_status="waiting").all()
    return render(request, "op.html",{"msg":msg, "data":data,"t1":t1,"t2":t2})
def op_history(request):
    msg=""
    t1=request.POST.get("t1",'')
    t2=request.POST.get("t2",'')
    if t1 != "" and t2 != "" :
        v=datetime.datetime.strptime(t2,"%Y-%m-%d").date()
        vu=str(v.strftime("%d-%m-%Y"))
        data=op.objects.filter(op_type=t1,op_date=vu).exclude(op_status="waiting").all()
    elif t1 != "" :
        data=op.objects.filter(op_type=t1).exclude(op_status="waiting").all()
    elif t2 != "" :
        v=datetime.datetime.strptime(t2, "%Y-%m-%d").date()
        vu=str(v.strftime("%d-%m-%Y"))
        data=op.objects.filter(op_date=vu).exclude(op_status="waiting").all()
    else:
        data=op.objects.filter().exclude(op_status="waiting").all()
    return render(request, "op_history.html",{"msg":msg, "data":data})

def casesheetlist(request):
    
    
    data= rd.objects.all()
    return render(request, "Casesheet.html",{"data":data})

def Casesheet(request):
    msg=""
    datau=usr.objects.get(User_id=request.GET["id"])
    data= rd.objects.filter(User=datau).all()
    return render(request, "Casesheet.html",{"msg":msg, "data":data})
def op_absent(request):
    msg=""
    op.objects.filter(op_id=request.GET["id"]).update(op_status="Not Reached ")
    response = redirect('/ops')
    return response
def Case_report(request):
    msg=""
    datao=op.objects.get(op_id=request.GET["id"])
    data= rd.objects.get(op=datao)
    return render(request, "Case_report.html",{"msg":msg, "data":data})

def report(request):
    t1=request.POST["t1"]
    t2=request.POST["t2"]
    op.objects.filter(op_id=t1).update(op_status="closed")
    datao=op.objects.get(op_id=t1)
    today = date.today()
    rd.objects.create(op=datao,User=datao.User,record_detail=t2,record_date=today)
    response = redirect('/ops')
    return response

def complaints(request):
    id=request.session['id']
    datal=log.objects.get(logid=id)
    datas=usr.objects.get(Log_id=datal)
    Complaint_date=date.today()
    if request.POST:
        t1=request.POST["Complaint_subject"]
        t2=request.POST["Complaint_message"]
        comp.objects.create(User_id=datas,Complaint_subject=t1,Complaint_message=t2,Complaint_reply="",Complaint_date=Complaint_date)
    data=comp.objects.filter(User_id=datas).all()
    return render(request,"complaints.html",{"data":data})

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'rooms.html', {'rooms': rooms})

def add_room(request):
    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        floor = request.POST.get('floor')
        capacity = request.POST.get('capacity')

        room = Room.objects.create(room_number=room_number, floor=floor, capacity=capacity)
        return redirect('room_list')

    return render(request, 'add_room.html')

def edit_room(request, room_id):
    room = Room.objects.get(pk=room_id)

    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        floor = request.POST.get('floor')
        capacity = request.POST.get('capacity')

        room.room_number = room_number
        room.floor = floor
        room.capacity = capacity
        room.save()
        return redirect('room_list')

    return render(request, 'edit_room.html', {'room': room, 'room_id': room_id})



def delete_room(request, room_id):
    room = Room.objects.get(pk=room_id)
    room.delete()
    return redirect('room_list')

def appointments_today(request):
    staff_id = request.session['id']
    staff = stf.objects.get(Staff_id=staff_id)
    today = date.today()
    appointments = op.objects.filter(Staff=staff, op_date=str(today))
    return render(request, 'appointments.html', {'appointments': appointments})

def casesheet_doctor(request):
    appointments = op.objects.all()
    casesheets = []

    for appointment in appointments:
        if case.objects.filter(patient=appointment.User.User_name, doctor=appointment.Staff).exists():
            casesheet = case.objects.get(patient=appointment.User.User_name, doctor=appointment.Staff)
            casesheets.append(casesheet)

    return render(request, 'casesheet_doctor.html', {'casesheets': casesheets})

def add_casesheet(request, op_id):
    appointment = op.objects.get(op_id=op_id)

    if request.method == 'POST':
        # Retrieve the form data submitted by the user
        symptoms = request.POST.get('symptoms')
        diagnosis = request.POST.get('diagnosis')
        treatment = request.POST.get('treatment')
        admit = request.POST.get('admit') == 'yes'  # Convert the value to a boolean

        # Check if a case sheet already exists for the appointment
        if case.objects.filter(patient=appointment.User.User_name, doctor=appointment.Staff).exists():
            # Case sheet already exists, retrieve the existing case sheet
            casesheet = case.objects.get(patient=appointment.User.User_name, doctor=appointment.Staff)
            casesheet.symptoms = symptoms
            casesheet.diagnosis = diagnosis
            casesheet.treatment = treatment
            casesheet.admit = admit
            casesheet.save()
        else:
            # Create a new case sheet object
            casesheet = case.objects.create(
                patient=appointment.User.User_name,
                doctor=appointment.Staff,
                date=date.today(),
                symptoms=symptoms,
                diagnosis=diagnosis,
                treatment=treatment,
                status='added',
                admit=admit  # Set the value of the admit field
            )

        # Update the appointment status
        appointment.op_status = 'added'
        appointment.save()

        # Redirect to a success page or perform any other necessary actions
        return redirect('appointments_today')

    # Check if a case sheet already exists for the appointment
    casesheet_exists = case.objects.filter(patient=appointment.User.User_name, doctor=appointment.Staff).exists()
    if casesheet_exists:
        # Case sheet already exists, retrieve the existing case sheet
        casesheet = case.objects.get(patient=appointment.User.User_name, doctor=appointment.Staff)
        return render(request, 'add_casesheet.html', {'appointment': appointment, 'casesheet': casesheet})

    return render(request, 'add_casesheet.html', {'appointment': appointment})



def casesheet_list_view(request):
    casesheets = case.objects.all()

    return render(request, 'casesheet_list.html', {'casesheets': casesheets})

def allot_room(request, casesheet_id):
    casesheet = case.objects.get(pk=casesheet_id)
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        room = Room.objects.get(pk=room_id)
        casesheet.room = room
        casesheet.save()
        room.is_available = False
        room.save()
        return redirect('casesheet_list_view')
    rooms = Room.objects.filter(is_available=True)
    return render(request, 'allot_room.html', {'casesheet': casesheet, 'rooms': rooms})

def prescribe_medicine(request, casesheet_id):
    casesheet = case.objects.get(casesheet_id=casesheet_id)

    if request.method == 'POST':
        medicine_name = request.POST.get('medicine_name')
        dosage = request.POST.get('dosage')
        frequency = request.POST.get('frequency')

        # Create a new Prescription object
        prescription = Prescription.objects.create(
            casesheet=casesheet,
            medicine_name=medicine_name,
            dosage=dosage,
            frequency=frequency
        )

        # Redirect to the case sheet details page or perform any other necessary actions
      

    return render(request, 'prescribe_medicine.html', {'casesheet_id': casesheet_id})



























