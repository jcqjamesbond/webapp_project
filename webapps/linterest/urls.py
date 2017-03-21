from django.conf.urls import include, url
import django.contrib.auth.views
import linterest.views

urlpatterns = [
    url(r'^$', linterest.views.home, name = 'home'),
    # Route for built-in authentication with own custom login page
    url(r'^login$', django.contrib.auth.views.login, {'template_name':'login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', django.contrib.auth.views.logout_then_login, name='logout'),
    url(r'^register$', linterest.views.register, name = 'register'),
    # Route to User's profile
    url(r'^profile/(?P<username>\w+)$', linterest.views.profile, name = 'profile'),
    # Route to Edit profile
    url(r'^edit-profile/(?P<username>\w+)$', linterest.views.edit_profile, name = 'edit'),
    # Route to Post directly in home page
    url(r'^create-event$', linterest.views.createEvent),
    url(r'^init-event-search$', linterest.views.initEventSearch, name = 'init'),
    url(r'^post/(?P<type>\w+)/(?P<city>[\w\s]+)/(?P<start_time>.+)/(?P<end_time>.+)$', linterest.views.populate),
    # Route to post
    url(r'^post$', linterest.views.post, name = 'post'),
    url(r'^photo/(?P<username>\w+)$', linterest.views.get_photo, name = 'photo'),
    url(r'^like/(?P<event_id>\d+)$', linterest.views.like, name = 'like'),
    # Route to accept group followers
    url(r'^accept/(?P<username>\w+)/(?P<group_id>\d+)$', linterest.views.accept, name = 'likeBack'),
    # Route to pair the user
    url(r'^likeBack/(?P<username>\w+)/(?P<event_id>\d+)$', linterest.views.likeBack, name = 'likeBack'),
    url(r'^get-changes/(?P<time>.+)$', linterest.views.get_changes),
    url(r'^get-changes/?$', linterest.views.get_changes),
    # event and group in profile page
    url(r'^get-groupchanges-profile/(?P<username>\w+)/(?P<time>.+)$', linterest.views.get_groupchanges_profile),
    url(r'^get-groupchanges-profile/(?P<username>\w+)/?$', linterest.views.get_groupchanges_profile),
    url(r'^get-changes-profile/(?P<username>\w+)/(?P<time>.+)$', linterest.views.get_changes_profile),
    url(r'^get-changes-profile/(?P<username>\w+)/?$', linterest.views.get_changes_profile),
    # url(r'^get-followers-changes/(?P<time>.+)/(?P<event_id>\d+)$', linterest.views.get_followers_changes),
    # followers for both event and group
    url(r'^get-followers/(?P<event_id>\d+)$', linterest.views.get_followers),
    url(r'^get-group-followers/(?P<group_id>\d+)$', linterest.views.get_group_followers),
    # Route to recommendation page
    # url(r'^recommendations/$', linterest.views.recommend, name = 'recommend'),
    url(r'^recommendations/(?P<event_id>\d+)$', linterest.views.recommend, name = 'recommend'),
    url(r'^group_recommendations/(?P<event_id>\d+)$', linterest.views.group_recommend, name = 'group_recommend'),
    # forget password
    url(r'^forgotpwd$', linterest.views.forgotpwd, name = 'forgotpwd'),
    url(r'^confirm/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$',linterest.views.confirm, name='confirm'),
    url(r'^resetpassword/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$',linterest.views.resetpassword,name='resetpassword'),
    # Route to sliding page
    url(r'^group_followers/(?P<group_id>\d+)$', linterest.views.group_followers, name='group_followers'),
    url(r'^event_followers/(?P<event_id>\d+)$', linterest.views.event_followers, name='event_followers'),
    # Route to slide event's followers
    url(r'^get_event_followers/(?P<event_id>\d+)$', linterest.views.get_event_slide_followers, name='get_event_followers'),
    url(r'^get_group_slide_followers/(?P<group_id>\d+)$', linterest.views.get_group_slide_followers, name='get_event_followers'),
    url(r'^leader$', linterest.views.leader, name = 'leader'),
    url(r'^join/(?P<group_id>\d+)$', linterest.views.join, name = 'join'),
    # Route to search groups
    url(r'^search$', linterest.views.search, name = 'search'),
    url(r'^search/(?P<type>\w+)/(?P<city>[\w\s]+)/(?P<start_time>.+)/(?P<end_time>.+)$', linterest.views.populateGroups),
    url(r'^init-search$', linterest.views.initGroupSearch, name = 'init-search'),
    # Route to chat room
    # url(r'^chatroom/(?P<event_id>\d+)$', linterest.views.chatroom, name='chat'),

    url(r'^get-changes-message/$', linterest.views.get_changes_message),
    url(r'^get-changes-message-group/$', linterest.views.get_changes_message_group),
    url(r'^sendMessage/$', linterest.views.sendMessage),
    url(r'^sendGroupMessage/$', linterest.views.sendGroupMessage),
]
