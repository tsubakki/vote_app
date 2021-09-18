from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'audition'

urlpatterns = [
    path('vote/', views.VoteView.as_view(), name='vote'),
    path('vote/result/', views.VoteResultView.as_view(), name='result'),
    path('vote/admin_result/', views.VoteAdminResultView.as_view(), name='admin_result'),
    path('accounts/profile/', views.ProfileView.as_view(), name='accounts/profile'),
    path('accounts/signup/', views.SignUpView.as_view(), name='accounts/signup'),
    path('accounts/delete_confirm', TemplateView.as_view(template_name='registration/delete_confirm.html'), name='accounts/delete-confirmation'),
    path('accounts/delete_complete', views.DeleteView.as_view(), name='accounts/delete-complete'),
    path('accounts/password_change/', views.PasswordChange.as_view(), name='accounts/password_change'),
    path('accounts/password_change/done/', views.PasswordChangeDone.as_view(), name='accounts/spassword_change_done'),
]