from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .forms import addEventForm
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
import pymysql
import json

db = pymysql.connect(host='localhost', port=3306, user='root',
 passwd='nyj19971023', db='events_calendar')

def user_login(request):
    username = request.POST.get('Uname')
    password = request.POST.get('Pass')
    cursor = db.cursor()
    sql = "SELECT * FROM events_calendar.uname_pass;"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        if (username == str(row[0])) and (password == str(row[1])):
            request.session['user'] = username
            return redirect('index')
    request.session['note'] = 'Wrong username or password !'
    return redirect('login')


def valid_timeslot(request):
    timeslots = [1,2,3,4]
    username = request.GET.get('timeslot', None)
    data = {
        'is_taken': (int(username) in timeslots)
    }
    return JsonResponse(data)

# def submit_add_event(request):
#
#     # If this is a POST request then process the Form data
#     if request.method == 'POST':
#         # print('post')
#         event_list = ['1',]
#
#         # Create a form instance and populate it with data from the request (binding):
#         form = addEventForm(request.POST)
#         # print(form)
#         # Check if the form is valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
#             user = request.POST.get('user')
#             event = form.cleaned_data['event']
#             date = form.cleaned_data['date']
#             start = form.cleaned_data['start_time']
#             end = form.cleaned_data['end_time']
#             event_list.append({'event':event,'date': date,'start':start,'end':end})
#
#             start_time = datetime.datetime.combine(date, start).strftime("%Y-%m-%d, %H:%M:%S")
#             end_time = datetime.datetime.combine(date, end).strftime("%Y-%m-%d, %H:%M:%S")
#
#             cursor = db.cursor()
#
#             sql = "INSERT INTO user_event(user, event_title, start_time, end_time) VALUES ('%s', '%s', '%s', '%s')" % (user, event, start_time, end_time);
#             try:
#
#                 cursor.execute(sql)
#                 db.commit()
#             except:
#                 db.rollback()
#
#             print(event.__class__,start_time.__class__,end_time.__class__)
#             # redirect to a new URL:
#             return render(request, 'index.html', {'list': event_list})
#         # return render(request, 'index.html', {'form': form, 'list':event_list})
#
#     # If this is a GET (or any other method) create the default form.
#     else:
#         # print('get')
#         form = addEventForm(request.GET)
#         # print(form)
#         return render(request, 'index.html', {'form': form})
#
#     return render(request, 'index.html', )

def submit_add_event(request):

    user = request.POST.get('user')
    event = request.POST.get('event')
    start = request.POST.get('start')
    end = request.POST.get('end')


    cursor = db.cursor()

    sql1 = "SELECT * FROM user_event WHERE user='%s' AND start_time='%s'" % (user, start)

    if event and start and end:
        sql2 = "INSERT INTO user_event(user, event_title, start_time, end_time) VALUES ('%s', '%s', '%s', '%s')" % (
    user, event, start, end)
    elif start and event:
        sql2 = "INSERT INTO user_event(user, event_title, start_time, end_time) VALUES ('%s', '%s', '%s', '%s')" % (
    user, event, start, start)
    elif start and end:
        sql2= "INSERT INTO user_event(user, event_title, start_time, end_time) VALUES ('%s', '%s', '%s', '%s')" % (
    user, "unknown", start, end)
    elif start:
        sql2 = "INSERT INTO user_event(user, event_title, start_time, end_time) VALUES ('%s', '%s', '%s', '%s')" % (
    user, "unknown", start, start)

    result = False;
    try:
        cursor.execute(sql1)
        result = cursor.fetchall()
        db.commit()
    except:
        db.rollback()

    if not(result):
        try:
            cursor.execute(sql2)
            db.commit()
        except:
            db.rollback()
        return render(request, 'index.html', {'note': 'Successfully Add New Event !'})
    # redirect to a new URL:
    return render(request, 'index.html', {'note': 'An Event Already Exist At That Time !'})

def submit_edit_event(request):

    user = request.POST.get('user')
    event = request.POST.get('event')
    start = request.POST.get('start')
    end = request.POST.get('end')
    init_start = request.POST.get('init',None)

    # print(user)
    # print(event)
    # print(start)
    # print(end)
    # print(init_start)

    cursor = db.cursor()

    sql1 = "DELETE FROM user_event WHERE user='%s' AND start_time='%s'" % (user, init_start)

    sql2 = "INSERT INTO user_event(user, event_title, start_time, end_time) VALUES ('%s', '%s', '%s', '%s')" % (
        user, event, start, end);

    result={}
    try:
        cursor.execute(sql1)
        cursor.execute(sql2)
        db.commit()
        result['edit_note'] = "Successfully edited the event."
    except:
        db.rollback()
        result['edit_note'] = "Failed to edit the event!"

    # redirect to a new URL:
    return JsonResponse(result)

