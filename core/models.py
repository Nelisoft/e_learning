from django.db import models
from autoslug import AutoSlugField
from django.utils.text import slugify
# Create your models here.


class Contactinfo(models.Model):
    address = models.CharField(max_length=255)
    phone_number =models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    content = models.TextField()
    gmap =models.URLField()
    
    def __str__(self):
        return f'Contact information'
    
    
class Category(models.Model):
    img = models.ImageField(upload_to='Category_img')
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    def get_all_category(self):
        return Category.objects.all().order_by('-id')
    
    
class Instructor(models.Model):
    img = models.ImageField(upload_to='instructors')
    name =models.CharField(max_length=100)
    fb= models.CharField(max_length=200)
    twt=models.CharField(max_length=200)
    ig = models.CharField(max_length=200)
    designation = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Course(models.Model):
    
    STATUS = (
        ('PUBLISH',"PUBLISH"),
        ('DRAFT','DRAFT')
    )
    featured_image = models.ImageField(upload_to='courses/featured_img')
    featured_video = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.IntegerField(null=True, default=0)
    discount = models.IntegerField(null=True)
    course_slug= AutoSlugField(populate_from='title',unique=True, default=None)
    status = models.CharField(choices=STATUS, max_length=100,null=True)
    created_at = models.DateField(auto_now_add=True)
    duration = models.CharField(max_length=100)
    tutor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    student =models.IntegerField()
    
    
    def __str__(self):
        return self.title
    
    
