import string

from django.db import models
from django.utils.text import slugify
from random import SystemRandom


# Create your models here.
class TAG(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    # # HERE WE HAVE THE RELATION GENERIC
    # #  means that will be used in any places, don't link with project..
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # CASCADE WILL DELETE THIS LINE IF THE
    # # MAIN OBJ WAS DELETED
    #
    # object_id = models.CharField(max_length=255)  # this will receive id from id_obj that will be using with.
    #
    # content_object = GenericForeignKey("content_type", "object_id")  # Mixing content with TAG

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.name}-'.join(SystemRandom().choices(string.ascii_letters + string.digits, k=5)))
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
