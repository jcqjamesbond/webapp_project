from django.shortcuts import render, redirect, get_object_or_404

from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# Needed to manually create HttpResponses or raise an Http404 exception
from django.http import HttpResponse, Http404

from linterest.models import *
from linterest.forms import *
from django.db import transaction

# Yelp API dependencies
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import io, json

from django.contrib.auth import login
from django.core.mail import send_mail

# for email confirmation
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse

@login_required
def home(request):
    context = dict()
    return render(request, 'home.html', context)

# this function handles the request for creating event in home page
@login_required
@transaction.atomic
def createEvent(request):
    dicts = dict()
    context = dict()
    # return to the page if this is a get request
    if request.method == "GET":
        context = {'form': EventForm()}
        return render(request, 'post.html', context)

    # encode the unicode strings to ascii and validate the form
    type=request.POST.get('type')
    city=request.POST.get('city')
    start_time=request.POST.get('start_time')
    end_time=request.POST.get('end_time')
    if type:
        dicts['type'] = type.encode('ascii', 'replace')
    if city:
        dicts['city'] = city.encode('ascii', 'replace')
    if start_time:
        dicts['start_time_text'] = start_time.encode('ascii', 'replace')
    if end_time:
        dicts['end_time_text'] = end_time.encode('ascii', 'replace')

    form = EventForm(dicts)
    if not form.is_valid():
        context['form'] = form
        context['form_error'] = form.cleaned_data['error']
        return render(request, 'init.json', context, content_type="application/json")

    # to find if there is a same event already exist in the DB. If so, we won't save this event.
    same_events = Event.objects.filter(user=request.user) \
        .filter(city=form.cleaned_data['city'].upper()) \
        .filter(type=form.cleaned_data['type']) \
        .filter(start_time=form.cleaned_data['start_time']) \
        .filter(end_time=form.cleaned_data['end_time'])

    # only save the event when there is not same events
    if not same_events:
        # save the new event
        new_event = Event(type=form.cleaned_data['type'], city=form.cleaned_data['city'].upper(), \
                          start_time=form.cleaned_data['start_time'], end_time=form.cleaned_data['end_time'], \
                          user=request.user)
        new_event.save()
        context['form_error'] = 'success'
    else:
        context['form_error'] = 'Same Event Created'
    return render(request, 'init.json', context, content_type="application/json")

# this function handles the request for searching events directly from home page
@login_required
@transaction.atomic
def initEventSearch(request):
    context = {}
    # return to the page if this is a get request
    if request.method == "GET":
        context = {'form': EventForm()}
        return render(request, 'home.html', context)

    # encode the unicode strings to ascii and validate the form
    dict = {}
    type=request.POST.get('type')
    city=request.POST.get('city')
    start_time=request.POST.get('start_time')
    end_time=request.POST.get('end_time')
    if type:
        dict['type'] = type.encode('ascii', 'replace')
    if city:
        dict['city'] = city.encode('ascii', 'replace')
    if start_time:
        dict['start_time_text'] = start_time.encode('ascii', 'replace')
    if end_time:
        dict['end_time_text'] = end_time.encode('ascii', 'replace')

    form = EventForm(dict)
    if not form.is_valid():
        context['form'] = form
        context['form_error'] = form.cleaned_data['error']
        return render(request, 'init.json', context, content_type="application/json")
    context['type'] = dict['type']
    context['city'] = dict['city']
    context['start_time'] = dict['start_time_text']
    context['end_time'] = dict['end_time_text']
    context['form_error'] = "success"
    return render(request, 'init.json', context, content_type="application/json")

# redirect to post page with the valid search pair event request from home page
@login_required
@transaction.atomic
def populate(request, type, city, start_time, end_time):
    context = dict()
    context['type'] = type
    context['city'] = city
    context['start_time'] = start_time
    context['end_time'] = end_time
    return render(request, 'post.html', context)

