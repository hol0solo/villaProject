from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_verified = models.BooleanField(default=False)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    expiration = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'EmailVerification for {self.user.username}'

    def send_email_verification(self):
        link = f'users/verify/{self.user.email}/{self.code}'
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        send_mail(
            subject=f"Email Verification for {self.user.username}",
            message=f"Mr or Mrs {self.user.first_name} {self.user.last_name} confirm your email in Holosolo shop "
                    f"by clicking on this link {verification_link}",
            from_email="from@example.com",
            recipient_list=[f'{self.user.email}'],
            fail_silently=False,
        )
