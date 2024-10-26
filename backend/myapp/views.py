from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from .models import *
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json

def trailers_list(request):
    """Render the trailers list view"""
    trailers = Trailer.objects.all()
    return render(request, 'trailers.html', {'trailers': trailers})

def add_trailer(request):
    """Handle AJAX requests to add a new trailer"""
    if request.method == 'POST':
        rego_number = request.POST.get('rego_number', '').strip()
        if rego_number:
            trailer, created = Trailer.objects.get_or_create(rego_number=rego_number)
            print("already exit",trailer,created)
            if created:
                return JsonResponse({'status': 'success', 'rego_number': trailer.rego_number})
            else:
                return JsonResponse({'status': 'exists', 'message': 'Trailer already exists.'})
        return JsonResponse({'status': 'error', 'message': 'Invalid trailer registration number.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
# views.py

def vehicle_list(request):
    """Render the vehicles list view"""
    vehicles = Vehicle.objects.all()  # Changed from 'vehicle' to 'vehicles' for clarity
    return render(request, 'vehicles.html', {'vehicle': vehicles})  # Keep the context variable the same
def add_vehicle(request):
    """Handle AJAX requests to add a new vehicle"""
    if request.method == 'POST':
        rego_number = request.POST.get('rego_number', '').strip()
        if rego_number:
            vehicle, created = Vehicle.objects.get_or_create(rego_number=rego_number)
            print("vehicle:", vehicle, "created:", created)
            if created:
                return JsonResponse({'status': 'success', 'rego_number': vehicle.rego_number})
            else:
                return JsonResponse({'status': 'exists', 'message': 'Vehicle already exists.'})
        return JsonResponse({'status': 'error', 'message': 'Invalid vehicle registration number.'})
    
    # Ensure this part of the code is unreachable unless an incorrect method is used
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def drivers_list(request):
    """Render the drivers list view."""
    drivers = Driver.objects.all()
    return render(request, 'drivers.html', {'drivers': drivers})

def add_driver(request):
    """Handle AJAX requests to add a new driver."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        on_leave = request.POST.get('on_leave') == 'true'
        has_msic = request.POST.get('has_msic') == 'true'
        has_white_card = request.POST.get('has_white_card') == 'true'

        if name and phone_number:
            # Check if a driver with the same name and phone number already exists
            if not Driver.objects.filter(name=name, phone_number=phone_number).exists():
                driver = Driver.objects.create(
                    name=name,
                    phone_number=phone_number,
                    on_leave=on_leave,
                    has_msic=has_msic,
                    has_white_card=has_white_card
                )
                return JsonResponse({
                    'status': 'success',
                    'name': driver.name,
                    'phone_number': driver.phone_number,
                    'on_leave': driver.on_leave,
                    'has_msic': driver.has_msic,
                    'has_white_card': driver.has_white_card
                })
            else:
                return JsonResponse({'status': 'exists', 'message': 'Driver with this name and phone number already exists.'})
        return JsonResponse({'status': 'error', 'message': 'Please Enter the Phone number and Name.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})



def delete_driver(request, id):
    if request.method == 'DELETE':
        try:
            driver = Driver.objects.get(id=id)
            driver.delete()
            return JsonResponse({'status': 'success'})
        except Driver.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Driver not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
from django.views.decorators.http import require_http_methods

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["POST"])
def edit_driver(request, id):
    try:
        driver = Driver.objects.get(id=id)
        driver.name = request.POST.get('name')
        driver.phone_number = request.POST.get('phone_number')
        driver.on_leave = request.POST.get('on_leave') == 'true'
        driver.has_msic = request.POST.get('has_msic') == 'true'
        driver.has_white_card = request.POST.get('has_white_card') == 'true'

        # Check if another driver (not this one) exists with the same name and phone number
        if Driver.objects.filter(name=driver.name, phone_number=driver.phone_number).exclude(id=driver.id).exists():
            return JsonResponse({'status': 'exists', 'message': 'Driver with this name and phone number already exists.'})
        else:
            driver.save()
            return JsonResponse({'status': 'success'})
    except Driver.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Driver not found'}, status=404)


def jobs_list(request):
    """Render the jobs list view."""
    jobs = Job.objects.all()  # Use plural to match the template
    print(jobs)
    vehicles = Vehicle.objects.all()
    trailers = Trailer.objects.all()
    drivers = Driver.objects.all()
    drivers_list = [{'id': driver.id, 'name': driver.name, 'has_msic': driver.has_msic, 'has_whitecard': driver.has_white_card} for driver in drivers]


    rosters = Roster.objects.all()

    return render(request, 'job.html', {'jobs': jobs,'vehicles':vehicles,'trailers':trailers,'drivers':drivers_list,'rosters':rosters})  # Change 'job' to 'jobs'

def add_job(request):
    """Handle AJAX requests to add a new job."""
    if request.method == 'POST':
        job_name = request.POST.get('job_name', '').strip()
        job_count = request.POST.get('job_count', '').strip()
        job_date = request.POST.get('job_date', '')
        trailer_type = request.POST.get('trailer_type', '')

        if job_name and job_count and job_date and trailer_type:
            try:
                # Convert job_daate string to a datetime object
                job_date = datetime.strptime(job_date, '%Y-%m-%d')  # Adjust format as necessary

                job = Job.objects.create(
                    job_name=job_name,
                    job_count=job_count,
                    job_date=job_date,
                    trailer_type=trailer_type
                )
                return JsonResponse({'status': 'success', 'job': {
                    'id': job.id,
                    'job_name': job.job_name,
                    'job_count': job.job_count,
                    'job_date': job.job_date.isoformat(),
                    'trailer_type': job.trailer_type
                }})
            except ValueError:
                return JsonResponse({'status': 'error', 'message': 'Invalid date format. Please use YYYY-MM-DD.'})
        
        return JsonResponse({'status': 'error', 'message': 'Please fill in all fields.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def delete_job(request, id):
    """Handle AJAX requests to delete a job."""
    if request.method == 'DELETE':
        try:
            job = Job.objects.get(id=id)
            job.delete()
            return JsonResponse({'status': 'success'})
        except Job.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Job not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def edit_job(request, id):
    if request.method == 'POST':
        job = get_object_or_404(Job, id=id)

        job_name = request.POST.get('job_name')
        job_count = request.POST.get('job_count')
        job_date = request.POST.get('job_date')
        trailer_type = request.POST.get('trailer_type')

        # Validate input values
        if not job_name or not job_count or not trailer_type:
            return JsonResponse({'status': 'error', 'message': 'Please provide all fields.'}, status=400)

        # Validate job_date
        try:
            job_date = datetime.strptime(job_date, "%Y-%m-%d").date()
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid date format. Please use YYYY-MM-DD.'}, status=400)

        # Update job fields
        job.job_name = job_name
        job.job_count = job_count
        job.job_date = job_date
        job.trailer_type = trailer_type

        # Save the job
        job.save()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@csrf_exempt  # Use cautiously, consider proper CSRF protection
def add_roster(request):



    
    if request.method == 'POST':
        data = json.loads(request.body)
        print("aa--ffffffff", data)
        try:
            # Parse the date from the incoming data
            job_date = datetime.strptime(data['date'], '%b. %d, %Y').date()
            
            # Validate and parse start_time
            start_time_str = data.get('startTime')
            end_time_str = data.get('finishTime')

            if not start_time_str or not end_time_str:
                return JsonResponse({'status': 'error', 'message': 'startTime and finishTime cannot be empty.'})

            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()

            # Create a new Roster instance
            print("aaa-----------")
            print("data['wharfStatus']",data['wharfStatus'])
            print("data['constructionSite']",data['constructionSite'])

            vehicles = Vehicle.objects.get(id=data['vehicleRegos'])
            trailer1 = Trailer.objects.get(id=data['trailerRegos'][0])
            print("trailer1",trailer1)
            # print("Trailer.objects.get(id=data['trailerRegos'][1])",Trailer.objects.get(id=data['trailerRegos'][1]))
            if data['trailerRegos'][1] == '':
                trailer2 = None
                print("trailer2",trailer2)
            else:
                print("hello1")
                trailer2=Trailer.objects.get(id=data['trailerRegos'][1])

            if data['trailerRegos'][2] == '':
                trailer3 = None
                print("trailer2",trailer3)    
            else:
                print("hello1")
                trailer3=Trailer.objects.get(id=data['trailerRegos'][2])
       
            driver = Driver.objects.get(id=data['driverName'])
            roster = Roster.objects.create(
                job_date=job_date,
                vehicle=vehicles,
                trailer1=trailer1,
                trailer2=trailer2,
                trailer3=trailer3,
                trailer_type=data['trailerType'],
                start_time=start_time,
                end_time=end_time,
                client_name=data['clientName'],
                wharf_status=data['wharfStatus'],
                construction_site=data['constructionSite'],
                driver=driver,
                notes=data['notes']
            )
            roster.save()
            return JsonResponse({'status': 'success', 'message': 'Roster added successfully!'})
        except ValueError as ve:
            return JsonResponse({'status': 'error', 'message': str(ve)})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
# views.py
from django.http import JsonResponse
from .models import Driver

from django.http import JsonResponse
from .models import Driver  # Make sure to import your Driver model

def get_filtered_drivers(request):
    if request.method == "GET":
        # Retrieve query parameters
        wharfStatus = request.GET.get('wharfStatus')
        constructionSite = request.GET.get('constructionSite')

        # Convert query parameters to Boolean values
        wharfStatus = wharfStatus.lower() == 'true' if wharfStatus is not None else False
        constructionSite = constructionSite.lower() == 'true' if constructionSite is not None else False

        # Print for debugging
        print(f"Wharf Status: {wharfStatus}, Construction Site: {constructionSite}")
        if not wharfStatus and not constructionSite:
            # Fetch drivers excluding those with both has_msic and has_white_card set to False
            filtered_drivers = Driver.objects.exclude(has_msic=False, has_white_card=False)
        # Filter drivers based on the received parameters
        else:
            filtered_drivers = Driver.objects.filter(has_msic=wharfStatus, has_white_card=constructionSite)

        # Prepare driver data for the response
        driver_data = [{'id': driver.id, 'name': driver.name} for driver in filtered_drivers]

        return JsonResponse(driver_data, safe=False)


import csv
from django.http import HttpResponse
from .models import Roster

def export_roster_csv(request):
    # Create the HTTP response object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rosters.csv"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write the header row
    writer.writerow([
        'Job Date', 'Vehicle Rego Number', 'Driver Name', 
        'Trailer1 Rego Number', 'Trailer2 Rego Number', 'Trailer3 Rego Number', 
        'Trailer Type', 'Start Time', 'End Time', 
        'Client Name', 'Wharf Status', 'Construction Site', 'Notes'
    ])

    # Fetch all Roster objects and write to the CSV
    rosters = Roster.objects.all()
    for roster in rosters:
        writer.writerow([
            roster.job_date.strftime('%Y-%m-%d') if roster.job_date else '',
            roster.vehicle.rego_number if roster.vehicle else '',
            roster.driver.name if roster.driver else '',
            roster.trailer1.rego_number if roster.trailer1 else '',
            roster.trailer2.rego_number if roster.trailer2 else '',
            roster.trailer3.rego_number if roster.trailer3 else '',
            roster.trailer_type,
            roster.start_time.strftime('%H:%M') if roster.start_time else '',
            roster.end_time.strftime('%H:%M') if roster.end_time else '',
            roster.client_name,
            roster.wharf_status,
            roster.construction_site,
            roster.notes,
        ])

    return response
