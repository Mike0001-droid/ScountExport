from django.db import models
from django.contrib.auth.models import User
import os


def get_upload_path(instance, filename):
    path = 'files/' + os.path.join(
        f"{instance.upload_date.date()} {instance.user} {instance.file_name[10:] if len(instance.file_name) > 10 else instance.file_name}"
    )
    return path


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class UserFile(models.Model):
    upload_date = models.DateTimeField('Дата загрузки файла', auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField('Загруженный файл', upload_to=get_upload_path)
    file_name = models.CharField('Название загруженного файла', max_length=100, default='')

    def __str__(self):
        return f"{self.user.username}_{self.file_name}"
    
    def save(self, *args, **kwargs):
        if not self.file_name:
            self.file_name = str(self.file).replace('_', ' ')
            super(UserFile, self).save(*args, **kwargs)
        

