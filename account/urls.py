from django.urls import path

from . import views
urlpatterns = [
    path('<str:uid>/<str:token>',views.ActivateUser.as_view()),#mrs
    path('reset/confirm/<str:uid>/<str:token>' , views.ConfirmPassword.as_view()),#mrs
    path('forgot_password' , views.SendEmailForgotPassword),#mrs
    path('change_password' , views.changepassword),#mrs
    # path(r'^auth/users/activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$', views.UserActivationView.as_view()),
   
]