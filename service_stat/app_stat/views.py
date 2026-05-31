from django.http import JsonResponse
import requests
from datetime import datetime, date

def get_analytics(request):
    try:
        # получаем данные из input
        url = 'http://input:8000/input/api/humans/list'
        response = requests.get(url, timeout=5)
        response.raise_for_status() 
        raw_data = response.json().get('data', [])
        total_patients = len(raw_data)
        
        # считаем мужчин и женщин
        males = sum(1 for h in raw_data if h['gender'] == 'M')
        females = sum(1 for h in raw_data if h['gender'] == 'F')
        
        # создаем пустые списки
        ages = []
        all_diseases = []
        cities = [] 
        # и сегодняшнюю дату
        today = date.today()
        
        # Сбор возрастов, городов и болезней, подсчет среденего возраста
        for h in raw_data:
            birth_date = datetime.strptime(h['birthday'], '%Y-%m-%d').date()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            ages.append(age)
            all_diseases.extend(h['diseases'])
            cities.append(h.get('city', 'Не указан'))
        avg_age = sum(ages) // len(ages) if ages else 0
        
        # Получаем все болезни в словарь и сортируем при помощи лямбда-функции
        disease_counts = {}
        for d in all_diseases:
            disease_counts[d] = disease_counts.get(d, 0) + 1
        top_diseases = sorted(disease_counts.items(), key=lambda x: x[1], reverse=True)[:3]

        # Получаем все города в словарь и сортируем при помощи лямбда-функции
        city_counts = {}  
        for c in cities:
            city_counts[c] = city_counts.get(c, 0) + 1
        top_cities = sorted(city_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Результат упаковываем в формат JSON
        analytics_result = {
            'status': 'success',
            'stats': {
                'total_patients': total_patients,
                'gender_split': {'males': males, 'females': females},
                'average_age': avg_age,
                'top_diseases': top_diseases,
                'top_cities': top_cities  
            }
        }
        return JsonResponse(analytics_result, json_dumps_params={'ensure_ascii': False},)

    except requests.exceptions.RequestException:
        return JsonResponse({
            'status': 'stat_error',
            'message': 'stat_error'
        },)