from django.shortcuts import render
from django.http import HttpResponse
from .models import Human, Disease

def input_page(request):
    if request.method == 'GET':
        # Достаем все объекты болезней
        disease_objects = Disease.objects.all()
        # Передаем их в HTML под именем 'all_diseases'
        return render(request, 'app_input/index.html', {'all_diseases': disease_objects})

    elif request.method == 'POST':
        name = request.POST.get('name')
        birthday = request.POST.get('birthday')  # Забираем 'birthday' из HTML
        gender = request.POST.get('gender')
        # Забираем массив ID выбранных болезней из HTML (из <select name="disease">)
        selected_diseases = request.POST.getlist('disease') 

        # Создаем человека в базе
        new_human = Human.objects.create(
            name=name,
            birthday=birthday,
            gender=gender
        )

        # Привязываем болезни через ManyToMany-поле 'disease' (как в твоей модели Human)
        new_human.disease.set(selected_diseases)

        return HttpResponse("<h3>Пациент успешно сохранен в базу данных!</h3> <a href='.'>Добавить еще одного</a>")
