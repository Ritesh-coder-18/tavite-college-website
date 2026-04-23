from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('courses/', views.courses, name='courses'),
    path('notes/bca/', views.notes_dashboard, name='notes_dashboard'),
    path('notes/subject/<int:subject_id>/', views.subject_notes, name='subject_notes'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('test/', views.test, name='test'),
    path('events/', views.events, name='events'),
    path('bca-papers/', views.bca_papers, name='bca_papers'),
    path('notices/', views.notice_page, name='notices'),
    path('results/', views.results_page, name='results'),
    path('messages/', views.teacher_messages, name='teacher_messages'),
    path('google407a2edeb44b4096.html', TemplateView.as_view(template_name='google407a2edeb44b4096.html')),
]