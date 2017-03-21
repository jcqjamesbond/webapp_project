function initPost() {
    console.log('initing');
    var init_type = $("#init_type");
    // set default value in type select field
    $("#type_field").val(init_type.val());
    postEvent();
}

function postEvent(){
    var err_place = $("#error_place");
    err_place.html('');
    var type = $("#type_field");
    var city = $("#city_field");
    var start_time = $("#start_time_field");
    var end_time = $("#end_time_field");
    var list = $("#event-list");
    console.log(city.val());
    $.post("/linterest/post", {type: type.val(), city: city.val(), start_time: start_time.val(), end_time: end_time.val()})
      .done(function(data) {
        // toast errors
        if (data.form_error === "success") {
            Materialize.toast("Searching Events", 4000);
            // refresh list
            list.empty()
            for (var i = 0; i < data.events.length; i++) {
                var event = data.events[i];
                var new_event = $(event.html);
                list.append(new_event);
            }
          } else {
            Materialize.toast("Search Event Failed! " + data.form_error, 4000);
        }


      });
}

function likeEvent(post_id){
    $.post("/linterest/like/" + post_id, {})
      .done(function(data) {
        if (data.form_error === "success") {
            Materialize.toast("Followed Event Succesfully!", 4000);
          } else {
            Materialize.toast("Follow Event Failed! " + data.form_error, 4000);
        }

      });
}

$(document).ready(function () {
  // Add event-handlers
  $("#post-button").click(postEvent);


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
    initPost();
});
