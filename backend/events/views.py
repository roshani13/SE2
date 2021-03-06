from django.http import HttpResponse
from events.models import UserInfo, ReminderDetails, Notes, CreatedNotes, CreatedReminders
from django.db.models.query import QuerySet
import datetime
import pytz
import json


def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        user = data.get('email')
        try:
            user_details = UserInfo.objects.get(user_name=user)
        except UserInfo.DoesNotExist:
            return HttpResponse('User Not Registered', status='403')
        if user_details.password == data.get("password"):
            return HttpResponse(status='200')
        else:
            return HttpResponse('Wrong Password', status='403')
    else:
        return HttpResponse(status='404')


def register_user(request):
    ''' handle registration of users '''
    if request.method == "POST":

        """convert the request to simple dict format"""
        user_dict = json.loads(request.body.decode('utf-8'))
        user = user_dict.get('email')
        try:
            if get_user_details(user):
                return HttpResponse("User already exists", status='400')
        except UserInfo.DoesNotExist:
            pass
        try:
            user = UserInfo()
            user.user_name = user_dict['email']
            user.password = user_dict['password']
            user.save()
            return HttpResponse("Success", status='201')
        except Exception as e:
            return HttpResponse(e.args[0], status='400')
    else:
        return HttpResponse(status='404')


def add_note(request):
    '''create a note'''
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        try:

            note = Notes()
            note.title = data['title']
            note.description = data['description']
            note.save()
            note_id = note.id
        except Exception as e:
            print(e.args[0])
            return HttpResponse("Unable to add notes", status='400')
        try:
            user_details = get_user_details(data['user'])
            notes_details = get_notes_details(note_id)

            user_notes = CreatedNotes()
            user_notes.notes_id = notes_details
            user_notes.user_name = user_details
            user_notes.save()
            return HttpResponse("Success", status='201')
        except Exception as e:
            return HttpResponse(e.args[0], status='400')
    else:
        return HttpResponse(status='404')


def add_reminder(request):
    '''create a reminder'''
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        request_data = dict()
        request_data['date_time'] = data["date"]
        event_time = data["time"].split('.')[0]
        event_date = request_data['date_time'] + " " + event_time

        date_format = '%Y-%m-%d %H:%M:%S'

        unaware_date = datetime.datetime.strptime(
            event_date, date_format)
        request_data['date_time'] = pytz.utc.localize(unaware_date)

        try:
            reminder = ReminderDetails()
            reminder.title = data['title']
            reminder.description = data['description']
            reminder.date_time = request_data['date_time']
            reminder.save()
            reminder_id = reminder.id
        except Exception as e:
            print(e.args[0])
            return HttpResponse("Unable to add reminder", status='400')
        try:
            user_details = get_user_details(data['user'])
            reminder_details = get_reminder_details(reminder_id)

            user_reminders = CreatedReminders()
            user_reminders.reminder_id = reminder_details
            user_reminders.user_name = user_details
            user_reminders.save()
            return HttpResponse("Success", status='201')
        except Exception as e:
            return HttpResponse(e.args[0], status='400')
    else:
        return HttpResponse(status='404')


def get_dashboard_details(request):
    if request.method == "GET":
        try:
            user = dict(request.GET)['user'][0]
        except Exception as e:
            print(e.args[0])
            return HttpResponse("username is not present", status='404')
        reminders = get_user_created_reminders(user)
        notes = get_user_created_notes(user)
        response = dict()
        response["notes"] = notes
        response["reminders"] = reminders
        return HttpResponse(json.dumps(response), status='200')
    else:
        return HttpResponse(status='404')


def get_user_created_notes(user_name):
    try:
        user_created_notes_list = list()
        user_id = user_name
        notes_list = CreatedNotes.objects.filter(user_name_id=user_id).values()
        if not isinstance(notes_list, QuerySet):
            notes_list = [notes_list]

        for note in notes_list:
            user_created_notes_list.append(
                get_notes_details(note_id=note['notes_id_id'],
                get_values=True))
        return user_created_notes_list
    except UserInfo.DoesNotExist:
        return None


def get_user_created_reminders(user_name):
    try:
        user_created_reminders_list = list()
        user_id = user_name
        reminders_list = CreatedReminders.objects.filter(
            user_name_id=user_id).values()
        if not isinstance(reminders_list, QuerySet):
            reminders_list = [reminders_list]

        for reminder in reminders_list:
            user_created_reminders_list.append(
                get_reminder_details(reminder_id=reminder['reminder_id_id'],
                get_values=True))

        return user_created_reminders_list
    except UserInfo.DoesNotExist:
        return None


def get_notes_details(note_id, get_values=False):
    try:
        note_val =  Notes.objects.get(id=note_id)
        if get_values:
            note = dict()
            note['title'] = note_val.title
            note['description'] = note_val.description
            return note
        else:
            return note_val
    except Notes.DoesNotExist:
        return None


def get_reminder_details(reminder_id, get_values=False ):
    try:
        reminder_val =  ReminderDetails.objects.get(id=reminder_id)

        if get_values:
            reminder = dict()
            reminder['title'] = reminder_val.title
            reminder['description'] = reminder_val.description
            date_val  = str(reminder_val.date_time)
            reminder['date'] = date_val.split(' ')[0]
            reminder['time'] = date_val.split(' ')[1].split('+')[0]
            return reminder
        else:
            return reminder_val
    except ReminderDetails.DoesNotExist:
        return None


def get_user_details(user):
    try:
        return UserInfo.objects.get(user_name=user)
    except UserInfo.DoesNotExist:
        return None
