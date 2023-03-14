from django.contrib.auth import get_user_model
from django.dispatch import receiver as listener
from django.db.models.signals import post_save

from authors.models import Profile

User = get_user_model()


# I USER @RECEIVE as @LISTENER BECAUSE MAKE MORE SENSE SINCE IT WILL LISTEN WHEN AN AUTHOR WILL BE SAVED
@listener(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    # print(f"signals: usuario na instancia: {instance.username}")
    if created:
        profile = Profile.objects.create(author=instance)
        profile.save()
