from django.contrib import admin
from .models import Cities, Apartment, Comment, Reply
# Register your models here.


admin.site.register(Cities)
admin.site.register(Apartment)
admin.site.register(Comment)
admin.site.register(Reply)
