import uuid
from django.db import models

# Create your models here.

class Clinic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['name']

    def __str__(self):
        return self.name 


class Branch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    clinic = models.ForeignKey(Clinic,on_delete=models.CASCADE,related_name='branches')
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=50,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Branches"
        ordering = ['name']

    def __str__(self):
        return f"{self.clinic.name} - {self.name}"



class TenantManager(models.Manager):
    def for_clinic(self,clinic):
        return self.get_queryset().filter(clinic=clinic, is_deleted=False)

class TenantAwareModel(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, db_index=True)
    is_deleted = models.BooleanField(default=False,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TenantManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True 


