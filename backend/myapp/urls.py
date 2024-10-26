from django.urls import path
# from . import views
from .views import *
urlpatterns = [
    path('', trailers_list, name='trailers_list'),
    path('add_trailer/', add_trailer, name='add_trailer'),
    path('add_vehicle/', add_vehicle, name='add_vehicle'),  # Ensure this is correctly set up
    path('list_vehicle/', vehicle_list, name='add_vehicle'),  # Ensure this is correctly set up
    path('drivers/', drivers_list, name='drivers_list'),
    path('add_driver/', add_driver, name='add_driver'),
    path('delete_driver/<int:id>/', delete_driver, name='delete_driver'),
    path('edit_driver/<int:id>/', edit_driver, name='edit_driver'),
    path('jobs/', jobs_list, name='jobs_list'),
    path('jobs_add/', add_job, name='add_job'),
    path('jobs/delete/<int:id>/', delete_job, name='delete_job'),
    path('jobs/edit/<int:id>/', edit_job, name='edit_job'),
    path('roster/add/', add_roster, name='add_roster'),
    path('api/get_filtered_drivers', get_filtered_drivers, name='get_filtered_drivers'),
    path('export/roster/', export_roster_csv, name='export_roster_csv'),

]
