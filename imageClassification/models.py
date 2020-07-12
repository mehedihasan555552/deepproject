from django.db import models

class Users (models.Model):
    FullName = models.TextField()
    Email = models.TextField(unique=True)
    Password = models.TextField()

    def __str__(self):
        return self.FullName
    class Meta:
        verbose_name_plural = "Users"

class Files (models.Model):
    Path = models.TextField()
    userId = models.ForeignKey(Users, models.CASCADE)

    def __str__(self):
        return self.Path
    class Meta:
        verbose_name_plural = "Files"

class Result (models.Model):
    classLabel = models.TextField()
    fileId = models.ForeignKey(Files, models.CASCADE)

    def __str__(self):
        return self.classLabel