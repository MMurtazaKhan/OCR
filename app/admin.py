from django.contrib import admin
from .models import Folder, Image, OCRImage, PDF

# Register your models here.

admin.site.register(Folder)
admin.site.register(Image)
admin.site.register(OCRImage)
admin.site.register(PDF)
