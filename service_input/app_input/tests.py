import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import Human, Disease

class HumanApiTestCase(TestCase):
    def setUp(self):
        # Этот метод выполняется ПЕРЕД каждым тестом.
        # Создаем тестовый клиент и наполняем временную базу болезнями.
        self.client = Client()
        self.disease_1 = Disease.objects.create(disease="Грипп")
        self.disease_2 = Disease.objects.create(disease="ОВРИ")
        self.disease_3 = Disease.objects.create(disease="Ангина")
        self.disease_4 = Disease.objects.create(disease="Бронхит")
        

    def test_api_create_human_success(self):
        """Проверяем успешное создание пациента с городом и 4 болезнями через JSON"""
        
        # 1. Готовим payload, как если бы его прислал сервис main
        payload = {
            "name": "Иванов Иван Иванович",
            "birthday": "1990-05-15",
            "gender": "M",
            "city": "Томск",
            # Передаем ID всех четырех созданных болезней
            "disease": [self.disease_1.id, self.disease_2.id, self.disease_3.id, self.disease_4.id]
        }

        # 2. Делаем POST-запрос на наш API (укажи тут имя своего url или прямой путь)
        url = '/input/api/humans/create/'  
        response = self.client.post(
            url, 
            data=json.dumps(payload), 
            content_type='application/json'
        )

        # 3. ПРОВЕРКИ (Asserts)
        # Проверяем, что сервер ответил ОК (200)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

        # Проверяем, что пациент реально появился в базе данных
        self.assertEqual(Human.objects.count(), 1)
        
        # Достаем его и проверяем поля
        human = Human.objects.first()
        self.assertEqual(human.name, "Иванов Иван Иванович")
        self.assertEqual(human.city, "Томск")
        self.assertEqual(human.gender, "M")

        # КРИТИЧЕСКАЯ ПРОВЕРКА: привязались ли все 4 болезни?
        linked_diseases_count = human.disease.count()
        self.assertEqual(linked_diseases_count, 4)

        