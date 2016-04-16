from django.db import models
from django.contrib.auth.models import *
import time


# Group

class Group(models.Model):
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    format = models.CharField(max_length=50)

    class Meta:
        permissions = (
            ("can_admin", "can admin"),
            ("can_developer", "can developer"),
            ("can_plan", "can plan"),
            ("can_art", "can art"),
        )

    def __unicode__(self):
        return self.name


# Tag and Group To Tag

class Tag(models.Model):
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class GroupToTag(models.Model):
    group = models.ForeignKey(Group)
    tag = models.ForeignKey(Tag)
    info = models.CharField(max_length=200)


class TagInfo(models.Model):
    group = models.ForeignKey(Group)
    tag = models.ForeignKey(Tag)
    code = models.IntegerField(null=False)
    name = models.CharField(max_length=100)


class TagOrder(models.Model):
    group = models.ForeignKey(Group)
    code = models.CharField(max_length=100)
    sort = models.IntegerField(null=False)
    is_select = models.BooleanField(default=False)


# Art

def screen_shot_path(instance, filename):
    file_time = time.strftime('%Y%m%d%H%M%s', time.localtime(time.time()))
    filename = str(file_time) + '.png'
    return '/'.join([instance.group.name, 'preview', time.strftime('%m%d', time.localtime(time.time())), filename])

def resource_file_path(instance, filename):
    file_time = time.strftime('%Y%m%d%H%M%s', time.localtime(time.time()))
    filename = str(file_time) + instance.group.format
    return '/'.join([instance.group.name, 'resource', time.strftime('%m%d', time.localtime(time.time())), filename])

class Art(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    description = models.TextField()
    priority = models.IntegerField()
    version = models.CharField(max_length=50)
    upload_time = models.DateTimeField(auto_now_add=True)
    screen_shot = models.ImageField(upload_to=screen_shot_path, null=True)
    resource_file = models.FileField(upload_to=resource_file_path, null=True)
    is_audit = models.BooleanField(default=False)
    is_pass = models.BooleanField(default=False)
    reason = models.TextField(null=True)


class ArtInfo(models.Model):
    art = models.ForeignKey(Art)
    tag = models.ForeignKey(Tag)
    value = models.TextField()
