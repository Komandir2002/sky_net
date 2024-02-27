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

def show_applications(request):
    applications = models.Applications.objects.all().order_by('id')
    return render(request, 'show_applications.html', {'applications': applications})

def review(request, application_slug):
    # Здесь логика получения данных заявки по application_slug
    # Например:
    application = get_object_or_404(models.Applications, slug=application_slug)
    return render(request, 'index.html', {'application': application})

def rate_application(request, application_slug):
    if request.method == 'POST':
        data = json.loads(request.body)
        score = data['score']
        message = data.get('message', '')  # Извлекаем сообщение, если оно есть

        application = models.Applications.objects.get(slug=application_slug)  # Находим соответствующее приложение по slug
        rating, created = models.ApplicationRating.objects.update_or_create(
            application=application,
            defaults={'score': score, 'message': message}  # Обновляем или создаем оценку с сообщением
        )

        return JsonResponse({'status': 'success', 'message': 'Rating submitted successfully'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@csrf_exempt
def planup_p(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        request.session['user_id'] = user_id  # Сохраняем user_id в
        request.session.save()
        print(user_id)
        # Возвращаем user_id в ответе
        return JsonResponse({"message": "This is a POST request. User ID received.", "user_id": user_id}, status=200)
    else:
        return JsonResponse({"message": "This is not a POST request."}, status=400)


def application_info(request, application_slug):
    application = get_object_or_404(models.Applications, slug=application_slug)
    user_id = request.session.get('user_id')
    print(user_id)
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


    return render(request, 'application_info.html', {
        'application': application,
        'reviews': reviews,
        'bitrix_data': bitrix_data,
        'user_id':user_id

    })

def add_application(request):
    message = ""
    deal_id = request.GET.get('deal_id')  # Получаем deal_id из GET-запроса вне зависимости от типа запроса
    bitrix_data = {}  # Инициализируем bitrix_data как пустой словарь заранее
    print(f"deal_id: {deal_id}")

    if request.method == "POST":
        form = forms.AplicationsForm(request.POST, request.FILES)
        if form.is_valid():
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


from django.http import HttpResponse

from django.http import JsonResponse


@csrf_exempt
def testik(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        # Возвращаем user_id в ответе
        return JsonResponse({"message": "This is a POST request. User ID received.", "user_id": user_id}, status=200)

    else:
        return JsonResponse({"message": "This is not a POST request."}, status=400)


