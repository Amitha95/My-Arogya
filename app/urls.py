from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",views.index,name="index"),
    path("index",views.index,name="index"),
    path("login",views.Login,name="login"),
    path("admin",views.admin,name="admin"),
    path("staff",views.staff,name='staff'),
    path("Logout",views.Logout,name='Logout'),
    path("Privacy",views.Privacy,name='Privacy'),
    path("Appoint_Staff",views.Appoint_Staff,name='Appoint_Staff'),
    path("List_Staff",views.List_Staff,name='List_Staff'),
    path("delete_staff",views.delete_staff,name='delete_staff'),
    path("complaintsrply",views.complaintsrply,name='complaintsrply'),
    path("All_Users",views.All_Users,name='All_Users'),
    path("remove_usr",views.remove_usr,name='remove_usr'),
    path("Profile",views.Profile,name='Profile'),
    path("ops",views.ops,name='ops'),
    path("op_history",views.op_history,name='op_history'),
    path("Casesheet",views.Casesheet,name='Casesheet'),
    path("op_absent",views.op_absent,name='op_absent'),
    path("Case_report",views.Case_report,name='Case_report'),
    path("report",views.report,name='report'),
    path("user",views.user,name="user"),
    path("userreg",views.userreg,name="userreg"),
    path("complaints",views.complaints,name="complaints"),
    path("regOp",views.regOp,name="regOp"),
    path("oplist",views.oplist,name="oplist"),
    path("casesheetlist",views.casesheetlist,name="casesheetlist"),
    path("profileeditcandid",views.profileeditcandid,name="profileeditcandid"),
    path("profileeditscandid",views.profileeditscandid,name="profileeditscandid"),
    
    path("add_department",views.add_department,name="add_department"),
    path("department_list",views.department_list,name="department_list"),
    path("fetch_doctors",views.fetch_doctors,name="fetch_doctors"),
    path("appointment_list",views.appointment_list,name="appointment_list"),
    path("accept_appointment/<int:op_id>/",views.accept_appointment,name="accept_appointment"),
    path("reject_appointment/<int:op_id>/",views.reject_appointment,name="reject_appointment"),
    path("user_panel_view",views.user_panel_view,name="user_panel_view"),
    path('allot_room/<int:casesheet_id>/', views.allot_room, name='allot_room'),
    path("appointments_today",views.appointments_today,name="appointments_today"),
    path("add_casesheet/<int:op_id>/",views.add_casesheet,name="add_casesheet"),
    path("casesheet_doctor",views.casesheet_doctor,name="casesheet_doctor"),
    path("casesheet_list_view",views.casesheet_list_view,name="casesheet_list_view"),
    path("room_list",views.room_list,name="room_list"),
    path("add_room",views.add_room,name="add_room"),
    path('rooms/edit/<int:room_id>/', views.edit_room, name='edit_room'),
    path('rooms/delete/<int:room_id>/', views.delete_room, name='delete_room'),
    path('prescribe_medicine/<int:casesheet_id>/', views.prescribe_medicine, name='prescribe_medicine'),



   



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
