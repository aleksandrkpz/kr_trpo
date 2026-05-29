from django.db import models

class Disease(models.Model):
    disease = models.CharField(max_length = 50, verbose_name = 'Название болезни')
    def __str__(self):
        return self.disease

class Meta:
    managed = False
    db_table = 'app_input_disease'



class Human (models.Model):
    name = models.CharField(max_length = 100, verbose_name = 'ФИО')

    LIST_GENDER = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]

    gender = models.CharField(max_length = 1, choices = LIST_GENDER, verbose_name = 'Пол')
    birthday = models.DateField(verbose_name = 'Дата рождения')
    disease = models.ManyToManyField(Disease, verbose_name = 'Заболевание')

    def __str__(self):
        return self.namefrom django.db import models

# Create your models here.
