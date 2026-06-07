import json
from django.test import TestCase, Client # type: ignore
from .models import Disease, Human

class ApiInputTestCase(TestCase):
    def setUp(self):
        # Создаем виртуального клиента для отправки запросов
        self.client = Client()
        # Наполняем временную БД тестовой болезнью
        self.disease = Disease.objects.create(id=1, disease="Грипп")

    def test_api_get_diseases(self):
        #Проверка, что API отдает список болезней в правильном формате
        response = self.client.get('/input/api/diseases/')
        
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data['status'], 'success')
        self.assertEqual(len(json_data['diseases']), 1)
        self.assertEqual(json_data['diseases'][0]['disease'], 'Грипп')

    def test_api_create_human_success(self):
        #Проверка успешного сохранения пациента через POST-запрос
        payload = {
            'name': 'Тест',
            'birthday': '1995-05-10',
            'gender': 'M',
            'city': 'Томск',
            'disease': [self.disease.id]
        }
        
        # Отправляем JSON-пакет, имитируя сервис main
        response = self.client.post(
            '/input/api/humans/create/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        
        # Проверяем, что человек реально создался в базе
        self.assertEqual(Human.objects.count(), 1)
        saved_human = Human.objects.first()
        self.assertEqual(saved_human.name, 'Тест')
        self.assertEqual(saved_human.disease.first().disease, 'Грипп')