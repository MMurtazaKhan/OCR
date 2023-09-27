from django.contrib import admin
from .models import Folder, Image, OCRImage

# Register your models here.

admin.site.register(Folder)
admin.site.register(Image)
admin.site.register(OCRImage)
