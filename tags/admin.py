from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.TaggedItem)

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("text",),
    }