# redirect to search groups page with the valid request from home page
@login_required
@transaction.atomic
def populateGroups(request, type, city, start_time, end_time):
    context = dict()
    context['type'] = type
    context['city'] = city
    context['start_time'] = start_time
    context['end_time'] = end_time
    return render(request, 'join.html', context)

@login_required
@transaction.atomic
def post(request):
    context = {}
    # return to the page if this is a get request
    if request.method == "GET":
        context = {'form':EventForm()}
        return render(request, 'post.html', context)
    # encode the unicode strings to ascii and validate the form
    dict = {}
    type=request.POST.get('type')
    city=request.POST.get('city')
    start_time=request.POST.get('start_time')
    end_time=request.POST.get('end_time')
    if type:
        dict['type'] = type.encode('ascii', 'replace')
    if city:
        dict['city'] = city.encode('ascii', 'replace')
    if start_time:
        dict['start_time_text'] = start_time.encode('ascii', 'replace')
    if end_time:
        dict['end_time_text'] = end_time.encode('ascii', 'replace')

    form = EventForm(dict)
    if not form.is_valid():
        context['form'] = form
        context['form_error'] = form.cleaned_data['error']
        return render(request, 'error.json', context, content_type="application/json")
    # filter related events and return results in JSON
    events = Event.objects.filter(city=form.cleaned_data['city'].upper()) \
        .filter(type=form.cleaned_data['type']) \
        .filter(start_time__lt=form.cleaned_data['end_time']) \
        .filter(end_time__gt=form.cleaned_data['start_time']) \
        .exclude(user=request.user) \
        .exclude(is_active=False) \
        .order_by("-time")
    context['form'] = form
    context['events'] = events
    context['form_error'] = "success"
    return render(request, 'events.json', context, content_type='application/json')

@login_required
def profile(request, username):
    context = dict()
    # click_user = User.objects.get(username = username)
    try:
        click_user = get_object_or_404(User, username = username)
    except User.DoesNotExist:
        raise Http404("No model matches the given query.")
    # Get profile object
    print(click_user.username)
    # profile = Profile.objects.get(user = click_user)
    user_profile = get_object_or_404(Profile, user = click_user)
    context['gender'] = user_profile.gender
    context['age'] = user_profile.age
    context['phone'] = user_profile.phone
    context['bio'] = user_profile.bio
    context['click_user'] = click_user
    events = Event.objects.all()
    context["events"] = events
    context["user"] = click_user
    context['picture'] = user_profile.picture
    return render(request, 'profile.html', context)

@login_required
def edit_profile(request, username):
    context = dict()
    profile_to_edit = get_object_or_404(Profile, user=request.user)
    context['age'] = profile_to_edit.age
    context['gender'] = profile_to_edit.gender
    context['phone'] = profile_to_edit.phone
    context['bio'] = profile_to_edit.bio
    if request.method == "GET":
        form = ProfileForm(instance=profile_to_edit)
        context['form'] = form
        return render(request, 'edit_profile.html', context)

    form = ProfileForm(request.POST, request.FILES, instance=profile_to_edit)
    if not form.is_valid():
        context['form'] = form
        return render(request, 'edit_profile.html', context)
    form.save()
    print('save profile change')
    url = '/linterest/profile/' + request.user.username
    return redirect(url)

@login_required
def get_photo(request, username):
    click_user = User.objects.get(username = username)
    user = get_object_or_404(Profile, user = click_user)
    if not user.picture:
        raise Http404
    return HttpResponse(user.picture)

def register(request):
    context = dict()
    errors = []
    #Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'register.html', context)
    # Creates a bound form from the request POST parameters and makes the form
    # available in the request context dictionary
    form = RegistrationForm(request.POST)
    context['form'] = form
    # Validate the form
    if not form.is_valid():
        return render(request, 'register.html', context)
    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=request.POST.get('username'), \
                                        password=request.POST.get('password1'), \
                                        first_name = request.POST.get('firstname'), \
                                        last_name=request.POST.get('lastname'), \
                                        email=request.POST.get('email'), \
                                        is_active=False)
    new_user.save()
    # Create user profile model
    new_profile = Profile(user = new_user)
    new_profile.save()

    token = default_token_generator.make_token(new_user)

    email_subject = 'Linterest - Verify your email address'
    email_body="""
	Welcome to Linterest! Please click the link below to verify
	your email address and complete the registration of your account:
	http://%s%s
	""" % (request.get_host(),
           reverse('confirm', args=(new_user.username, token)))
    send_mail(email_subject, email_body,'no-reply@linterest.com',[new_user.email])
    return render(request,'loginwithconfirm.html', {'created': True})

