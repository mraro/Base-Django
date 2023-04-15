from utility.image_utils import *

from django.dispatch import receiver as listener
from django.db.models.signals import pre_delete, pre_save

from farmacia.models import Remedios

""" 
SIGNALS IS SUPER UTIL, HERE WE CAN CHANGE SOME DATA BEFORE OR AFTER SAVES
IN THIS CASE I'M REMOVING IMAGES THAT WON'T BE USED

https://docs.djangoproject.com/en/4.1/ref/signals/
"""


# I USER @RECEIVE as @LISTENER BECAUSE MAKE MORE SENSE SINCE IT WILL LISTEN WHEN AN AUTHOR WILL BE SAVED
@listener(pre_delete, sender=Remedios)
def delete_cover(sender, instance, *args, **kwargs):  # this deletes image if it has no cover
    # print(f"signals: instancia: {instance, sender}")  # LOG
    instance_to_delete = Remedios.objects.filter(pk=instance.pk).first()
    delete_cover_file(instance_to_delete)


@listener(pre_save, sender=Remedios)
def update_cover_file_delete_old(sender, instance, *args, **kwargs):  # this deletes on change image
    instance_to_delete = Remedios.objects.filter(pk=instance.pk).first()
    # check ifs should delete properly, avoid delete wrong
    if instance.cover and instance.cover != "static/images/default.jpg":
        new_instance = instance.cover
        print(f"signals: new instance: {instance.cover}")  # LOG
        if instance_to_delete:
            if instance_to_delete.cover != new_instance:
                delete_cover_file(instance_to_delete)
                print('instance deleted: ', instance_to_delete)


