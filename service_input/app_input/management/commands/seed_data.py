import random
from django.core.management.base import BaseCommand
from app_input.models import Human, Disease

class Command(BaseCommand):
    help = 'Заполнение БД тестовыми данными'

    def handle(self, *args, **kwargs):
        # Список имен
        names = ["Иван", "Мария", "Алексей", "Елена", "Дмитрий"]
        cities = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург"]
        genders = ["M", "F"]
        
        # Получаем все существующие болезни
        diseases = list(Disease.objects.all())
        
        if not diseases:
            self.stdout.write(self.style.ERROR("Сначала добавьте болезни в БД!"))
            return

        for _ in range(1000):  # Создаем пациентов
            name = random.choice(names)
            city = random.choice(cities)
            gender = random.choice(genders)
            # Случайная дата рождения от 1950 до 2010
            year = random.randint(1950, 2010)
            birthday = f"{year}-0{random.randint(1,9)}-{random.randint(10,28)}"
            
            human = Human.objects.create(
                name=name,
                birthday=birthday,
                gender=gender,
                city=city
            )
            
            # Добавляем 1-3 случайные болезни
            selected = random.sample(diseases, random.randint(1, min(3, len(diseases))))
            human.disease.set(selected)
            
        self.stdout.write(self.style.SUCCESS("База успешно заполнена 10 тестовыми пациентами!"))