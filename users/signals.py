from django.db.models.signals import post_save
from django.contrib.auth.models import User

from .models import Profile

# @receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    user = instance  # instance will be the sender which is the User in this case (line 55)
    if created == True:  # It will be true when the user is first created else it will be false
        Profile.objects.create(
            user=user,
            name=user.first_name,
            email=user.email,
            username=user.username
        )

def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

post_save.connect(createProfile, sender=User) # Creating user will create a profile
post_save.connect(updateUser, sender=Profile) # Updating profile will update user information in users table