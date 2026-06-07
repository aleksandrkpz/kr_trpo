import json 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Human, Disease

# API функция для возврата списка болезенй в формате JSON
def api_get_diseases(request):
    diseases = list(Disease.objects.values('id', 'disease'))
    return JsonResponse({'status': 'success', 'diseases': diseases}
                        , json_dumps_params={'ensure_ascii': False})

# Разрешает отправлять POST-запросы без csrf_token
# В данном проекте нужен для обмена данными между микросервисами
@csrf_exempt

# API функция сохранения человека в БД.
def api_create_human(request):
    if request.method == 'POST':
        data = json.loads(request.body) # Берем JSON из сервиса MAIN 
        #парсим его 
        name = data.get('name')
        birthday = data.get('birthday')
        gender = data.get('gender')
        city = data.get('city', 'Не указан')  
        selected_diseases = data.get('disease', [])
        new_human = Human.objects.create(
            name=name,
            birthday=birthday,
            gender=gender,
            city=city  
        )
        new_human.disease.set(selected_diseases)

    return JsonResponse({'status': 'success', 'message': 'success'})
              
# функция сериализации в output_data всех людей из таблицы Human 
def api_get_humans_data(request):
    # оптимизация запросов к БД (prefetch_related)
    humans = Human.objects.prefetch_related('disease').all()
    output_data = []
    for human in humans:
        diseases_names = []
        # собираем текстовые названия болезней, связанных с текущим пациентом 
        for d in human.disease.all():
            diseases_names.append(d.disease)
        output_data.append({
            'id': human.id,
            'name': human.name,
            'gender': human.gender,
            'birthday': human.birthday.strftime('%Y-%m-%d'),
            'city': human.city, 
            'diseases': diseases_names
        })
    return JsonResponse({'status': 'success', 'data': output_data}, 
                        json_dumps_params={'ensure_ascii': False})