def forgotpwd(request):
    context = {}

    if request.method == "GET":
        form = ForgetPasswordForm()
        return render(request,'forgetpassword.html',{'form':form})

    form = ForgetPasswordForm(request.POST)

    if not form.is_valid():
        context['form_error'] = form.cleaned_data['error']
        # return error JSON
        return render(request,'error.json', context, content_type="application/json")

    else:
        username=form.cleaned_data['username']
        user = User.objects.get(username=username)
        token = default_token_generator.make_token(user)
        body="""
			Please click the link below to verify your email address
			and complete the password resetting of your account:
			http://%s%s
			""" % (request.get_host(),
                   reverse('resetpassword', args=(user.username,token)))
        send_mail(
            subject="Linterest- Reset your password",
            message=body,
            from_email="no-reply@linterest.com",
            recipient_list=[user.email])
        context['form_error'] = "success"
        return render(request,'error.json', context, content_type="application/json")

def resetpassword(request,username,token):
    user = get_object_or_404(User,username = username)
    if not default_token_generator.check_token(user,token):
        raise Http404
    if request.method == "GET":
        form = PasswordResetForm()
        return render(request, 'resetpassword.html', {'form':form,'token':token,'username':username})
    form = PasswordResetForm(request.POST)
    if not form.is_valid():
        return render(request, 'resetpassword.html',{"form":form,'token':token,'username':username})

    password = form.cleaned_data['password1']
    user.set_password(password)
    user.save()
    return render(request, 'home.html', {})

def confirm(request, username, token):
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise Http404

    if not default_token_generator.check_token(user, token):
        raise Http404

    user.is_active=True
    user.save()

    # # Logs in the new user and redirects to mainpage
    login(request, user)
    return redirect('/linterest/')

# Returns all recent changes to the database, as JSON
@login_required
@transaction.atomic
def get_changes(request, time="1970-01-01T00:00+00:00"):
    if time == 'undefined' or time == '':
        time="1970-01-01T00:00+00:00"
    max_time = Event.get_max_time()
    events = Event.get_changes(time)
    context = {"max_time":max_time, "events":events}
    return render(request, 'events.json', context, content_type='application/json')

# Returns all recent changes of events to the database, as JSON
@login_required
@transaction.atomic
def get_changes_profile(request, username, time="1970-01-01T00:00+00:00"):
    if time == 'undefined' or time == '':
        time="1970-01-01T00:00+00:00"
    user = User.objects.get(username=username)
    max_time = Event.get_max_time_user(user)
    events = Event.get_changes_user(user, time)
    context = {"max_time":max_time, "events":events}
    return render(request, 'user_events.json', context, content_type='application/json')


# Returns all recent changes to the database, as JSON
@login_required
@transaction.atomic
def get_changes_message(request):
    time = request.POST.get('max_time', "1970-01-01T00:00+00:00")
    if time == 'undefined' or time == '':
        time="1970-01-01T00:00+00:00"
    try:
        event = Event.objects.get(id=request.POST.get('event_id'))
    except ObjectDoesNotExist:
        raise Http404

    try:
        chatroom = ChatRoom.objects.get(event=event)
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404
    # if this user is does not belong to the chatroom, redirect to homepage
    if not profile in chatroom.users.all():
        return redirect('/linterest/')
    max_time = Message.get_max_time(chatroom)
    messages = Message.get_changes(chatroom, time)
    context = {"max_time":max_time, "messages":messages}
    return render(request, 'messages.json', context, content_type='application/json')

