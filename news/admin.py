from django.contrib import admin

#class Blog(models.Model):  #<---

from .models import New    #<---

class NewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_datetime', 'updated_datetime')
    list_display_links = ('id', 'title')

    
admin.site.register(New)
