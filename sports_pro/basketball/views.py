from django.shortcuts import render
from django.conf import settings
import datetime
import requests

# Create your views here.

def index(request):  # On the homepage the current day fixtures and results, group by competions
    dt = datetime.datetime.now()
    print(dt.strftime('%Y-%m-%d'))
    datefmt = str(dt.year)+str(dt.month)+str(dt.day)
    
    Fixtures = []  
    
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-league"    
    today_url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-date"
        
    querystring = {"Category":"basketball","Ccd":"nba","Scd":"play-offs","Timezone":"-7"}
    today_querystring = {"Category":"basketball","Date":datefmt,"Timezone":"-7"}

    headers = {
        "X-RapidAPI-Key": settings.API_KEY,
        "X-RapidAPI-Host": "livescore6.p.rapidapi.com"
    }

    response = requests.request('GET', url, headers=headers, params=querystring)

    today_response = requests.get(today_url, headers=headers, params=today_querystring)
    
    # response = requests.get(url, headers=headers, params=querystring)
    print(today_response.status_code)
    # Check if the API call was successful
    if response.status_code == 200 or today_response.status_code == 200:
        # Convert the response content to JSON
        
        data = response.json()
        stages = data['Stages']
        
        t_data = today_response.json()
        today_data = t_data['Stages']
        
        for stage in stages:
            # print(stage.keys())
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
                
                if  event_year >= dt.year and event_month == dt.month :
                    Fixtures.append(row)
            
        context = {
            'stages':stages,
            'today_data':today_data,
            'fixtures':Fixtures[0:25],
        }
        
        return render(request, 'basketball.html', context)        
    else:
        # If the API call failed, return the error message as a JSON response
        error_message = {'error': response.reason}
        return JsonResponse(error_message, status=response.status_code)
    
    return render(request, 'basketball.html', {'jsonResponse': jsonResponse})



def league_events(request, country: str, league: str):
    Results = []
    Fixtures = []
    template_name = 'basketball_leagues.html'
    
    dt = datetime.datetime.now()
    print(dt.strftime('%Y-%m-%d'))
    datefmt = str(dt.year)+str(dt.month)+str(dt.day)
    
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-league"

    query_string = {"Category":"basketball","Ccd":country,"Scd":league,"Timezone":"-7"}

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
        }
    else:
        context={
            'Fixtures':reversed(Fixtures),
            'Results':reversed(Results),
            'Competion_name':"Null",
        }
    return render(request, template_name, context)


def live(request):
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-live"

    querystring = {"Category":"basketball","Timezone":"-7"}

    headers = {
        "X-RapidAPI-Key": settings.API_KEY,
        "X-RapidAPI-Host": "livescore6.p.rapidapi.com"
    }

    
    response = requests.get(url, headers=headers, params=querystring)
    
    template_name = 'basketball_live.html'
    print(response.status_code)
    # Check if the API call was successful
    if response.status_code == 200:
        # Convert the response content to JSON
        data = response.json()
        
        stages = data['Stages']
        
        context = {
            'stages':stages,
        }
        return render(request, template_name, context)
    else:
        # If the API call failed, return the error message as a JSON response
        error_message = {'error': response.reason}
        return JsonResponse(error_message, status=response.status_code)
    
    return render(request, 'basketball.html', {'jsonResponse': jsonResponse})


def single_result(request, Eid: int):
    template_name = "basketball_single-result.html"
    print("EID", Eid)
    
    url = "https://livescore6.p.rapidapi.com/matches/v2/get-info"
    board_url = "https://livescore6.p.rapidapi.com/matches/v2/get-scoreboard"
    
    querystring = {"Category":"basketball","Eid":Eid}
    
    headers = {
        "X-RapidAPI-Key": settings.API_KEY,
        "X-RapidAPI-Host": "livescore6.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    board_response = requests.get(board_url, headers=headers, params=querystring)
    
    data = response.json()
    b_data = board_response.json()
    # print(b_data['Incs-s'])
    context = {
        'data':data,
        'b_data':b_data,
        
    }
    return render(request, template_name, context)

