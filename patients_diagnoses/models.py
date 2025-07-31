# models.py ///patients/01_Modelo_y_Recursos/patient.php :
from django.db import models
from django.utils import timezone
# Create your models here.

class Patient(models.Model):
    document_number = models.CharField(max_length=20, unique=True)
    paternal_lastname = models.CharField(max_length=100)
    maternal_lastname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    personal_reference = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField()
    sex = models.CharField(max_length=10)
    primary_phone = models.CharField(max_length=15)
    secondary_phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    ocupation = models.CharField(max_length=100, blank=True, null=True)
    health_condition = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # Relaciones foráneas
    region = models.ForeignKey('Region', on_delete=models.SET_NULL, null=True)
    province = models.ForeignKey('Province', on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey('District', on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True)
    document_type = models.ForeignKey('DocumentType', on_delete=models.SET_NULL, null=True)

    # Soft delete
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.paternal_lastname} {self.maternal_lastname}, {self.name}"
