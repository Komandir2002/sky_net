from django.contrib import admin
from .models import Status,Applications,ApplicationRating
# Register your models here.


admin.site.register(Status)
admin.site.register(Applications)
admin.site.register(ApplicationRating)