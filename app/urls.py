from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('upload/', views.upload_folder, name='upload_folder'),
    path('folders/', views.folder_list, name='folder_list'),
    path('folders/<int:folder_id>/', views.view_folder, name='view_folder'),
    path('folders/<int:folder_id>/ocr_check/', views.perform_ocr_check, name='perform_ocr_check'),  
    path('folders/<int:folder_id>/save_ocr_images/', views.save_ocr_images, name='save_ocr_images'),  
    path('folders/<int:folder_id>/view_ocr_images/', views.view_ocr_images, name='view_ocr_images'),
    path('generate_pdf/<str:image_id>/', views.download_image_as_pdf, name='generate_pdf'),

]
