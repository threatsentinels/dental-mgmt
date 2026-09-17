from django.contrib import admin
from .models import ToothRecord, TreatmentPlan, TreatmentItem


@admin.register(ToothRecord)
class ToothRecordAdmin(admin.ModelAdmin):
    list_display = ("patient", "tooth_number", "condition", "surface", "updated_at")
    list_filter = ("condition", "clinic")
    search_fields = ("patient__first_name", "patient__last_name", "tooth_number")


class TreatmentItemInline(admin.TabularInline):
    model = TreatmentItem
    extra = 1


@admin.register(TreatmentPlan)
class TreatmentPlanAdmin(admin.ModelAdmin):
    list_display = ("title", "patient", "doctor", "status", "total_cost", "created_at")
    list_filter = ("status", "clinic")
    search_fields = ("title", "patient__first_name", "patient__last_name")
    inlines = [TreatmentItemInline]