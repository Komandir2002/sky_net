import json
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
import asyncio
from .parser_bx import bitrix_1c_s
from . import models,forms
from django.contrib.sessions.models import Session
sessions = Session.objects.all()
for session in sessions:
    data = session.get_decoded()
    print(data)



def review(request, application_slug):
    # Здесь логика получения данных заявки по application_slug
    # Например:
    application = get_object_or_404(models.Applications, slug=application_slug)
    return render(request, 'index.html', {'application': application})





def application_info(request, application_slug):
    application = get_object_or_404(models.Applications, slug=application_slug)
    user_data_str = request.session.get('user_id', '[]')

    try:
        # Десериализация внешнего списка
        outer_list = json.loads(user_data_str)
        # Десериализация внутреннего списка
        if outer_list:
            inner_list_str = outer_list[0]
            inner_list = json.loads(inner_list_str)
            user_data = inner_list[0] if inner_list else {}
        else:
            user_data = {}
    except (json.JSONDecodeError, IndexError) as e:
        user_data = {}

    # Преобразуем строку JSON обратно в Python объект (список словарей)
    try:
        user_data_list = json.loads(user_data_str)
        user_data = user_data_list[0] if user_data_list and isinstance(user_data_list, list) else {}
    except (json.JSONDecodeError, IndexError):
        user_data = {}

    # Проверка, что полученный объект является списком словарей, и извлечение первого элемента

    planup_id = request.session.get('planup_id')
    print(user_data)
    print(planup_id)
    status = application.status_id.id
    print(status)
    try:
        reviews = application.reviews  # Убедитесь, что используете .all() для получения QuerySet отзывов
    except ObjectDoesNotExist:
        reviews = None

    bitrix_data = {}
    if application.bx_id:
        try:
            # Пытаемся синхронно получить данные из Bitrix24
            bitrix_data = asyncio.run(bitrix_1c_s(application.bx_id))
        except Exception as e:
            print(f"Ошибка при получении данных из Bitrix24: {e}")
    if isinstance(user_data, dict):
        user_full_name = user_data.get('full_name', 'Исполитель не назначен')
        user_phone_number = user_data.get('phone_number', 'Контакт не указан')
    else:
        user_full_name = 'Исполитель не назначен'
        user_phone_number = 'Контакт не указан'

    return render(request, 'application_info.html', {
        'application': application,
        'reviews': reviews,
        'bitrix_data': bitrix_data,
        'image': application.image,
        'user_full_name': user_full_name,
        'user_phone_number': user_phone_number,
        'planup_id':planup_id

    })

def add_application(request):
    message = ""
    deal_id = request.GET.get('deal_id')  # Получаем deal_id из GET-запроса вне зависимости от типа запроса
    bitrix_data = {}  # Инициализируем bitrix_data как пустой словарь заранее
    print(f"deal_id: {deal_id}")

    if request.method == "POST":
        form = forms.AplicationsForm(request.POST, request.FILES)
        if form.is_valid():
            user_id = request.POST.get('user_id')
            planup_id = request.POST.get('planup_id')
            request.session['user_id'] = json.dumps([user_id])
            request.session.save()
            print("Извлекаем из сессии:", request.session.get('user_id', '[]'))
            request.session['planup_id'] = planup_id  # Сохраняем planup_id в сесси
            request.session.save()
            form.save()
            return HttpResponse("Заявка добавлена успешно.")
    else:
        initial_data = {}
        if deal_id:
            try:
                # Пытаемся асинхронно получить данные
                bitrix_data = asyncio.run(bitrix_1c_s(deal_id))
                initial_data['bx_id'] = deal_id
                print(bitrix_data)  # Добавьте этот вывод для отладки
            except Exception as e:
                message = f"Ошибка получения данных из Bitrix24: {e}"
                bitrix_data = {}
        form = forms.AplicationsForm(initial=initial_data)  # Создаем форму с начальными данными

    return render(request, "add_application.html", {"form": form, "message": message, "bitrix_data": bitrix_data,"deal_id": deal_id})


def update_application(request, application_slug):
    message = ""
    instance = get_object_or_404(models.Applications, slug=application_slug)

    if request.method == "POST":
        form = forms.AplicationsForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            # Проверяем, изменились ли user_id или planup_id
            if instance.user_id != form.cleaned_data['user_id'] or instance.planup_id != form.cleaned_data['planup_id']:
                # Обновляем статус, например, на "В процессе"
                instance.status_id = models.Status.objects.get(status='В процессе')
                instance.save()
                message = "Статус обновлен"
            else:
                message = "user_id и planup_id не изменились, статус не обновлен"

            form.save()
            return HttpResponse(f"Заявка обновлена успешно. {message}")
    else:
        form = forms.AplicationsForm(instance=instance)

    return render(request, "update_application.html", {"form": form, "message": message})



