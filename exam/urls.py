from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('',views.home, name='home'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('question/<str:pk>/',views.questionView, name='question'),
    path('quest/<str:quiz>/<str:stud>/', views.nextquestion, name='quest'),
    

    path('createquiz/', views.createQuiz, name='createquiz'),
    path('createquestion/', views.createQuestion, name = 'createquestion'),
    path('createoptions/', views.createOptions, name='createoptions'),

    path('login/', views.logIn, name = 'login' ),
    path('register/', views.register, name ='register'),
    path('logout/', views.logOut, name='logout'),
]
