from django.shortcuts import render, redirect
from .models import Folder, OCRImage
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
import PIL.Image
import os
import cv2
import pytesseract

@api_view(['GET'])
def user_logout(request):
    logout(request)  # Log the user out
    return JsonResponse({"success": True})


def download_image_as_pdf(request, image_id):
    my_model_instance = OCRImage.objects.get(id=image_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="mypdf.pdf"'

    c = canvas.Canvas(response, pagesize=landscape(letter))
    
    # Calculate image dimensions and position to center it on the page
    image_path = my_model_instance.image.path
    img = PIL.Image.open(image_path)
    img_width, img_height = img.size
    page_width, page_height = landscape(letter)
    
    # Calculate the scaling factor to fit the image within the page
    scale_factor = min(page_width / img_width, page_height / img_height)
    img_width *= scale_factor
    img_height *= scale_factor
    
    x = (page_width - img_width) / 2
    y = (page_height - img_height) / 2

    # Draw the image on the page
    c.drawImage(image_path, x, y, width=img_width, height=img_height)

    c.showPage()
    c.save()
    return response

# Define the signup view
@csrf_protect
@api_view(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return render(request, 'app/signup.html', {'error': 'Username already exists'})

        # Create a new user
        user = User.objects.create_user(username=username, password=password)

        # Log the user in
        login(request, user)

        return redirect('upload_folder')  # Redirect to the folder list page upon successful signup

    return render(request, 'app/signup.html')

# Define the login view
@csrf_protect
@api_view(['GET', 'POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('upload_folder')  # Redirect to the folder list page upon successful login

    return render(request, 'app/login.html')



@login_required
def upload_folder(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        images = request.FILES.getlist('images')
        user = request.user  # Get the logged-in user

        # Create a new folder associated with the user
        folder = Folder.objects.create(name=name, user=user)

        # Create Image instances associated with the folder and user
        for image in images:
            Image.objects.create(folder=folder, image=image, user=user)

        return redirect('folder_list')

    return render(request, 'app/upload_folder.html')



def folder_list(request):
    folders = Folder.objects.filter(user=request.user)
    return render(request, 'app/folder_list.html', {'folders': folders})

from os.path import basename

def view_folder(request, folder_id):
    folder = Folder.objects.get(pk=folder_id)
    
    # Extract image names from image paths
    image_names = [basename(image.image.name).split('.')[0] for image in folder.image_set.all()]
    
    context = {
        'folder': folder,
        'image_names': image_names,
    }

    print(image_names)

    return render(request, 'app/view_folder.html', context)


from django.core.exceptions import ObjectDoesNotExist



def perform_ocr_with_opencv(image_path):
    try:
        # Specify the path to the Tesseract executable here
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        
        image = cv2.imread(image_path)
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text
    except Exception as e:
        raise e
    


from django.shortcuts import get_object_or_404
from .models import Folder, Image


from django.http import JsonResponse

def perform_ocr_check(request, folder_id):
    try:
        # Retrieve the folder based on the folder_id
        folder = get_object_or_404(Folder, pk=folder_id)

        # Query the database to get all images related to this folder
        images = Image.objects.filter(folder=folder)

        # Initialize a list to store OCR results
        ocr_images = []

        # Process each image and perform OCR
        for image in images:
            
            extracted_text = perform_ocr_with_opencv(image.image.path)
            print(extracted_text)
            if extracted_text:
                ocr_images.append({
                    'image_url': image.image.path,  # Assuming MEDIA_URL is configured correctly
                    'image_file': os.path.join(settings.MEDIA_URL, folder.name, image.image.name ),  # Assuming MEDIA_URL is configured correctly
                    'ocr_text': extracted_text
                })

        print(ocr_images)
        return JsonResponse({'ocr_images': ocr_images})
     

    except Folder.DoesNotExist:
        # Handle the case where the folder with the specified ID does not exist
        return HttpResponse("Folder not found", status=404)


def view_ocr_images(request, folder_id):
    folder = get_object_or_404(Folder, pk=folder_id)
    ocr_images = OCRImage.objects.filter(folder=folder)

    context = {
        'folder': folder,
        'ocr_images': ocr_images,
    }

    return render(request, 'app/view_ocr_images.html', context)


def save_ocr_images(request, folder_id):
    folder = get_object_or_404(Folder, pk=folder_id)

    try:
        # Check if OCR images already exist for this folder
        existing_ocr_images = OCRImage.objects.filter(folder=folder)
        
        # Initialize a list to store OCR results
        ocr_images = []

        # If OCR images exist, include them in the response
        if existing_ocr_images.exists():
            for existing_ocr_image in existing_ocr_images:
                ocr_images.append({
                    'image_url': existing_ocr_image.image.url,
                    'ocr_text': existing_ocr_image.ocr_text,
                })
        else:
            # Query the database to get all images related to this folder
            images = Image.objects.filter(folder=folder)

            # Process each image and perform OCR
            for image in images:
                extracted_text = perform_ocr_with_opencv(image.image.path)
                if extracted_text:
                    # Create an OCRImage instance and save it to the model
                    ocr_image_instance = OCRImage(
                        folder=folder,
                        image=image.image,
                        ocr_text=extracted_text,
                    )
                    ocr_image_instance.save()
                    ocr_images.append({
                        'image_url': ocr_image_instance.image.url,
                        'ocr_text': extracted_text,
                    })

        return JsonResponse({'success': True, 'ocr_images': ocr_images})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})