from django.test import TestCase, Client
from unittest.mock import patch
import requests

class StatAnalyticsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.analytics_url = '/stat/api/get_stats/' 

    @patch('requests.get')
    def test_get_analytics_success(self, mock_get):
        # Тест успешного расчета статистики на основе данных от сервиса input
        
        # Готовим моковый ответ, который якобы пришел от сервиса input
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': [
                {
                    'gender': 'M',
                    'birthday': '2000-01-01', 
                    'city': 'Нск',
                    'diseases': ['Грипп', 'Бронхит']
                },
                {
                    'gender': 'F',
                    'birthday': '1990-01-01',  
                    'city': 'Нск',
                    'diseases': ['Грипп']
                }
            ]
        }

        #  Делаем запрос к нашему сервису статистики
        response = self.client.get(self.analytics_url)
        
        # Проверяем результаты расчетов
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        
        self.assertEqual(json_data['status'], 'success')
        stats = json_data['stats']
        
        # Проверяем математику нашего сервиса stat
        self.assertEqual(stats['total_patients'], 2)
        self.assertEqual(stats['gender_split']['males'], 1)
        self.assertEqual(stats['gender_split']['females'], 1)
        
        # Средний возраст: 
        self.assertEqual(stats['average_age'], 31)
        
        # Проверяем сортировку ТОП-ов 
        self.assertEqual(stats['top_diseases'][0][0], 'Грипп')
        self.assertEqual(stats['top_cities'][0][0], 'Нск')

    @patch('requests.get')
    def test_get_analytics_input_down(self, mock_get):
        # Тест поведения системы, если сервис input упал или недоступен
        
        # Имитируем ошибку сети (RequestException) при попытке связаться с input
        mock_get.side_effect = requests.exceptions.RequestException("Input service is offline")

        response = self.client.get(self.analytics_url)
        
        # Сервис не должен упасть с 500 ошибкой, он должен вернуть stat_error
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data['status'], 'stat_error')
        self.assertEqual(json_data['message'], 'stat_error')