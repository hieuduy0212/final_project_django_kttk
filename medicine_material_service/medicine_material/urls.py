from django.urls import path
from .views import (
    MedicineSupplierCreateView,
    MedicineCategoryCreateView,
    MedicineListView,
    MedicineDetailView,
    MedicineCreateView,
    MedicineUpdateView,
    MedicineDeleteView,
    MaterialListView,
    MaterialDetailView,
    MaterialCreateView,
    MaterialUpdateView,
    MaterialDeleteView
)

urlpatterns = [
    # Medicine Supplier URLs
    path('medicine-suppliers/', MedicineSupplierCreateView.as_view(), name='medicine_supplier_create'),

    # Medicine Category URLs
    path('medicine-categories/', MedicineCategoryCreateView.as_view(), name='medicine_category_create'),

    # Medicine URLs
    path('medicines/', MedicineListView.as_view(), name='medicine_list'),
    path('medicines/<int:medicine_id>/', MedicineDetailView.as_view(), name='medicine_detail'),
    path('medicines/create/', MedicineCreateView.as_view(), name='medicine_create'),
    path('medicines/<int:medicine_id>/update/', MedicineUpdateView.as_view(), name='medicine_update'),
    path('medicines/<int:medicine_id>/delete/', MedicineDeleteView.as_view(), name='medicine_delete'),

    # Material URLs
    path('materials/', MaterialListView.as_view(), name='material_list'),
    path('materials/<int:material_id>/', MaterialDetailView.as_view(), name='material_detail'),
    path('materials/create/', MaterialCreateView.as_view(), name='material_create'),
    path('materials/<int:material_id>/update/', MaterialUpdateView.as_view(), name='material_update'),
    path('materials/<int:material_id>/delete/', MaterialDeleteView.as_view(), name='material_delete'),
]
