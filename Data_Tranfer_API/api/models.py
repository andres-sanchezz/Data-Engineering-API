from django.db import models

class Departments(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    department = models.CharField(max_length=50)

class Jobs(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    job = models.CharField(max_length=50)

class Hired_Employee(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    department_id = models.ForeignKey(Departments, on_delete=models.CASCADE)
    job_id = models.ForeignKey(Jobs, on_delete=models.CASCADE)