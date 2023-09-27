from django.shortcuts import render, redirect
from .models import Folder, OCRImage
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
import os
import cv2
import pytesseract

def upload_folder(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        images = request.FILES.getlist('images')
        folder = Folder.objects.create(name=name)
        for image in images:
            folder.image_set.create(image=image)
        return redirect('folder_list')
    return render(request, 'app/upload_folder.html')


def folder_list(request):
    folders = Folder.objects.all()
    return render(request, 'app/folder_list.html', {'folders': folders})


def view_folder(request, folder_id):
    folder = Folder.objects.get(pk=folder_id)
    return render(request, 'app/view_folder.html', {'folder': folder})


# views.py



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