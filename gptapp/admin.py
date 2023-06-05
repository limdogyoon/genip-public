from django.contrib import admin

# Register your models here.
#/project1/gptapp/admin.py

from gptapp.models import genip_db, freecount

class EasyViewAdmin(admin.ModelAdmin):
    list_display = ["username", "input", "timestamp"]
admin.site.register(genip_db, EasyViewAdmin)

admin.site.register(freecount)
