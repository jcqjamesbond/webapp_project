function populateGroupList() {
    console.log('init group');
    var username = $('#root').attr('username');
    $.get("/linterest/get-groupchanges-profile/" + username)
      .done(function(data) {
          console.log('success get group profiles');
          var list = $("#group-list");
          list.data('max-time', data['max-time']);
          getGroupUpdates();
          console.log(data.groups);
          for (var i = 0; i < data.groups.length; i++) {
              group = data.groups[i];
              var new_group = $(group.html);
              list.prepend(new_group);
          }
      });
}

function getGroupUpdates() {
    var list = $("#group-list");
    var max_time = list.data("max-time");
    var username = $('#root').attr('username');
    $.get("/linterest/get-groupchanges-profile/" + username + "/" + max_time)
      .done(function(data) {
          list.data('max-time', data['max-time']);
          // update the posts (prepend new group to the current list)
          for (var i = 0; i < data.groups.length; i++) {
              var group = data.groups[i];
              var new_group = $(group.html);
              list.prepend(new_group);
          }
          // update the followers
          var all_groups = list.children("div.group-item");
          for (var j = 0; j < all_groups.length; j++) {
              group = all_groups[j];
              updateGroupFollowers(group.id);
          }
      });
}

function populateList() {
    var username = $('#root').attr('username');
    $.get("/linterest/get-changes-profile/" + username)
      .done(function(data) {
          var list = $("#event-list");
          getUpdates();
          for (var i = 0; i < data.events.length; i++) {
              event = data.events[i];
              var new_event = $(event.html);
              // new_event.data("event-id", event.id);
              list.prepend(new_event);
          }
      });
}

function getUpdates() {
    var list = $("#event-list");
    var max_time = list.data("max-time");
    var username = $('#root').attr('username');
    $.get("/linterest/get-changes-profile/" + username + "/" + max_time)
      .done(function(data) {
          list.data('max-time', data['max-time']);
          // update the posts (prepend new posts to the current list)
          for (var i = 0; i < data.events.length; i++) {
              var event = data.events[i];
              var new_event = $(event.html);
              list.prepend(new_event);
          }

          // update the followers
          var all_events = list.children("div.event-item");
          for (var j = 0; j < all_events.length; j++) {
              event = all_events[j];
              updateFollowers(event.id);
          }
      });
}

function updateFollowers(id) {
    var list = $("#follower-list" + id);
    var max_time = list.data("max-time");
    // console.log("update followers done");
    $.get("/linterest/get-followers/" + id)
      .done(function(data) {
          // console.log("get followers done");
          list.empty();
          for (var i = 0; i < data.followers.length; i++) {
              var follower = data.followers[i];
              var new_follower = $(follower.html);
              list.append(new_follower);
          }
      });
}

function updateGroupFollowers(id) {
    var list = $("#group-follower-list" + id);
    $.get("/linterest/get-group-followers/" + id)
      .done(function(data) {
          console.log("get group followers successfully");
          list.empty();
          for (var i = 0; i < data.followers.length; i++) {
              var follower = data.followers[i];
              var new_follower = $(follower.html);
              list.append(new_follower);
          }
      });
}

$(document).ready(function () {
  // Add event-handlers
  populateList();
  populateGroupList();
  // Periodically refresh to-do list every 5 seconds
  window.setInterval(getUpdates, 5000);
  window.setInterval(getGroupUpdates, 5000);

  // CSRF set-up copied from Django docs
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});
