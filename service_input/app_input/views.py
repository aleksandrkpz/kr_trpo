from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Human, Disease

# 1. API: Отдаем список болезней для формы ввода
def api_get_diseases(request):
    # Забираем id и названия болезней
    diseases = list(Disease.objects.values('id', 'disease'))
    return JsonResponse({'status': 'success', 'diseases': diseases}, json_dumps_params={'ensure_ascii': False})


# 2. API: Принимаем данные из формы и сохраняем в БД
@csrf_exempt # Отключаем CSRF для межсервисных запросов, main проверит его сам
def api_create_human(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        birthday = request.POST.get('birthday')
        gender = request.POST.get('gender')
        selected_diseases = request.POST.getlist('disease') 

        new_human = Human.objects.create(
            name=name,
            birthday=birthday,
            gender=gender
        )
        new_human.disease.set(selected_diseases)

        # Вместо HttpResponse с HTML-тегом возвращаем JSON-статус
        return JsonResponse({'status': 'success', 'message': 'Пациент успешно сохранен в базу данных!'})
    
    return JsonResponse({'status': 'error', 'message': 'Только POST запросы'}, status=405)


# 3. API: Отдаем данные людей для сервиса статистики 
def api_get_humans_data(request):
    humans = Human.objects.prefetch_related('disease').all()
    output_data = []
    for human in humans:
        output_data.append({
            'id': human.id,
            'name': human.name,
            'gender': human.gender,
            'birthday': human.birthday.strftime('%Y-%m-%d'),
            'diseases': [d.disease for d in human.disease.all()]
        })
    return JsonResponse({'status': 'success', 'data': output_data}, json_dumps_params={'ensure_ascii': False})
