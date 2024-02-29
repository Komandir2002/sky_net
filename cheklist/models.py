from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField

# Create your models here.


'''Модель дял отображения статуса заявки'''
class Status(models.Model):
    CHOISE_STATUS = (
        ('Оформлено','Оформлено'),
        ('В процессе','В процессе'),
        ('Выполнено','Выполнено'),
    )
    status = models.CharField(max_length=15,choices=CHOISE_STATUS)

    def __str__(self):
        return self.status

'''Модель для оброботки заявок'''
class Applications(models.Model):
    status_id = models.ForeignKey(Status,on_delete=models.CASCADE)
    bx_id = models.IntegerField()
    planup_id = models.IntegerField()
    user_id = models.TextField(max_length=255,null=True,blank=True)
    slug = models.SlugField(unique=True, blank=True, editable=False, verbose_name="URL")
    image = models.ImageField(upload_to="", blank=True)

    def save(self, *args, **kwargs):
        if not self.id:  # Если объект еще не сохранен и не имеет ID
            super().save(*args, **kwargs)  # Сначала сохраняем, чтобы получить ID
        self.slug = f"slug-{self.id}"  # Пример генерации slug с использованием ID
        super().save(*args, **kwargs)  # Повторное сохранение с установленным slug

    def __str__(self):
        if self.user_id is not None:
            return f"Application {self.id} - User: {self.user_id}"
        else:
            return f"Application {self.id} - User: Не назначен"


class ApplicationRating(models.Model):
    application = models.OneToOneField('Applications', on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(default=0)
    message = models.TextField(blank=True)

    def __str__(self):
        return f"Rating for Application {self.application.id}: {self.score} stars"
