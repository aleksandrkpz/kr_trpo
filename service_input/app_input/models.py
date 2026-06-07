from django.db import models
# объявляем класс Болезнь, чтобы иметт возможность использовать свяь Many-to-Many
class Disease(models.Model):
    disease = models.CharField(max_length = 50, verbose_name = 'Название болезни')
    def __str__(self):
        return self.disease

class Human (models.Model):
    name = models.CharField(max_length = 100, verbose_name = 'ФИО')
    LIST_GENDER = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    city = models.CharField(max_length= 100, verbose_name= 'Город',default='Не указан')
    gender = models.CharField(max_length = 1, choices = LIST_GENDER, verbose_name = 'Пол')
    birthday = models.DateField(verbose_name = 'Дата рождения')
    # связь многие-ко-многим
    disease = models.ManyToManyField(Disease, verbose_name = 'Заболевание')

    def __str__(self):
        return self.name
