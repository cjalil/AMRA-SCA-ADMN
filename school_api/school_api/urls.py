from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token # 👈 Import مهم
from django.conf import settings             # 👈 زيد هادي
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('pickup/create/', views.create_pickup_request),
    path('pickup/pending/', views.get_pending_requests),
    path('pickup/<int:pk>/complete/', views.complete_request),
    path('api/', views.monitor_page, name='api'), 
    path('check-security/', views.check_school_security, name='check_school_security'),
    path('api/check_scan_status/', views.check_admin_scan_status, name='check_scan_status'),
 
    path('scan/record/', views.record_school_scan),
    path('students/all/', views.get_all_students),
    path('students/check-version/', views.check_db_version),
    path('api-token-auth/', views.custom_login, name='api_token_auth'),

    # 1. رابط الصفحة (فيه الكود)
    path('monitor/view/<str:school_key>/', views.monitor_page, name='monitor_view'),
    # 2. رابط الداتا (فيه الكود)
    path('monitor/data/<str:school_key>/', views.get_monitor_data, name='monitor_data'),
    path('monitor/cdnpdata/<str:school_key>/', views.get_monitor_cdnpdata, name='monitor_cdnpdata'),
    
     
    path('scan/clear/', views.clear_daily_scans),
    #إدارة التلاميذ
    path('manage/', views.manage_students, name='manage_students'),
    path('manage_admin/', views.manage_admin, name='manage_admin'),
    path('manageNC/', views.manage_students_NC, name='manage_students_NC'),
    path('manage/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('manageNC/edit/<int:student_id>/', views.edit_studentNC, name='edit_studentNC'),
    
    
    
    path('login/', auth_views.LoginView.as_view(template_name='school_login.html'), name='school_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='school_login'), name='school_logout'),
    path('school/update-location/', views.update_school_location),
    path("api/schools/<int:school_id>/ports/", views.school_ports, name="school_ports"),
    path("api/schools/<int:school_id>/ports/rename/", views.rename_port_api, name="rename_port"),

    
   
    # هادي هي الجديدة ديال الويب:
    path('dashboard/', views.school_dashboard, name='school_dashboard'),
    path('school/set-badge/', views.set_admin_badge),
    path('school/get-config/', views.get_school_config),
    path('scan/<str:school_slug>/', views.public_school_scan),
    path('student-qr/<str:school_key>/<int:student_id>/', views.generate_student_qr, name='generate_student_qr'),
    path('student-qrNC/<str:school_key>/<int:student_id>/', views.generate_student_qrNC, name='generate_student_qrNC'),
    path('save-class-order/', views.save_class_order, name='save_class_order'),
    path('delete-class/<int:class_id>/', views.delete_class, name='delete_class'), 
     
    path('conditions-dutilisation/', views.cgu_page, name='cgu_page'),
    path('pickup-history/', views.pickup_history, name='pickup_history'),
    
    
    path('presence/classes/', views.school_classes_list, name='school_classes_list'),
    path('presence/manage/<str:api_key>/<str:class_name>/', views.manage_attendance, name='manage_attendance'),

    # URL l-admin bach ychouf l-listat dyal l-youm
    path('presence/dashboard/', views.admin_presence_dashboard, name='admin_presence_dashboard'),
    path('upload-excel/', views.upload_all_students_excel, name='upload_all_students_excel'),    
    path('portal/', views.school_portal, name='school_portal'),
    path('clear-students/', views.clear_all_students, name='clear_all_students'),
    path('attendance/delete/<int:presence_id>/', views.delete_presence, name='delete_presence'),
    path('download-template/', views.download_template, name='download_template'),
    path('get-students/<str:class_name>/', views.get_students_by_class, name='get_students_by_class'),
    path('save-student/', views.save_student_ajax, name='save_student_ajax'),
    path('delete-student/<int:student_id>/', views.delete_student_ajax, name='delete_student_ajax'),
    path('export-all/', views.export_all_students, name='export_all_students'),
    path('export-class/<str:class_name>/', views.export_class_students, name='export_class_students'),

    path('delete-class/<str:class_name>/', views.delete_school_class, name='delete_school_class'),
    path('search-student/', views.search_student, name='search_student'),
    path('student-history/<int:student_id>/', views.student_history, name='student_history'),
    
    
    
     
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)