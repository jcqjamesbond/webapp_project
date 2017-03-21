function initSearch(){
    console.log('init search');
    var init_type = $("#init_type");
    // set default value in type select field
    $("#type_field").val(init_type.val());
    searchGroup();
}

function searchGroup() {
    console.log('start searching group');
    var err_place = $("#error_place");
    err_place.html('');
    var type = $("#type_field");
    var city = $("#city_field");
    var start_time = $("#start_time_field");
    var end_time = $("#end_time_field");
    var list = $("#group-list");
    console.log(city.val());
    $.post("/linterest/search", {type: type.val(), city: city.val(), start_time: start_time.val(), end_time: end_time.val()})
      .done(function(data) {
        console.log('return success');

        // error message
        if (data.form_error === "success") {
            if (data.groups.length == 0) {
                Materialize.toast("Oops! No Group found according to your filter rules!", 4000);
            } else {
                Materialize.toast("Searching Groups...", 2000);
            }

            // show search results
            list.empty();
            for (var i = 0; i < data.groups.length; i++) {
                var group = data.groups[i];
                var new_group = $(group.html);
                list.append(new_group);
            }
        } else {
            Materialize.toast("Search Group Failed! " + data.form_error, 4000);
        }


      });
}

function likeGroup(group_id) {
    $.post("/linterest/join/" + group_id, {})
      .done(function(data) {
        if (data.form_error === "success") {
            Materialize.toast("Followed Group Event Succesfully!", 4000);
          } else {
            Materialize.toast("Follow Group Event Failed! " + data.form_error, 4000);
        }
      });
}

$(document).ready(function () {
  // Add event-handlers
  $("#search-button").click(searchGroup);


  // Periodically refresh time every second
  //refreshTime()
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
    initSearch();
});
