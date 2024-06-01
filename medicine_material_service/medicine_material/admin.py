from django.contrib import admin

from .models import MedicineCategory, MedicineSupplier, Medicine, MaterialType, MaterialSupplier, Material
admin.site.register(MedicineCategory)
admin.site.register(MedicineSupplier)
admin.site.register(Medicine)
admin.site.register(MaterialType)
admin.site.register(MaterialSupplier)
admin.site.register(Material)
