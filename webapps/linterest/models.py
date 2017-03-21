from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models import Max

EVENT_TPYES = (
    ('Meal', 'Meal'),
    ('Movie', 'Movie'),
    ('Drink', 'Drink'),
    ('Party', 'Party'),
)

# users profile
class Profile(models.Model):
    gender = models.CharField(max_length=20, default='', blank=True)
    age = models.CharField(max_length=10, default = '', blank = True)
    bio = models.CharField(max_length=420, default="Write your short bio here.", blank = True)
    user = models.OneToOneField(User, primary_key=True)
    picture = models.ImageField(upload_to="profile_pictures", blank=True)
    phone = models.CharField(max_length=40, default = '', blank = True)
    def __str__(self):
        return self.user.username


    # Generates the HTML-representation of a single peofile item.
    @property
    def html(self):
        return render_to_string("user_profile.html", {"profile":self}).replace("\n", "");

    # Generates the HTML-representation of a single profile item in the follower selection page.
    @property
    def select_html(self):
        return render_to_string("event_follower.html", {"profile":self}).replace("\n", "");

    # Generates the HTML-representation of a single profile item in the follower selection page.
    @property
    def caption_html(self):
        return render_to_string("follower_info.html", {"profile":self}).replace("\n", "");

    # Generates the HTML-representation of member caption in the slide page.
    @property
    def member_caption_html(self):
        return render_to_string("member_info.html", {"profile":self}).replace("\n", "");

# events posted by users
class Event(models.Model):
    type = models.CharField(max_length=30, choices=EVENT_TPYES, default='meal')
    city = models.CharField(max_length=100, default='Pittsburgh')
    start_time = models.DateTimeField(null = True)
    end_time = models.DateTimeField(null = True)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True, null=True)  # time created
    last_changed = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    followers = models.ManyToManyField(
        Profile,
        related_name='following_event',
    )
    member = models.ManyToManyField(
        Profile,
        related_name='event_member',
    )

    @staticmethod
    def get_changes(changetime="1970-01-01T00:00+00:00"):
        return Event.objects.filter(last_changed__gt=changetime).distinct()

    @staticmethod
    def get_changes_user(user, changetime="1970-01-01T00:00+00:00"):
        return Event.objects.filter(last_changed__gt=changetime).filter(user=user).distinct()

    @staticmethod
    def get_max_time():
        return Event.objects.all().aggregate(Max('last_changed'))['last_changed__max'] or "1970-01-01T00:00+00:00"

    @staticmethod
    def get_max_time(id):
        return Event.objects.get(id=id).last_changed or "1970-01-01T00:00+00:00"

    @staticmethod
    def get_max_time_user(user):
        return Event.objects.filter(user=user).aggregate(Max('last_changed'))['last_changed__max'] or "1970-01-01T00:00+00:00"

    # Generates the HTML-representation of a single post item in post page.
    @property
    def html(self):
        profile = Profile.objects.get(user = self.user)
        return render_to_string("event.html", {"id":self.id,"user":self.user,"type":self.type,"time":self.time,"city":self.city,\
                                               "start_time":self.start_time,"end_time":self.end_time,"profile":profile})\
                                .replace("\n", "");

    # Generates the HTML-representation of a single post item in profile page.
    @property
    def user_html(self):
        profile = Profile.objects.get(user = self.user)
        return render_to_string("user_event.html", {"user":self.user,"type":self.type,"time":self.time,"city":self.city,\
                                               "start_time":self.start_time,"end_time":self.end_time,"event_id":self.id,"profile":profile})\
                                .replace("\n", "");

class Group(models.Model):
    type=models.CharField(max_length=30, choices=EVENT_TPYES, default='meal')
    city = models.CharField(max_length=100, default='Pittsburgh')
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    user = models.ForeignKey(User, related_name='user')
    time = models.DateTimeField(auto_now_add=True,null=True)
    last_changed = models.DateTimeField(auto_now=True)
    followers=models.ManyToManyField(Profile, related_name='follower')
    members = models.ManyToManyField(Profile, related_name='member')

    @staticmethod
    def get_changes(filter_rules, changetime="1970-01-01T00:00+00:00"):
        return Group.objects.filter(last_changed__gt=changetime).distinct()

    @staticmethod
    def get_changes_user(user, changetime="1970-01-01T00:00+00:00"):
        return Group.objects.filter(last_changed__gt=changetime).filter(user=user).distinct()

    @staticmethod
    def get_max_time():
        return Group.objects.all().aggregate(Max('last_changed'))['last_changed__max'] or "1970-01-01T00:00+00:00"

    @staticmethod
    def get_max_time_user(user):
        return Group.objects.filter(user=user).aggregate(Max('last_changed'))['last_changed__max'] or "1970-01-01T00:00+00:00"

    # Generates the HTML-representation of a single post item in profile page.
    @property
    def user_html(self):
        profile = Profile.objects.get(user = self.user)
        return render_to_string("user_group.html", {"group_id": self.id, "user": self.user, "type": self.type,
                                                    "time": self.time, "city": self.city, "start_time": self.start_time,
                                                    "end_time": self.end_time, "profile": profile}).replace("\n", "");

    # Generates the HTML-representation of a single post item in search group page.
    @property
    def html(self):
        profile = Profile.objects.get(user = self.user)
        return render_to_string("group.html", {"id":self.id,"user":self.user,"type":self.type,"time":self.time,"city":self.city,\
                                               "start_time":self.start_time,"end_time":self.end_time,"profile":profile})\
                                .replace("\n", "");

class ChatRoom(models.Model):
    event = models.OneToOneField(Event, primary_key=True)
    users = models.ManyToManyField(Profile, related_name='room_user')


class GroupChatRoom(models.Model):
    group = models.OneToOneField(Group, primary_key=True)
    users = models.ManyToManyField(Profile, related_name='group_room_user')

class Message(models.Model):
    room = models.ForeignKey(ChatRoom)
    user = models.ForeignKey(User, related_name="sender")
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True, null=True)  # time created

    @staticmethod
    def get_messages(chatroom):
        return Message.objects.filter(room=chatroom).distinct().order_by("time")

    @staticmethod
    def get_changes(chatroom, changetime="1970-01-01T00:00+00:00"):
        return Message.objects.filter(room=chatroom, time__gt=changetime).distinct().order_by("time")

    @staticmethod
    def get_max_time(chatroom):
        return Message.objects.filter(room=chatroom).aggregate(Max('time'))['time__max'] or "1970-01-01T00:00+00:00"

    @property
    def html(self):
        return render_to_string("message.html", {"self":self, "user":self.user}).replace("\n", "");

class GroupMessage(models.Model):
    room = models.ForeignKey(GroupChatRoom)
    user = models.ForeignKey(User, related_name="group_message")
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True, null=True)  # time created

    @staticmethod
    def get_messages(chatroom):
        return GroupMessage.objects.filter(room=chatroom).distinct().order_by("time")

    @staticmethod
    def get_changes(chatroom, changetime="1970-01-01T00:00+00:00"):
        return GroupMessage.objects.filter(room=chatroom, time__gt=changetime).distinct().order_by("time")

    @staticmethod
    def get_max_time(chatroom):
        return GroupMessage.objects.filter(room=chatroom).aggregate(Max('time'))['time__max'] or "1970-01-01T00:00+00:00"

    @property
    def html(self):
        return render_to_string("message.html", {"self":self, "user":self.user}).replace("\n", "");
