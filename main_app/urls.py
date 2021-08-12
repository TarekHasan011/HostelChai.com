from django.urls import path
from django.conf import settings
from django.conf.urls import *
from django.conf.urls.static import static
from . import views

handler500 = 'main_app.views.error_500'

app_name = 'main_app'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('setup_admin_page/', views.setup_admin_page, name='setup_admin_page'),
    path('setup_admin/', views.setup_admin, name='setup_admin'),
    path('requests_loader_page/', views.requests_loader_page, name='requests_loader_page'),
    path('requests_loader/', views.requests_loader, name='requests_loader'),
    path('ad_approval_page/', views.ad_approval_page, name='ad_approval_page'),
    path('approve_ad/<ads_id>/', views.approve_ad, name='approve_ad'),
    path('hostel_approval_page/', views.hostel_approval_page, name='hostel_approval_page'),
    path('approve_hostel/', views.approve_hostel, name='approve_hostel'),
    path('user_approval_page/', views.user_approval_page, name='user_approval_page'),
    path('approve_user/<user_id>/<int:user_type>/', views.approve_user, name='approve_user'),
    path('registration_page/', views.registration_page, name='registration_page'),
    path('student_registration/', views.student_registration, name='student_registration'),
    path('hostel_owner_registration/', views.hostel_owner_registration, name='hostel_owner_registration'),
    path('login_page/', views.login_page, name='login_page'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home_page/', views.home_page, name='home_page'),
    path('admin_home_page/', views.admin_home_page, name='admin_home_page'),
    path('student_home_page/', views.student_home_page, name='student_home_page'),
    path('hostel_owner_home_page/', views.hostel_owner_home_page, name='hostel_owner_home_page'),
    path('profile_page/<int:user>/<user_id>/', views.profile_page, name='profile_page'),
    path('admin_profile_page/<user_id>/', views.admin_profile_page, name='admin_profile_page'),
    path('student_profile_page/<user_id>/', views.student_profile_page, name='student_profile_page'),
    path('hostel_owner_profile_page/<user_id>/', views.profile_page, name='hostel_owner_profile_page'),
    path('add_hostel_page/', views.add_hostel_page, name='add_hostel_page'),
    path('add_hostel/', views.add_hostel, name='add_hostel'),
    path('process_hostel_review_and_rating/<user_id>/<hostel_id>/', views.process_hostel_review_and_rating, name='process_hostel_review_and_rating'),
    path('ad_posting_page/', views.ad_posting_page, name='ad_posting_page'),
    path('ad_posting/', views.ad_posting, name='ad_posting'),
    path('ads_feed_page/<int:page_number>/<location>/<institute>/<budget_from>/<budget_to>/', views.ads_feed_page, name='ads_feed_page'),
    path('complaint_box_page/', views.complaint_box_page, name='complaint_box_page'),
    path('complaint_box/', views.complaint_box, name='complaint_box'),
    path('complaint_checker_page/<complaint_id>/', views.complaint_checker_page, name='complaint_checker_page'),
    path('complaint_checker_page/', views.complaint_checker_page, name='complaint_checker_page'),
    path('resolve_complaint/<complaint_id>/', views.resolve_complaint, name='resolve_complaint'),
    path('test_page/', views.test_page, name='test_page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
