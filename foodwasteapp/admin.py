from django.contrib import admin
from .models import FoodEntry,Profile,completed
# Register your models here.
admin.site.register(FoodEntry)
admin.site.register(completed)
admin.site.register(Profile)





