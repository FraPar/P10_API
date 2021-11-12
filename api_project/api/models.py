import uuid
from django.conf import settings
from django.db import models
from authenticate.models import User


class Projects(models.Model):
    # COMMENT FAIRE POUR AVOIR LE FIELD ID !?
    author_user = models.ForeignKey(settings.AUTH_USER_MODEL, null = True, to_field='id', on_delete=models.CASCADE)
    project_id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, blank=True)
    type_choices = (
        ('Back-End', 'Back-End'),
        ('Front-End', 'Front-End'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
    )
    type = models.CharField(max_length=9, choices=type_choices)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "projects"
