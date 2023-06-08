
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
import requests
import datetime
from django.conf import settings


from django.http import JsonResponse
from .models import FavouriteModel, IpModel
# Create your views here.

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):  
    dt = datetime.datetime.now()
    # if dt.month <= 9:
    #     month = "0"+str(dt.month)
    # else:
    #     month = str(dt.month)
    
    # if dt.day <= 9:
    #     day = "0"+str(dt.day)
    # else:
    #     day = str(dt.day)
        
    datefmt = str(dt.year)+str(dt.month)+str(dt.day)
    Fixtures = []  
    # print(datefmt)
    
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-league"    
    today_url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-date"
        
    querystring = {"Category":"soccer","Ccd":"england","Scd":"premier-league","Timezone":"-7"}
    today_querystring = {"Category":"soccer","Date":datefmt,"Timezone":"-7"}
    
    headers = {
        "X-RapidAPI-Key": settings.API_KEY,
        "X-RapidAPI-Host": "livescore6.p.rapidapi.com"
    }

    response = requests.request('GET', url, headers=headers, params=querystring)

    today_response = requests.get(today_url, headers=headers, params=today_querystring)
    
    # response = requests.get(url, headers=headers, params=querystring)
    print(response.status_code)
    # Check if the API call was successful
    if response.status_code == 200 or today_response.status_code == 200:
        # Convert the response content to JSON
        
        data = response.json()
        stages = data['Stages']
        
        t_data = today_response.json()
        today_data = t_data['Stages']
        
        for stage in stages:
            # print(stage.keys())
            competion_name = stage['CompN']
            events = stage['Events']
            # print('events', len(events))
            for row in events:
                # print(row.keys())
                # print(row['Esd'])
                event_date = row['Esd']
                event_year = int(str(event_date)[0:4])
                event_month = int(str(event_date)[4:6])
                event_day = int(str(event_date)[6:8])
                # print(event_year, 'ED',event_day, 'DTD',day, 'EM',event_month, 'DTM',month)
                
                if  event_year >= dt.year and event_month == dt.month :
                    Fixtures.append(row)
        print(Fixtures)    
        context = {
            'stages':stages,
            'today_data':today_data,
            'fixtures':Fixtures[0:25],
        }
        
        return render(request, 'soccer.html', context)        
    else:
        # If the API call failed, return the error message as a JSON response
        error_message = {'error': response.reason}
        return JsonResponse(error_message, status=response.status_code)
    
    favoured = FavouriteModel.objects.all()
    
    
    return render(request, 'soccer.html', {'jsonResponse': jsonResponse, 'favourite':favoured})



# def index(request):
#     dt = datetime.datetime.now()
#     Fixtures = []
#     template_name = 'soccer.html'
    
#     url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-league"

#     query_string_premier_league = {"Category":"soccer","Ccd":"england","Scd":"premier-league","Timezone":"-7"}

#     headers = {
#         "X-RapidAPI-Key": settings.API_KEY,
#         "X-RapidAPI-Host": "livescore6.p.rapidapi.com"
#     }

    
#     response = requests.get(url, headers=headers, params=query_string_premier_league)

    
#     # Check if the API call was successful
#     if response.status_code == 200:
#         # Convert the response content to JSON
#         data = response.json()
        
#         stages = data['Stages']
        
        
#         for stage in stages:
#             # print(stage.keys())
#             competion_name = stage['CompN']
#             events = stage['Events']
#             print('events', len(events))
#             for row in events:
#                 # print(row.keys())
#                 # print(row['Esd'])
#                 event_date = row['Esd']
#                 event_year = int(str(event_date)[0:4])
#                 event_month = int(str(event_date)[4:6])
#                 event_day = int(str(event_date)[6:8])
#                 # print(event_year, 'ED',event_day, 'DTD',dt.day, 'EM',event_month, 'DTM',dt.month)
                
#                 if  event_year >= dt.year and event_month == dt.month:
#                     if not event_day < dt.day:
#                         Fixtures.append(row)
#                 elif event_year >= dt.year and event_month > dt.month:
#                     Fixtures.append(row)
                
#         # print('Fixtures', Fixtures)
#         context = {
#             'stages':stages,
#             'fixtures':Fixtures[0:25],
#         }
#         return render(request, template_name, context)
#         # Return the data as a JSON response to the frontend
#     else:
#         # If the API call failed, return the error message as a JSON response
#         print('failed')
#         error_message = {'error': response.reason}
#         return JsonResponse(error_message, status=response.status_code)
  