# Returns all recent changes to the database, as JSON
@login_required
@transaction.atomic
def get_changes_message_group(request):
    time = request.POST.get('max_time', "1970-01-01T00:00+00:00")
    if time == 'undefined' or time == '':
        time="1970-01-01T00:00+00:00"
    try:
        group = Group.objects.get(id=request.POST.get('event_id'))
    except ObjectDoesNotExist:
        raise Http404

    try:
        chatroom = GroupChatRoom.objects.get(group=group)
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404

    # if this user is does not belong to the chatroom, redirect to homepage
    if not profile in chatroom.users.all():
        return redirect('/linterest/')
    max_time = GroupMessage.get_max_time(chatroom)
    messages = GroupMessage.get_changes(chatroom, time)
    context = {"max_time":max_time, "messages":messages}
    return render(request, 'messages.json', context, content_type='application/json')

# return all recent changes of groups to the database in JSON format
def get_groupchanges_profile(request, username, time="1970-01-01T00:00+00:00"):
    if time == 'undefined' or time == '':
        time="1970-01-01T00:00+00:00"
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise Http404

    max_time = Group.get_max_time_user(user)
    groups = Group.get_changes_user(user, time)
    context = {"max_time": max_time, "groups": groups}
    return render(request, 'user_groups.json', context, content_type='application/json')


# # Returns all recent changes to the database, as JSON
# @login_required
# @transaction.atomic
# def get_followers_changes(request, event_id, time="1970-01-01T00:00+00:00"):
#     if time == 'undefined':
#         time="1970-01-01T00:00+00:00"
#     max_time = Event.get_max_time_event(event_id)
#
#     followers = Event.get_followers_changes(event_id, time)
#     context = {"max_time":max_time, "followers":followers}
#     return render(request, 'followers.json', context, content_type='application/json')

# this function returns followers of certain event in JSON format in profile page
@login_required
@transaction.atomic
def get_followers(request, event_id):
    try:
        followers = Event.objects.get(id=event_id).followers.all()
    except ObjectDoesNotExist:
        raise Http404
    context = {"followers":followers}
    return render(request, 'followers.json', context, content_type='application/json')

# this function returns followers of certain group in JSON format in profile page
@login_required
@transaction.atomic
def get_group_followers(request, group_id):
    try:
        followers = Group.objects.get(id = group_id).followers.all()
    except ObjectDoesNotExist:
        raise Http404
    context = {"followers":followers}
    return render(request, 'followers.json', context, content_type='application/json')

# this function returns the followers of certain group in JSON format in slide page
@login_required
@transaction.atomic
def get_group_slide_followers(request, group_id):
    try:
        followers = Group.objects.get(id = group_id).followers.all()
        members = Group.objects.get(id = group_id).members.all()
    except ObjectDoesNotExist:
        raise Http404
    context = {"followers":followers, "members": members}
    return render(request, 'event_followers.json', context, content_type='application/json')

