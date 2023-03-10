import os

from django.dispatch import receiver as listener
from django.db.models.signals import pre_delete, pre_save

from farmacia.models import Remedios

""" 
SIGNALS IS SUPER UTIL, HERE WE CAN CHANGE SOME DATA BEFORE OR AFTER SAVES
IN THIS CASE I'M REMOVING IMAGES THAT WON'T BE USED
"""


def delete_cover_file(instance):
    if instance.cover != "static/images/default.jpg":
        try:
            print(f'apagado: {instance.cover.path}')  # LOG
            os.remove(instance.cover.path)
        except (ValueError, FileNotFoundError) as e:  # LOG
            print(f'Erro ao apagar: {e}')


# I USER @RECEIVE as @LISTENER BECAUSE MAKE MORE SENSE SINCE IT WILL LISTEN WHEN AN AUTHOR WILL BE SAVED
@listener(pre_delete, sender=Remedios)
def delete_cover(sender, instance, *args, **kwargs):
    # print(f"signals: instancia: {instance, sender}")  # LOG
    instance_to_delete = Remedios.objects.filter(pk=instance.pk).first()
    delete_cover_file(instance_to_delete)


@listener(pre_save, sender=Remedios)
def update_cover_file_delete_old(sender, instance, *args, **kwargs):
    print(f"signals: instancia: {instance.cover}")  # LOG
    instance_to_delete = Remedios.objects.filter(pk=instance.pk).first()
    if instance.cover:
        new_instance = instance.cover
        if instance_to_delete:
            if instance_to_delete.cover != new_instance:
                delete_cover_file(instance_to_delete)
