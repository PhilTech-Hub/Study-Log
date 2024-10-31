from django.contrib import admin
from .models import Profile
# Register your models here.
from .models import Topic, Entry

admin.site.register(Topic)
admin.site.register(Entry)
admin.site.register(Profile)
