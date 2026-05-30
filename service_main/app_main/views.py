from django.shortcuts import render, redirect
import requests

def dashboard_page(request):
    # Инициализируем контекст на случай, если сервисы лежат
    context = {
        'all_diseases': [],
        'stats': None,
        'input_error': None,
        'stat_error': None,
    }

    # Если пользователь заполнил форму и нажал "Отправить"
    if request.method == 'POST':
        # Перенаправляем данные формы напрямую в сервис ввода
        try:
            # Ссылаемся на имя контейнера сервиса ввода в докере
            input_url = 'http://input:8000/input/api/humans/create/'
            # Передаем данные, которые прислал пользователь
            response = requests.post(input_url, data=request.POST, timeout=3)
            
            if response.ok:
                # Перезагружаем страницу, чтобы увидеть обновленную статистику
                return redirect('/') 
        except requests.exceptions.RequestException:
            context['input_error'] = "Не удалось сохранить данные, сервис ввода недоступен."

    # Если обычный GET-запрос (просто открыли страницу)
    # 1. Запрашиваем болезни у service_input для выпадающего списка
    try:
        res_diseases = requests.get('http://input:8000/input/api/diseases/', timeout=2)
        context['all_diseases'] = res_diseases.json().get('diseases', [])
    except requests.exceptions.RequestException:
        context['input_error'] = "Сервис ввода недоступен. Форма отключена."

    # 2. Запрашиваем посчитанную статистику у service_stat
    try:
        res_stats = requests.get('http://stat:8000/stat/api/get_stats/', timeout=2)
        if res_stats.status_code == 200:
            context['stats'] = res_stats.json().get('stats')
    except requests.exceptions.RequestException as e:
        print(f"\nОШИБКА ПОДКЛЮЧЕНИЯ К СТАТИСТИКЕ: {e}\n")
        context['stat_error'] = "Сервис статистики недоступен."

    # Рендерим ОДНУ общую страницу
    return render(request, 'app_main/dashboard.html', context)