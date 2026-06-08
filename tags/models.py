from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class TaggedItem(models.Model):
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_id")

    def __str__(self):
        return f"{self.tag} | {self.content_object}"


class Tag(models.Model):
    text = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    items = models.ManyToManyField(ContentType, through=TaggedItem)

    def __str__(self):
        return self.text
