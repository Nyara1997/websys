from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from .models import Cost_Of_Production

@receiver(pre_save, sender=Cost_Of_Production)
def generate_serial_number(sender, instance, **kwargs):
	if not instance.serial_number:
		instance.serial_number = f'TR-{get_random_string(length=8)}'
