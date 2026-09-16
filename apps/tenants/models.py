from django.db import models


class Clinic(models.Model):
    name = models.CharField(max_length=255)
    code = models.SlugField(max_length=50, unique=True, help_text="Unique short code/identifier for the clinic.")
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Branch(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="branches")
    name = models.CharField(max_length=255)
    code = models.SlugField(max_length=50, help_text="Unique short identifier within clinic.")
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["clinic", "name"]
        unique_together = [("clinic", "code")]

    def __str__(self):
        return f"{self.clinic.name} - {self.name}"