def submit_search_event(request):

    user = request.POST.get('user')
    key_word = request.POST.get('key_word')
    key_date = request.POST.get('key_date')

    if key_word and key_date:
        sql = "SELECT * FROM events_calendar.user_event WHERE user='"+user+"' AND event_title LIKE '%"+key_word+"%' AND (start_time LIKE '%"+key_date+"%' OR end_time LIKE '%"+key_date+"%')"
    elif key_word:
        sql = "SELECT * FROM events_calendar.user_event WHERE user='"+user+"' AND event_title LIKE '%"+key_word+"%'"
    elif key_date:
        sql = "SELECT * FROM events_calendar.user_event WHERE user='"+user+"' AND (start_time LIKE '%"+key_date+"%' OR end_time LIKE '%"+key_date+"%')"
    else:
        sql = "SELECT * FROM events_calendar.user_event WHERE user='%s'" % (user)

    cursor = db.cursor()

    data = {}
    result = False;
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        db.commit()
    except:
        db.rollback()

    if result:
        data['rows']= []
        for i in result:
            data['rows'].append({'user':i[0], 'event':i[1], 'start_time':i[2].strftime("%m/%d/%Y, %H:%M:%S"),'end_time':i[3].strftime("%m/%d/%Y, %H:%M:%S") })
    else:
        data['rows'] = ""
    # print('admit search event',data)

    if (not key_date) and (not key_word):
        data['search_note'] = 'Neither Key Date nor Key Word provided ! All events related to '+user+' was returned.'
        return JsonResponse(data)
        # return render(request, 'index.html', {'search_result': data, 'search_note':'Neither Key Date nor Key Word provided ! All events related to '+user+' was returned.'})
    else:
        data['search_note'] = ""
        return JsonResponse(data)
        # return render(request, 'index.html', {'search_result': json.loads(data)})
        # return redirect('/index/',search_result=data)
        # return HttpResponse('index.html',JsonResponse(data),content_type="application/json");

def submit_remove_event(request):

    user = request.POST.get('user')
    # event = request.POST.get('event')
    start = request.POST.get('start')
    # end = request.POST.get('end')

    cursor = db.cursor()

    sql1 = "DELETE FROM user_event WHERE user='%s' AND start_time='%s'" % (user, start)

    result={}
    try:
        cursor.execute(sql1)
        db.commit()
        result['remove_note'] = "Successfully removed the event."
    except:
        db.rollback()
        result['remove_note'] = "Failed to removed the event!"

    # redirect to a new URL:
    return JsonResponse(result)

def load_events(request):

    user = request.GET.get('user',None);
    data = {}

    cursor = db.cursor()

    sql = 'SELECT * FROM events_calendar.user_event WHERE user= "%s" AND start_time>="2021-01-01 00:00:00" AND start_time<"2021-02-01 00:00:00"' % (str(user));

    result = False;
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        db.commit()
    except:
        db.rollback()

    sql2 = "SELECT host FROM events_calendar.host_client_share WHERE client='%s'" % (user)

    try:
        cursor.execute(sql2)
        news = cursor.fetchall()
        db.commit()
    except:
        db.rollback()

    if news:
        data['news']= []
        for i in news:
            data['news'].append(i[0])
    else:
        data['news']=""

    if result:
        data['rows'] = []
        for i in result:
            data['rows'].append({'user':i[0], 'event':i[1], 'start':i[2].strftime("%m/%d/%Y, %H:%M:%S")[3:5], 'end':i[3].strftime("%m/%d/%Y, %H:%M:%S")[3:5], 'start_time':i[2],'end_time':i[3] })
        return JsonResponse(data)
    else:
        data['rows'] = '1'
        return JsonResponse(data)

def share_event(request):

    client = request.POST.get('client')
    host = request.POST.get('user')

    cursor = db.cursor()

    sql1 = "SELECT * FROM uname_pass WHERE username='%s'" % (client)

    try:
        cursor.execute(sql1)
        result = cursor.fetchall()
        db.commit()
    except:
        db.rollback()

    data = {}
    if not result:
        data['share_note'] = "Given username does not exist !"
        data['exit_code'] = 1
    else:
        sql2 = "INSERT INTO host_client_share (host,client) VALUE ('%s','%s')" % (host,client)
        try:
            cursor.execute(sql2)
            result = cursor.fetchall()
            data['share_note'] = "Successfully shared your calendar to "+client+"."
            data['exit_code'] = 0
            db.commit()
        except:
            data['share_note'] = "Error when sharing you calendar. Please try again!"
            data['exit_code'] = 1
            db.rollback()

    # redirect to a new URL:
    return JsonResponse(data)

def submit_share_event(request):

    user = request.GET.get('user')

    cursor = db.cursor()

    sql1 = "SELECT * FROM user_event WHERE user='%s'" % (user)

    result = {'rows':[],}
    try:
        cursor.execute(sql1)
        calendar = cursor.fetchall()
        db.commit()
    except:
        db.rollback()
        result['share_note'] = "Failed to fetch the calendar!"

    if calendar:
        result['share_note'] = ""
        for i in calendar:
            result['rows'].append({'user': i[0], 'event': i[1], 'start_time': i[2].strftime("%m/%d/%Y, %H:%M:%S"),
                                 'end_time': i[3].strftime("%m/%d/%Y, %H:%M:%S")})

    # redirect to a new URL:
    return JsonResponse(result)

def signup(request):

    username = request.POST.get('username')
    password = request.POST.get('password')

    cursor = db.cursor()

    sql1 = "SELECT * FROM uname_pass WHERE username='%s'" % (username)

    result = {}
    try:
        cursor.execute(sql1)
        duplicate = cursor.fetchall()
        db.commit()
    except:
        db.rollback()

    if duplicate:
        result['exit_note'] = 1
    else:
        sql2 = "INSERT INTO uname_pass (username, password) VALUE ('%s','%s')" % (username, password)
        try:
            cursor.execute(sql2)
            db.commit()
            result['exit_note'] = 0
        except:
            db.rollback()
            result['exit_note'] = 2

    # redirect to a new URL:
    return JsonResponse(result)