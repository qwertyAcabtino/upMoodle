from django.db import models


# Carrer, course, subject
class LevelType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Level(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    type = models.ForeignKey('LevelType') 
    visible = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class NoteBoard(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=100)
    text = models.CharField(max_length=2000)
    level = models.ForeignKey('Level')

    def __unicode__(self):
        return self.topic