from csv import DictReader
from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.http import HttpResponse

from pagination.app.settings import BUS_STATION_CSV
from django.shortcuts import render_to_response, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse(bus_stations))



from pagination.app.settings import BUS_STATION_CSV

# Путь к файлу храниться в настройках settings.BUS_STATION_CSV. Для чтения csv файла можете использовать DictReader
# и учтите что файл в кодировке cp1251
DATA = []
with open(BUS_STATION_CSV) as f:
    reader = DictReader(f)
    for row in reader:
        # new_row = [row['Name'],row['Street'],row['District']]
        DATA.append(row)

def listing(request):
    # contact_list = Contacts.objects.all()
    paginator = Paginator(DATA, 25) # Show 25 contacts per page
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, 'list.html', {'contacts': contacts})


# Для формирования url'а с get параметром помимо reverse используйте urllib.parse.urlencode

def bus_stations(request):
    current_page = request.GET.get('page',1)
    paginator = Paginator(DATA, 10)  # Show 25 contacts per page
    page = request.GET.get('page')
    bus_stations = paginator.get_page(page)
    next_page_url =(f'?page={bus_stations.next_page_number()}')
    if bus_stations.has_previous():
        prev_page_url = (f'?page={bus_stations.previous_page_number()}')
    else:
        prev_page_url = None
    return render_to_response('index.html', context={
        'bus_stations': bus_stations,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })

