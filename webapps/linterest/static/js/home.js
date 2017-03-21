function createGroup() {
    console.log('prepare to create group.');
    var error = $("#group_error_place");
    error.html('');
    var type = $("#group_type_field");
    var city = $("#group_city_field");
    var start_time = $("#group_start_time_field");
    var end_time = $("#group_end_time_field");
    console.log(type.val())
    $.post("/linterest/leader", {type: type.val(), city: city.val(), start_time: start_time.val(), end_time: end_time.val()})
      .done(function(data) {
          if (data.form_error === "Create Group Successfully") {
            Materialize.toast("Created Group Scuccessfully!", 4000);
          } else {
            Materialize.toast("Create Group Failed! " + data.form_error, 4000);
          }
      });
}

function joinGroup() {
    console.log('prepare to join group.');
    var error = $("#group_error_place");
    error.html('');
    var type = $("#group_type_field");
    var city = $("#group_city_field");
    var start_time = $("#group_start_time_field");
    var end_time = $("#group_end_time_field");
    $.post("/linterest/init-search", {type: type.val(), city: city.val(), start_time: start_time.val(), end_time: end_time.val()})
      .done(function(data) {
          if (!data.form_error) {
            Materialize.toast("Joined Group Scuccessfully!", 4000);
          } else {
            Materialize.toast("Join Group Failed! " + data.form_error, 4000);
          }

          if (!data.form_error) {
              console.log('no error, valid search for groups');
              var type = data.type;
              var city = data.city;
              var start_time = data.start_time;
              var end_time = data.end_time;
              var event_string = type + city + start_time + end_time;
              console.log(encodeURI(event_string));
              window.location.replace("/linterest/search/" + type + "/" + city + "/" + start_time + "/" + end_time);
          }
      });
}

function createEvent() {
    console.log('prepare to create event.');
    var error = $("#error_place");
    var type = $("#type_field");
    var city = $("#city_field");
    var start_time = $("#start_time_field");
    var end_time = $("#end_time_field");
    $.post("/linterest/create-event", {type: type.val(), city: city.val(), start_time: start_time.val(), end_time: end_time.val()})
      .done(function(data) {
          if (data.form_error === "success") {
            Materialize.toast("Posted Event Scuccessfully!", 4000);
          } else {
            Materialize.toast("Post Event Failed! " + data.form_error, 4000);
          }
      });
}

function searchEvent(){
    console.log("prepare to post");
    var err_place = $("#error_place");
    err_place.html('');
    var type = $("#type_field");
    var city = $("#city_field");
    var start_time = $("#start_time_field");
    var end_time = $("#end_time_field");
    // var list = $("#event-list");
    $.post("/linterest/init-event-search", {type: type.val(), city: city.val(), start_time: start_time.val(), end_time: end_time.val()})
      .done(function(data) {
          console.log('return success');
          console.log(data.form_error);
          if (data.form_error === "success") {
            Materialize.toast("Searching Events", 4000);
          } else {
            Materialize.toast("Search Event Failed! " + data.form_error, 4000);
          }
        if (data.form_error === "success") {
            console.log('valid event');
            var type = data.type;
            var city = data.city;
            var start_time = data.start_time;
            var end_time = data.end_time;
            window.location.replace("/linterest/post/" + type + "/" + city + "/" + start_time + "/" + end_time);
        }
      });
}


$(document).ready(function () {
  // Add event-handlers
  $("#post-button").click(createEvent);
  $("#search-button").click(searchEvent);
  $("#create-group").click(createGroup);
  $("#join-group").click(joinGroup);
  $('.modal-trigger').leanModal();

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
