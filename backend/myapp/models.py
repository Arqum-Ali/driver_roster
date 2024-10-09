from django.db import models

class Vehicle(models.Model):
    rego_number = models.CharField(max_length=20, null=True, blank=True, default='default_value')  # Vehicle Registration

    def __str__(self):
        return self.rego_number

class Driver(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, default='default_value')
    on_leave = models.BooleanField(default=False)
    has_msic = models.BooleanField(default=False)  # MSIC - Maritime Security ID
    has_white_card = models.BooleanField(default=False)  # White card for construction
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Trailer(models.Model):
    rego_number = models.CharField(max_length=10, unique=True, null=True, blank=True, default='default_value')

    def __str__(self):
        return self.rego_number

class Job(models.Model):
    job_name = models.CharField(max_length=255)
    job_count = models.PositiveIntegerField()
    job_date = models.DateField()
    trailer_type = models.CharField(max_length=4, choices=[
        ('S', 'S'),
        ('SDL', 'SDL'),
        ('RT', 'RT'),
        ('BDBL', 'BDBL'),
    ])

    def __str__(self):
        return self.job_name
from django.db import models
from django.db import models

class Roster(models.Model):
    job_date = models.DateField()
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, blank=True)  # Remove default
    trailer1 = models.ForeignKey(Trailer, related_name='trailer1', on_delete=models.CASCADE, null=True, blank=True)  # Remove default
    trailer2 = models.ForeignKey(Trailer, related_name='trailer2', on_delete=models.CASCADE, null=True, blank=True)  # Remove default
    trailer3 = models.ForeignKey(Trailer, related_name='trailer3', on_delete=models.CASCADE, null=True, blank=True)  # Remove default
    trailer_type = models.CharField(max_length=50, default="")  # Use empty string as default
    start_time = models.TimeField(null=True, blank=True)  # Use null or blank for optional
    end_time = models.TimeField(null=True, blank=True)  # Use null or blank for optional
    client_name = models.CharField(max_length=100, default="")  # Use empty string as default
    wharf_status = models.CharField(max_length=20, default="")  # Use empty string as default
    construction_site = models.CharField(max_length=100, default="")  # Use empty string as default
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)  # Remove default
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.job_date} - {self.client_name} - {self.vehicle.rego_number}"
