from django.contrib import admin

# Register your models here.
from .models import Contactinfo, Category,Course,Instructor

admin.site.register(Contactinfo)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Instructor)