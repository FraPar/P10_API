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


class Contributors(models.Model):
    user = models.ForeignKey(User, null = True, to_field='id', on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, null = True, to_field='project_id', on_delete=models.CASCADE)
    permission_choices = (
        ('Back-End', 'Back-End'),
        ('Front-End', 'Front-End'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
    )
    permission = models.CharField(max_length=9, choices=permission_choices)
    role = models.CharField(max_length=128)


class Issues(models.Model):
    issue_id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=128)
    tag_choices = (
        ('Bug', 'Bug'),
        ('Tâche', 'Tâche'),
        ('Amélioration', 'Amélioration'),
    )
    tag = models.CharField(max_length=12, choices=tag_choices)
    priority_choices = (
        ('Faible', 'Faible'),
        ('Moyenne', 'Moyenne'),
        ('Élevée', 'Élevée'),
    )
    priority = models.CharField(max_length=7, choices=priority_choices)
    project = models.ForeignKey(Projects, null = True, to_field='project_id', on_delete=models.CASCADE)
    status = models.CharField(max_length=128)
    author_user = models.ForeignKey(settings.AUTH_USER_MODEL, null = True, to_field='id', on_delete=models.CASCADE)
    # assignee_user_id = models.ForeignKey(User, default=settings.AUTH_USER_MODEL, null = True, to_field='id', related_name="assignee_user", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    description = models.CharField(max_length=128)
    author_user = models.ForeignKey(settings.AUTH_USER_MODEL, null = True, to_field='id', on_delete=models.CASCADE)
    issue_id = models.ForeignKey(Issues, null = True, to_field='issue_id', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    