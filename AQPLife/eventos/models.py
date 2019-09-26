from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
	user 				= models.OneToOneField(User, on_delete=models.CASCADE)
	tipo_idenficacion	= models.CharField(max_length=30)
	identificacion		= models.IntegerField(default=0)
	permission_asistente= models.BooleanField(default=True)
	permission_administrador= models.BooleanField(default=False)
	permission_colaborador  = models.BooleanField(default=False)
	permission_ponente      = models.BooleanField(default=False)
	def __str__(self):
		return str(self.user.get_username())


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
    	Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()