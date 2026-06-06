from django.test import TestCase, Client
from django.contrib.messages import get_messages

class MainValidationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_name_with_digits_rejected(self):
        # Проверка защиты: имя с цифрами должно вызывать ошибку
        response = self.client.post('/', data={
            'name': 'Иван321',
            'birthday': '1990-01-01',
            'gender': 'Мужской',
            'city': 'Москва',
            'disease': []
        })
        
        # Проверяем, что вернули ту же страницу с ошибкой
        self.assertEqual(response.status_code, 200)
        
        # Извлекаем messages
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("В имени не должно быть цифр!" in str(m) for m in messages))
        # Проверка защиты: дата рождения в будущем
    def test_future_birthday_rejected(self):
        
        response = self.client.post('/', data={
            'name': 'Алексей',
            'birthday': '2030-12-12',
            'gender': 'Мужской',
            'city': 'Самара',
            'disease': []
        })
        
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Дата рождения не может быть в будущем" in str(m) for m in messages))