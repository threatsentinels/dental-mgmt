from django import forms
from .models import PatientImaging

class PatientImagingForm(forms.ModelForm):
    class Meta:
        model = PatientImaging
        fields = ["imaging_type", "tooth_number", "title", "image_file", "taken_at", "notes"]
        widgets = {
            "taken_at": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-input"}),
            "notes": forms.Textarea(attrs={"rows": 3, "class": "form-input"}),
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "imaging_type": forms.Select(attrs={"class": "form-input"}),
            "tooth_number": forms.NumberInput(attrs={"class": "form-input", "placeholder": "e.g. 16"}),
            "image_file": forms.FileInput(attrs={"class": "form-input"}),
        }

    def clean_image_file(self):
        image = self.cleaned_data.get("image_file")
        if image:
            # Secure file type & extension validation
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                raise forms.ValidationError("Only JPEG, PNG, and WEBP image formats are permitted.")
            if image.size > 10 * 1024 * 1024:  # 10MB limit
                raise forms.ValidationError("Image file size must not exceed 10MB.")
        return image