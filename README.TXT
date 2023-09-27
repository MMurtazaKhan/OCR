-----------------------Requirements----------------------------

asgiref==3.7.2
Django==4.2.5
django-rest-framework==0.1.0
djangorestframework==3.14.0
numpy==1.26.0
opencv-python==4.8.0.76
packaging==23.1
Pillow==10.0.1
pytesseract==0.3.10
pytz==2023.3.post1
sqlparse==0.4.4
tesseract==0.1.3
typing-extensions==4.8.0
tzdata==2023.3

-----------------------Install pytesseract---------------------------

Download link: https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.1.20230401.exe

Download Path should be: C:\\Program Files\\Tesseract-OCR\\tesseract.exe

Add path in your environment variables: C:\Program Files\Tesseract-OCR

--------------------- Activate the Virtual Environment --------------------

Add Virtual Env: python -m venv env

Activate Virtua Env: env\Scripts\Activate

Install all dependencies provided under requirements after activating env

Run Server: python manage.py runserver

---------------------URLS-----------------------------

Upload folder: http://127.0.0.1:8000/image-gallery/upload/

View folders and Check OCR: http://127.0.0.1:8000/image-gallery/folders/