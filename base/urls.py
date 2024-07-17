from django.urls import path
from .views import MedicineList, MedicineDetail, MedicineCreate, MedicineUpdate, MedicineDelete, CustomLoginView, RegisterPage, UserMedicineList
from django.contrib.auth.views import LogoutView

# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('', MedicineList.as_view(), name="medicines"),
    path('medicine/<int:pk>/', MedicineDetail.as_view(), name='medicine'),
    path('medicine-create/', MedicineCreate.as_view(), name='medicine-create'),
    path('medicine-update/<int:pk>/', MedicineUpdate.as_view(), name='medicine-update'),
    path('medicine-delete/<int:pk>/', MedicineDelete.as_view(), name='medicine-delete'),
    path('user/<int:user_id>/medicines/', UserMedicineList.as_view(), name='user-medicines'),  # User medicines path

]

