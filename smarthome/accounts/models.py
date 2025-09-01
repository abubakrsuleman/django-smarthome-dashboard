from django.db import models
from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
class account(AbstractUser):
    middle_name = models.CharField(max_length=100, blank=True)
    class Gender(models.IntegerChoices):
        DEFAULT = 0
        Male = 1
        Female = 2
        Other = 9
    gender = models.IntegerField(default=0,choices=Gender.choices)
    date_of_birth = models.DateField(null=True)
    #user_pfp = models.ImageField(default='default_assets/default.jpg', upload_to='profile_pictures')
    mobile_number = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')],blank=True)
    recovery_email = models.EmailField(unique=True,null=True)
    def __str__(self): return f'User: {self.first_name} {self.last_name}'
'''
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.user_pfp.path)

        if img.height > 1080 or img.width > 1920:
            output_size = (1920,1080)
            img.thumbnail(output_size)
            img.save(self.pfp_image_account.path)
'''