# this function returns the followers of certain event in JSON format in slide page
@login_required
@transaction.atomic
def get_event_slide_followers(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        members = Event.objects.get(id=event_id).member.all()
    except ObjectDoesNotExist:
        raise Http404
    followers = event.followers.all()
    context = {"followers":followers, "members": members}
    return render(request, 'event_followers.json', context, content_type='application/json')


# let the logged in user follow some event
@login_required
@transaction.atomic
def like(request, event_id):
    # Add the request user to the follower list of the event
    try:
        event = Event.objects.get(id=event_id)
    except ObjectDoesNotExist:
        raise Http404
    event.followers.add(Profile.objects.get(user=request.user));
    event.save()
    return HttpResponse("")
# this function makes the group creator accept the followers as memebers

@login_required
@transaction.atomic
def accept(request, username, group_id):
    # add the group follower into the member list of the group
    try:
        user = User.objects.get(username = username)
        current_group = Group.objects.get(id = group_id)
    except ObjectDoesNotExist:
        raise Http404
    current_group.members.add(Profile.objects.get(user = user))
    current_group.save()
    email_subject = 'Linterest - You have been accepted into a new group!'
    email_body = """Congratulations! You have been accepted to a new group(%s at %s Starts from:%s Ends:%s)
                    Please click the link below to access the recommendation page and chat room:
                    http://%s/linterest/group_recommendations/%s
                    """ % (current_group.type, current_group.city, current_group.start_time, current_group.end_time,
                           request.get_host(), group_id)
    send_mail(email_subject, email_body, 'no-reply@linterest.com', [user.email])
    return HttpResponse('')

# let the logged in user like back a follower to an event and match with him/her
@login_required
@transaction.atomic
def likeBack(request, username, event_id):
    # Add the request user to the follower list of the event
    try:
        user = User.objects.get(username=username)
        this_event = Event.objects.get(id=event_id)
    except ObjectDoesNotExist:
        raise Http404
    # Once there is a match, make the event inactive so that it won't be searched.
    print(user.email)
    if len(list(this_event.member.all())) < 1:
        try:
            this_event.member.add(Profile.objects.get(user = user))
        except ObjectDoesNotExist:
            raise Http404
        this_event.is_active=False
        this_event.save()
        # send email
        email_subject = 'Linterest - You have a new event match'
        email_body = """Congratulations! You have a new event match(%s at %s: Starts from: %s Ends: %s)
                        Please click the link below to access the recommendation page and chat room:
                        http://%s/linterest/group_recommendations/%s
                        """ % (this_event.type, this_event.city, this_event.start_time, this_event.end_time,
                               request.get_host(), event_id)
        send_mail(email_subject, email_body,'no-reply@linterest.com',[user.email])
        print(email_body)
    return HttpResponse("")

# this function handles the create group request
@login_required
@transaction.atomic
def leader(request):
    dicts = dict()
    context = dict()
    if request.method == 'GET':
        return render(request, 'leader.html', context)

    type=request.POST.get('type')
    city=request.POST.get('city')
    start_time=request.POST.get('start_time')
    end_time=request.POST.get('end_time')
    if type:
        dicts['type'] = type.encode('ascii', 'replace')
    if city:
        dicts['city'] = city.encode('ascii', 'replace')
    if start_time:
        dicts['start_time_text'] = start_time.encode('ascii', 'replace')
    if end_time:
        dicts['end_time_text'] = end_time.encode('ascii', 'replace')

    form = EventForm(dicts)
    if not form.is_valid():
        print('form invalid')
        # context['form'] = form
        context['form_error'] = form.cleaned_data['error']
        return render(request, 'init.json', context, content_type="application/json")
    # test if there is a same group in the database
    same_groups = Group.objects.filter(user=request.user) \
        .filter(city=form.cleaned_data['city'].upper()) \
        .filter(type=form.cleaned_data['type']) \
        .filter(start_time=form.cleaned_data['start_time']) \
        .filter(end_time=form.cleaned_data['end_time'])
    # only save the event when there is no same group
    if not same_groups:
        # save the new group
        new_group = Group(type=form.cleaned_data['type'], city=form.cleaned_data['city'].upper(), \
                          start_time=form.cleaned_data['start_time'], end_time=form.cleaned_data['end_time'], \
                          user=request.user)
        new_group.save()
        context['form_error'] = 'Create Group Successfully'
    else:
        context['form_error'] = 'Same Group Created'
    return render(request, 'init.json', context, content_type="application/json")

@login_required
@transaction.atomic
def join(request, group_id):
    context={}
    # Add the request user to the follower list of the event
    try:
        group = Group.objects.get(id=group_id)
    except ObjectDoesNotExist:
        context['form_error'] = "Group not found."
        return render(request,'error.json', context, content_type="application/json")

    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        raise Http404

    # if this user is already in the event's follower list
    if profile in group.followers.all():
        context['form_error'] = "You have already followed the group!"
        return render(request,'error.json', context, content_type="application/json")

    try:
        group.followers.add(Profile.objects.get(user=request.user))
    except ObjectDoesNotExist:
        raise Http404
    group.save()

    context['form_error'] = "success"
    return render(request,'error.json', context, content_type="application/json")


# let the logged in user follow some event
@login_required
@transaction.atomic
def like(request, event_id):
    context={}
    # Add the request user to the follower list of the event
    try:
        event = Event.objects.get(id=event_id)
    except ObjectDoesNotExist:
        context['form_error'] = "Event not found."
        return render(request,'error.json', context, content_type="application/json")

    profile = Profile.objects.get(user=request.user)

    # if this user is already in the event's follower list
    if profile in event.followers.all():
        context['form_error'] = "You have already followed the event!"
        return render(request,'error.json', context, content_type="application/json")

    event.followers.add(Profile.objects.get(user=request.user));
    event.save()

    context['form_error'] = "success"

    return render(request,'error.json', context, content_type="application/json")

# this function handles the initial join-group request in home page
@login_required
def initGroupSearch(request):
    context = dict()
    dicts = dict()
    if request.method == "GET":
        return render(request, 'join.html', {'form': EventForm()})

    type=request.POST.get('type')
    city=request.POST.get('city')
    start_time=request.POST.get('start_time')
    end_time=request.POST.get('end_time')
    if type:
        dicts['type'] = type.encode('ascii', 'replace')
    if city:
        dicts['city'] = city.encode('ascii', 'replace')
    if start_time:
        dicts['start_time_text'] = start_time.encode('ascii', 'replace')
    if end_time:
        dicts['end_time_text'] = end_time.encode('ascii', 'replace')

    form = EventForm(dicts)
    if not form.is_valid():
        # context['form'] = form
        context['form_error'] = form.cleaned_data['error']
        return render(request, 'init.json', context, content_type="application/json")
    context['type'] = dicts['type']
    context['city'] = dicts['city']
    context['start_time'] = dicts['start_time_text']
    context['end_time'] = dicts['end_time_text']
    return render(request, 'init.json', context, content_type="application/json")

# this function handles the request in join group page
@login_required
def search(request):
    context = {}
    if request.method == "GET":
        return render(request,'join.html',{'form':EventForm()})

    type=request.POST.get('type')
    city=request.POST.get('city')
    start_time=request.POST.get('start_time')
    end_time=request.POST.get('end_time')
    if type:
        context['type'] = type.encode('ascii', 'replace')
    if city:
        context['city'] = city.encode('ascii', 'replace')
    if start_time:
        context['start_time_text'] = start_time.encode('ascii', 'replace')
    if end_time:
        context['end_time_text'] = end_time.encode('ascii', 'replace')

    form = EventForm(context)
    if not form.is_valid():
        context['form'] = form
        context['form_error'] = form.cleaned_data['error']
        # return error JSON
        return render(request,'error.json', context, content_type="application/json")

    groups = Group.objects.filter(city=form.cleaned_data['city'].upper()) \
        .filter(type=form.cleaned_data['type']) \
        .filter(start_time__lt=form.cleaned_data['end_time']) \
        .filter(end_time__gt=form.cleaned_data['start_time']) \
        .exclude(user=request.user).order_by("-time")

    context['form'] = form
    context['groups'] = groups
    context['form_error'] = "success"
    print('filter groups')
    # return groups JSON
    return render(request, 'groups.json', context, content_type="application/json")

@login_required
def event_followers(request, event_id):
    context = {'event_id': event_id}
    return render(request, 'event_followers.html',context)

@login_required
def group_followers(request, group_id):
    context = {'group_id': group_id}

    return render(request, 'group_followers.html',context)

@login_required
def recommend(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except ObjectDoesNotExist:
        raise Http404


    context = {}
    print(request.user == event.user)
    print(request.user)
    print(event.user)
    print(event.followers.filter(user=request.user).exists())
    # for f in event.followers.get(username=event.user.username):
    #     print(f)

    # if the request user has no relation with the event, redirect to homepage
    if not (request.user == event.user or event.member.filter(user=request.user).exists()):
        return redirect('/linterest/')

    # create a new chatroom associated with event if not already exist
    try:
        chatroom = ChatRoom.objects.get(event=event)
    except ObjectDoesNotExist:
        # create a new chatroom w.r.t. the event if not already exist
        chatroom = ChatRoom(event=event)

        member = event.member;

        chatroom.users.add(Profile.objects.get(user=event.user))
        chatroom.users.add(member)

        chatroom.save()

    context["event_id"] = event_id
    context["user"] = request.user
    context["type"] = "event"

    with io.open('yelp_secret.json') as cred:
        creds = json.load(cred)
        auth = Oauth1Authenticator(**creds)
        client = Client(auth)
        params = {
            'term': event.type,
            'lang': 'en',
            'limit': 10,
        }
        print('prepare to search')
        try:
            response = client.search(event.city, **params)
        except:
            defaultCoordinate = [40.44, -79.99]
            context['latitude'] = defaultCoordinate[0]
            context['longitude'] = defaultCoordinate[1]
            context['error_message'] = 'Recommendations are unavailable in the given location'
            return render(request, 'recommend.html', context)
        print('search successfully')

        context['latitude'] = response.region.center.latitude
        context['longitude'] = response.region.center.longitude
        context['businesses'] = response.businesses
        return render(request, 'recommend.html', context)


@login_required
def group_recommend(request, event_id):
    try:
        event = Group.objects.get(id=event_id)
    except ObjectDoesNotExist:
        raise Http404

    context = {}

    # if the request user has no relation with the event, redirect to homepage
    if not (request.user == event.user or event.members.filter(user=request.user).exists()):
        return redirect('/linterest/')

    # create a new chatroom associated with event if not already exist
    try:
        chatroom = GroupChatRoom.objects.get(group=event)
    except ObjectDoesNotExist:
        # create a new chatroom w.r.t. the event if not already exist
        chatroom = GroupChatRoom(group=event)

        members = event.members.all();

        chatroom.users.add(Profile.objects.get(user=event.user))

        for member in members:
            chatroom.users.add(member)

        chatroom.save()

    context["event_id"] = event_id
    context["user"] = request.user
    context["type"] = "group"

    with io.open('yelp_secret.json') as cred:
        creds = json.load(cred)
        auth = Oauth1Authenticator(**creds)
        client = Client(auth)
        params = {
            'term': event.type,
            'lang': 'en',
            'limit': 10,
        }
        print('prepare to search')
        try:
            response = client.search(event.city, **params)
        except:
            defaultCoordinate = [40.44, -79.99]
            context['latitude'] = defaultCoordinate[0]
            context['longitude'] = defaultCoordinate[1]
            context['error_message'] = 'Recommendations are unavailable in the given location'
            return render(request, 'recommend.html', context)
        print('search successfully')

        context['latitude'] = response.region.center.latitude
        context['longitude'] = response.region.center.longitude
        context['businesses'] = response.businesses
        return render(request, 'recommend.html', context)


@login_required
def sendMessage(request):
    text = request.POST.get('message', "")

    if not request.POST.get('event_id'):
        return redirect('/linterest/')

    event_id = int(request.POST.get('event_id', "1"))

    try:
        room = ChatRoom.objects.get(event=Event.objects.get(id=event_id))
    except ObjectDoesNotExist:
        raise Http404

    message = Message(message=text, room=room, user=request.user)
    message.save()

    return HttpResponse("")

@login_required
def sendGroupMessage(request):
    text = request.POST.get('message', "")

    if not request.POST.get('event_id'):
        return redirect('/linterest/')

    event_id = int(request.POST.get('event_id', "1"))

    try:
        room = GroupChatRoom.objects.get(group=Group.objects.get(id=event_id))
    except ObjectDoesNotExist:
        raise Http404

    message = GroupMessage(message=text, room=room, user=request.user)
    message.save()

    return HttpResponse("")
