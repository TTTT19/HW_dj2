from collections import Counter

from django.shortcuts import render_to_response

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся


counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    counter_show[(request.GET.get('from-landing'))] += 1
    counter_click['count'] += 1
    return render_to_response('index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов

    if request.GET.get('ab-test-arg') == 'test':
        return render_to_response('landing_alternate.html')
    elif request.GET.get('ab-test-arg') == 'original':
        return render_to_response('landing.html')
    else:
        return render_to_response('index.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:
    try:
        test_conversion_original = int(counter_show['original']) / int(counter_click['count'])
    except:
        test_conversion_original = 'Нет данных'
    try:
        test_convesion_test = int(counter_show['test']) / int(counter_click['count'])
    except:
        test_convesion_test = 'Нет данных'
    return render_to_response('stats.html', context={
        'test_conversion': test_conversion_original,
        'original_conversion': test_convesion_test,
    })
