from datetime import timedelta
from uuid import uuid4

from celery import shared_task
from django.utils.timezone import now

from users.models import EmailVerification, User


@shared_task
def celery_email_verification(user_id):
    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(hours=1)
    record = EmailVerification.objects.create(code=uuid4(), user=user, expiration=expiration)
    record.send_email_verification()
