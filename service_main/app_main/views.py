from django.shortcuts import render, redirect
import requests


#функция в сервисе Main которая открывается по адресу / (из URLS)
# context - словарь, в который складываются данные для html шаблона  {% stats %}например 
def dashboard_page(request):
    context = {
        'all_diseases': [], #{% for d in all_diseases %}
        'stats': None,
        'input_error': None, #{% if input_error %}
        'stat_error': None,
    }

    
    if request.method == 'POST':
        
     # словарь payload забирает данные из HTML формы по их 'name'
        payload = {
            'name': request.POST.get('name'),
            'birthday': request.POST.get('birthday'),
            'gender': request.POST.get('gender'),
            'city': request.POST.get('city'),
            #здесь getlist, т.к. болезней много                   
            'disease': request.POST.getlist('disease')         
        }
        #отправляем в сервис input данные из словаря payload в формате json
        try:
            input_url = 'http://input:8000/input/api/humans/create/'
            response = requests.post(input_url, json=payload, timeout=3)
            if response.ok:
                return redirect('/') 
        # обрабатываем исключение если сервис input недоступен
            else:
                context['input_error'] = "input_error"
        except requests.exceptions.RequestException:
            context['input_error'] = "input_error"

    
        # получаем из сервиса input данные о болезнях
        # кладем данные в all_diseases словаря context в начале функции (предварительно превращая json в словарь)
        # применяем метод .get() и по ключу 'diseases' ищем его пару

        ###########  ПОЛУЧЕННЫЙ СЛОВАРЬ ИМЕЕТ ТАКОЙ ВИД  ############
#           'status': 'success', 
#           'diseases': [
#               {'id': 1, 'disease': 'Грипп'}, 
#               {'id': 2, 'disease': 'Сахарный диабет'}
#           ]
    try:
        res_diseases = requests.get('http://input:8000/input/api/diseases/', timeout=2)
        if res_diseases.status_code == 200:
            context['all_diseases'] = res_diseases.json().get('diseases', [])
    except requests.exceptions.RequestException:
        context['input_error'] = "input_error"

         #получаем из сервиса stat статистику
    try:
        res_stats = requests.get('http://stat:8000/stat/api/get_stats/', timeout=2)
         # если сервис ответил, то 
        if res_stats.status_code == 200:
        # кладем данные в ['stats'] словаря context в начале функции (предварительно превращая json в словарь)
        # применяем метод .get() и по ключу 'diseases' ищем его пару    
            context['stats'] = res_stats.json().get('stats')
    except requests.exceptions.RequestException:
        context['stat_error'] = "stat_error"
        
    # возвращаем веб-страницу с данными
    return render(request, 'app_main/dashboard.html', context)