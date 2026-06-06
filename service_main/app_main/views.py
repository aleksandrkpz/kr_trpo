from django.shortcuts import render, redirect
import requests                  
from django.contrib import messages 
from datetime import datetime, date
from django.shortcuts import redirect

def login_as_admin(request):
    # Записываем в сессию (куки) роль админа
    request.session['user_role'] = 'admin'
    return redirect('dashboard_page')  # редирект обратно на главную

def logout_user(request):
    # Сбрасываем роль на обычного пациента
    request.session['user_role'] = 'patient'
    return redirect('dashboard_page')

#функция в сервисе Main которая открывается по адресу / (из URLS)
# context - словарь, в который складываются данные для html шаблона  {% stats %}например 
def dashboard_page(request):
    # 1. СОЗДАЕМ ПЕРЕМЕННУЮ СРАЗУ (на самом верху функции!)
    role = request.session.get('user_role', 'patient')
    all_diseases = [] 
    
    # 2. Пытаемся скачать симптомы из API сервиса input
    if role == 'patient':
        try:
            res_diseases = requests.get('http://input:8000/input/api/diseases/', timeout=2)
            if res_diseases.status_code == 200:
                # Вытаскиваем список из ключа 'diseases'
                all_diseases = res_diseases.json().get('diseases', [])
        except requests.exceptions.RequestException:
            pass

    # 3. Собираем контекст и передаем туда нашу рабочую переменную
    context = {
        'role':role,
        'all_diseases': all_diseases,
        'stats': None,
        'input_error': None,
        'stat_error': None,
    }
    
    

    # 4. ОБРАБОТКА НАЖАТИЯ КНОПКИ 
    if request.method == 'POST':
        selected_name = request.POST.get('name')
        birthday_str = request.POST.get('birthday', '')
        gender = request.POST.get('gender')
        city = request.POST.get('city', '').strip()
        selected_diseases = request.POST.getlist('disease') 

        if any(char.isdigit() for char in selected_name):
            messages.error(request, "Ошибка: В имени не должно быть цифр!")
            return render(request, 'app_main/dashboard.html', context)
        
        if any(char.isdigit() for char in city):
            messages.error(request, "Ошибка: В названии города не должно быть цифр!")
            return render(request, 'app_main/dashboard.html', context)
        
        if birthday_str:
            try:
                # Превращаем строку "YYYY-MM-DD" в реальный объект даты Python
                birthday_date = datetime.strptime(birthday_str, '%Y-%m-%d').date()
                # Проверяем, не в будущем ли дата (сейчас у нас 2026 год)
                if birthday_date > date.today():
                    messages.error(request, "Ошибка: Дата рождения не может быть в будущем")
                    return render(request, 'app_main/dashboard.html', context)
                
                # Дополнительно: защита от слишком старых дат (например, старше 120 лет)
                if birthday_date.year < (date.today().year - 120):
                    messages.error(request, "Пожалуйста, укажите корректный год рождения.")
                    return render(request, 'app_main/dashboard.html', context)
                
            except ValueError:
                messages.error(request, "Ошибка: Неверный формат даты.")
                return render(request, 'app_main/dashboard.html', context)   

        
        payload = {
            'name': selected_name,
            'birthday': request.POST.get('birthday'),
            'gender': request.POST.get('gender'),
            'city': request.POST.get('city'),
            'disease': selected_diseases         
        }

        #
        chosen_symptom_names = [
            d['disease'] for d in all_diseases if str(d['id']) in selected_diseases
        ]

        # риски
        red_flags = [ 'Боль в груди', 'Потеря сознания', 'Нарушение речи или асимметрия лица', 
                     'Внезапная слабость или онемение конечностей',
                     'Отек шеи, лица или губ', 'Кашель с кровью', 'Судороги']


        orange_flags = ['Одышка','Высокая температура', 'Острая боль', 'Сильный кашель',
                        'Спутанность сознания или сильная вялость', 'Непрекращающаяся рвота или диарея',
                        'Сыпь на коже', 'Внезапное сильное головокружение', 'Резкое ухудшение зрения']
        

        if any(symptom in red_flags for symptom in chosen_symptom_names):
            messages.error(
                request, 
                f"Критический риск! {selected_name}, у вас обнаружены опасные симптомы. "
                f"Настоятельно рекомендуем немедленно обратиться к регистратору для оказания неотложной помощи"
            )
        elif any(symptom in orange_flags for symptom in chosen_symptom_names) or len(selected_diseases) > 4:
            messages.warning(
                request, 
                f"Средний риск. {selected_name}, указанные симптомы требуют очного осмотра врача. "
                f"Пожалуйста, прямо сейчас пройдите в кабинет доврачебной помощи."
            )
        else:
            messages.success(
                request, 
                f"Низкий риск. {selected_name}, симптомы не угрожают жизни. "
                f"Соблюдайте домашний режим, пейте больше жидкости. При ухудшении обратитесь в клинику."
                f" '<a href='https://www.gosuslugi.ru/help/faq/doctor/17' target='_blank'> Как записаться на Госуслугах? </a>"
            )

        # Отправляем данные в базу
        try:
            input_url = 'http://input:8000/input/api/humans/create/'
            response = requests.post(input_url, json=payload, timeout=3)
            if response.ok:
                return redirect('/') 
            else:
                context['input_error'] = "input_error"
        except requests.exceptions.RequestException:
            context['input_error'] = "input_error"

    # 5. ПОЛУЧЕНИЕ СТАТИСТИКИ (Для правой плашки)
    elif role == 'admin':
        try:
            res_stats = requests.get('http://stat:8000/stat/api/get_stats/', timeout=2)
            if res_stats.status_code == 200:
                context['stats'] = res_stats.json().get('stats')
        except requests.exceptions.RequestException:
            context['stat_error'] = "Сервис статистики временно недоступен"
            pass
            
    return render(request, 'app_main/dashboard.html', context)