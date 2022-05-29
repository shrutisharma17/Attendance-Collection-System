from django.urls import path,include
from .views import *
# This is the list of urls used for various paths in our final implementation

urlpatterns = [
    path('', start, name= 'start'),
    path('home/',index, name = 'index'),
    path('ajax/', lastface, name= 'ajax'),
    path('scan/',scan,name='scan'),
    path('student_profile/', profiles, name= 'student_profile'),
    path('details/', details, name= 'details'),

    path('add_student/',add_student,name='add_student'),
    path('edit_student/<int:id>/',edit_student,name='edit_student'),
    path('delete_student/<int:id>/',delete_student,name='delete_student'),


    path('clear_history/',clear_history,name='clear_history'),
    path('reset/',reset,name='reset'),


]
