from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User
import os

# Create your models here.
class Cities(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(max_length=500,blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

def save_subject_image(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.subject_id:
        filename = 'Subject_Pictures/{}.{}'.format(instance.subject_id, ext)
    return os.path.join(upload_to, filename)




def save_apartment_files(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.apartment_id:
        filename = 'apartment_files/{}/{}.{}'.format(instance.apartment_id,instance.apartment_id, ext)
        if os.path.exists(filename):
            new_name = str(instance.lesson_id) + str('1')
            filename =  'apartment_images/{}/{}.{}'.format(instance.apartment_id,new_name, ext)
    return os.path.join(upload_to, filename)

class Apartment(models.Model):
    apartment_id = models.CharField(max_length=100, unique=True)
    Cities = models.ForeignKey(Cities, on_delete=models.CASCADE, related_name='apartments')
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=250)
    desc = models.TextField()
    price = models.IntegerField(max_length=250)
    slug = models.SlugField(null=True, blank=True)
    pic1 = models.ImageField(upload_to='Images/')
    pic2 = models.ImageField(upload_to='Images/')
    pic3 = models.ImageField(upload_to='Images/')
    pic4 = models.ImageField(upload_to='Images/')

    class Meta:
        ordering = ['apartment_id']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('onlinerental:lesson_list', kwargs={ 'cities':self.Cities.slug})

class Comment(models.Model):
    apartment_name = models.ForeignKey(Apartment,null=True, on_delete=models.CASCADE,related_name='comments')
    comm_name = models.CharField(max_length=100, blank=True)
    # reply = models.ForeignKey("Comment", null=True, blank=True, on_delete=models.CASCADE,related_name='replies')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.comm_name = slugify("comment by" + "-" + str(self.author) + str(self.date_added))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.comm_name

    class Meta:
        ordering = ['-date_added']

class Reply(models.Model):
    comment_name = models.ForeignKey(Comment, on_delete=models.CASCADE,related_name='replies')
    reply_body = models.TextField(max_length=500)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "reply to " + str(self.comment_name.comm_name)
