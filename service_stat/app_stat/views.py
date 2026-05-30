from django.http import JsonResponse
import requests
from datetime import datetime, date

def get_analytics(request):
    try:
        url = 'http://input:8000/input/api/humans/list'
        
        response = requests.get(url, timeout=5)
        response.raise_for_status() # Вызовет ошибку, если контейнер недоступен
        
        raw_data = response.json().get('data', [])
        
        # --- НАЧИНАЕМ СЧИТАТЬ СТАТИСТИКУ ---
        total_patients = len(raw_data)
        
        # 1. Распределение по полу
        males = sum(1 for h in raw_data if h['gender'] == 'M')
        females = sum(1 for h in raw_data if h['gender'] == 'F')
        
        # 2. Средний возраст
        ages = []
        all_diseases = []
        today = date.today()
        
        for h in raw_data:
            # Парсим дату рождения из строки обратно в объект даты
            birth_date = datetime.strptime(h['birthday'], '%Y-%m-%d').date()
            # Считаем чистый возраст
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            ages.append(age)
            
            # Собираем все болезни в один общий список для подсчета топа
            all_diseases.extend(h['diseases'])
            
        avg_age = sum(ages) / len(ages) if ages else 0
        
        # 3. Топ-3 самых частых болезней
        disease_counts = {}
        for d in all_diseases:
            disease_counts[d] = disease_counts.get(d, 0) + 1
        # Сортируем словарь по количеству упоминаний (по убыванию)
        top_diseases = sorted(disease_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Формируем итоговый ответ
        analytics_result = {
            'status': 'success',
            'stats': {
                'total_patients': total_patients,
                'gender_split': {'males': males, 'females': females},
                'average_age': round(avg_age, 1),
                'top_diseases': top_diseases # Вернет список кортежей [('Грипп', 5), ('ОВРИ', 3)]
            }
        }
        return JsonResponse(analytics_result, json_dumps_params={'ensure_ascii': False})

    except requests.exceptions.RequestException as e:
        # Если сервис ввода упал — отдаем ошибку в формате JSON, чтобы сайт не «лег»
        return JsonResponse({
            'status': 'error',
            'message': f'Сервис ввода данных недоступен. Ошибка: {str(e)}'
        }, status=503)