def competion_events(request, league: str, stage: str):
    Results = []
    Fixtures = []
    template_name = 'competions.html'
    
    dt = datetime.datetime.now()
    print(dt.strftime('%Y-%m-%d'))
    datefmt = str(dt.year)+str(dt.month)+str(dt.day)
    
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-league"

    query_string = {"Category":"soccer","Ccd":league,"Scd":stage,"Timezone":"-7"}

    headers = {
        "X-RapidAPI-Key": settings.API_KEY,
        "X-RapidAPI-Host": "livescore6.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=query_string)
    
    # Check if the API call was successful
    if response.status_code == 200:
        # Convert the response content to JSON
        data = response.json()
        
        stages = data['Stages']
        
        for stage in stages:
            # print(stage.keys())
            competion_name = stage['CompN']
            stage_name = stage['Snm']
            events = stage['Events']
            # print('events', len(events))
            for row in events:
                # print(row.keys())
                # print(row['Esd'])
                event_date = row['Esd']
                event_year = int(str(event_date)[0:4])
                event_month = int(str(event_date)[4:6])
                event_day = int(str(event_date)[6:8])
                # print(event_year, 'ED',event_day, 'DTD',dt.day, 'EM',event_month, 'DTM',dt.month)
                
                if event_year < dt.year:
                    Results.append(row)
                elif event_year == dt.year and event_month < dt.month:
                    Results.append(row)
                elif event_year == dt.year and event_month == dt.month:
                    if event_day < dt.day:
                        Results.append(row)
                    else:
                        Fixtures.append(row) 
                elif  event_year >= dt.year and event_month > dt.month:
                    Fixtures.append(row)
                    
       
        favoured = FavouriteModel.objects.all()
        context={
            'stages':stages,
            'Fixtures':reversed(Fixtures),
            'Results':reversed(Results),
            'Fixtures':reversed(Fixtures),
            'Results':reversed(Results),
            'Competion_name':competion_name,
            'stage_name':stage_name,
            'favourite':favoured
        }
    else:
        favourite = FavouriteModel.objects.all()
        context={
            'Fixtures':reversed(Fixtures),
            'Results':reversed(Results),
            'Competion_name':"Null",
            'stage_name':"Null",
            'favourite':favourite
        }
    
    return render(request, template_name, context)


def league_events(request, country: str, league: str):
    Results = []
    Fixtures = []
    template_name = 'leagues.html'
    
    dt = datetime.datetime.now()
    print(dt.strftime('%Y-%m-%d'))
    datefmt = str(dt.year)+str(dt.month)+str(dt.day)
    
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-league"

    query_string = {"Category":"soccer","Ccd":country,"Scd":league,"Timezone":"-7"}

    headers = {
        "X-RapidAPI-Key": settings.API_KEY,
        "X-RapidAPI-Host": "livescore6.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=query_string)
    
    # Check if the API call was successful
    if response.status_code == 200:
        # Convert the response content to JSON
        data = response.json()
        
        stages = data['Stages']
        
        for stage in stages:
            # print(stage.keys())
            try:
                competion_name = stage['CompN']
            except:
                competion_name = stage['Snm']
            
            country_name = stage['Cnm']
                
            events = stage['Events']
            
            print('events', len(events))
            for row in events:
                # print(row.keys())
                # print(row['Esd'])
                event_date = row['Esd']
                event_year = int(str(event_date)[0:4])
                event_month = int(str(event_date)[4:6])
                event_day = int(str(event_date)[6:8])
                # print(event_year, 'ED',event_day, 'DTD',dt.day, 'EM',event_month, 'DTM',dt.month)
                
                if event_year < dt.year:
                    Results.append(row)
                elif event_year == dt.year and event_month < dt.month:
                    Results.append(row)
                elif event_year == dt.year and event_month == dt.month:
                    if event_day < dt.day:
                        Results.append(row)
                    else:
                        Fixtures.append(row) 
                elif  event_year >= dt.year and event_month > dt.month:
                    Fixtures.append(row)
                    
        # print('Fixtures', len(Fixtures))
        # print('Results', len(Results))
        
        context={
            'stages':stages,
            'Fixtures':reversed(Fixtures),
            'Results':reversed(Results),
            'Competion_name':competion_name,
            'country_name': country_name,
        }
    else:
        context={
            'Fixtures':reversed(Fixtures),
            'Results':reversed(Results),
            'Competion_name':"Null",
        }
    return render(request, template_name, context)


def live(request):
    ip = get_client_ip(request)
    
    favoured = FavouriteModel.objects.filter(owner__ip=ip)
    
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-live"

    querystring = {"Category":"soccer","Timezone":"-7"}

    headers = {
        "X-RapidAPI-Key": settings.API_KEY,
        "X-RapidAPI-Host": "livescore6.p.rapidapi.com"
    }

    
    response = requests.get(url, headers=headers, params=querystring)
    
    template_name = 'live.html'
    print(response.status_code)
    
    # Check if the API call was successful
    if response.status_code == 200:
        # Convert the response content to JSON
        data = response.json()
        
        stages = data['Stages']
        
        context = {
            'stages':stages,
            'liked':favoured
        }
        return render(request, template_name, context)
    else:
        # If the API call failed, return the error message as a JSON response
        error_message = {'error': response.reason}
        return JsonResponse(error_message, status=response.status_code)
    
    return render(request, 'soccer.html', {'jsonResponse': jsonResponse, 'liked':favoured})


def single_result(request, Eid: int):
    template_name = "single-result.html"
    print("EID", Eid)
    
    url = "https://livescore6.p.rapidapi.com/matches/v2/get-statistics"
    board_url = "https://livescore6.p.rapidapi.com/matches/v2/get-scoreboard"
    info_url = "https://livescore6.p.rapidapi.com/matches/v2/get-info"
    lineUps_url = "https://livescore6.p.rapidapi.com/matches/v2/get-lineups" 
    
    querystring = {"Category":"soccer","Eid":Eid}
    
    
    headers = {
        "X-RapidAPI-Key": settings.API_KEY,
        "X-RapidAPI-Host": "livescore6.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    board_response = requests.get(board_url, headers=headers, params=querystring)
    info_response = requests.get(info_url, headers=headers, params=querystring)
    lineUps_response = requests.get(lineUps_url, headers=headers, params=querystring)
    
    data = response.json()

    try:
        stat = data['Stat']
        pstat = data['PStat']
    except:
        stat = []
        pstat = []
    
    b_data = board_response.json()
    # print(b_data['Incs-s'])

    
    info_data = info_response.json()
    lineups_data = lineUps_response.json()
    
    context = {
        'info_data':info_data,
        'stat':stat,
        'pstat':pstat,
        'b_data':b_data,
        'incs_s':b_data['Incs-s'],
        'line_T1':lineups_data['Lu'][0]['Ps'],
        'line_T2':lineups_data['Lu'][1]['Ps']
    }
    return render(request, template_name, context)


def get_favourite(request):
    template_name =  "favourite.html"
    ip = get_client_ip(request)
    if not IpModel.objects.filter(ip=ip).exists():
        IpModel.objects.create(ip=ip)
    
    favoured = FavouriteModel.objects.filter(owner__ip=ip)
    print(favoured)
    
    list_favoured = []
    
    sc_url = "https://livescore6.p.rapidapi.com/matches/v2/get-scoreboard"
    
    
    for fav in favoured:
        print(fav, 'fav')
        querystring = {"Eid":fav,"Category":"soccer"}

        headers = {
            "X-RapidAPI-Key": settings.API_KEY,
            "X-RapidAPI-Host": "livescore6.p.rapidapi.com"
        }
        
        sc_response = requests.get(sc_url, headers=headers, params=querystring)
        
        
        sc_data = sc_response.json()
        list_favoured.append(sc_data)
        
        # print(sc_data,'sc_data')
        # print("!!!!!!!!!!!!------------------------!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        
        
    context = {
        'list_favoured':list_favoured
    }
    return render(request, template_name, context)


def favourite(request, eid):
    print(eid)
    ip = get_client_ip(request)
    if not IpModel.objects.filter(ip=ip).exists():
        IpModel.objects.create(ip=ip)
        
    favoured = FavouriteModel.objects.filter(Eid=eid).exists()
    if favoured:
        obj = FavouriteModel.objects.get(Eid=eid).delete()
    else:
        new = FavouriteModel.objects.create(Eid=eid)
        new.owner.add(IpModel.objects.get(ip=ip).id)
        new.save()
    
    return redirect(request.META.get('HTTP_REFERER'))# Redirects to the formal page or view
        
