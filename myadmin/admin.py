from django.contrib import admin
from .models import Client,Services,Company

admin.site.register(Client)
admin.site.register(Company)
admin.site.register(Services)
