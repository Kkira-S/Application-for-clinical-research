from django.core.validators import MinValueValidator
from django.db import models


class Measurements(models.Model):
    measurement_id = models.AutoField(primary_key=True)  # Теперь ID создаётся автоматически
    patient = models.ForeignKey('Patients', models.DO_NOTHING, blank=True, null=True)
    trial = models.ForeignKey('Trials', models.DO_NOTHING, blank=True, null=True)
    drug = models.CharField(max_length=100)
    condition_score = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'measurements'


class Patients(models.Model):
    patient_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    condition = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'patients'


class Trials(models.Model):
    trial_id = models.IntegerField(
        validators=[MinValueValidator(0)], primary_key=True)
    trial_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    med = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trials'
