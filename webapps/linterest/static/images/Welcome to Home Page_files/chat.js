function populateList() {
    console.log("populating list");
    var username = $('#root').attr('username');
    $.post("/linterest/get-changes-message/", {event_id: $('#chat-field').attr("event_id")} )
      .done(function(data) {
          var list = $("#chat-field");
          getUpdates();
      });
}

function sendMessage(){
    var message = $("#submit_message").val();
    if (message == "") {
        return;
    }
    console.log("sending: " + message);
    console.log($('#chat-field').attr("event_id"));
    $.post("/linterest/sendMessage/", {message: message, event_id: $('#chat-field').attr("event_id")})
      .done(function(data) {
        console.log('message sent successfully');
        $("#submit_message").val("").focus();
      });
}


function getUpdates() {
    var list = $("#chat-field");
    var max_time = list.data("max-time");
    $.post("/linterest/get-changes-message/", {event_id: list.attr("event_id"), max_time: max_time})
      .done(function(data) {
          list.data('max-time', data['max-time']);
          // update the posts (prepend new posts to the current list)
          for (var i = 0; i < data.messages.length; i++) {
              var message = data.messages[i];
              var new_message_html = $(message.html);
              list.append(new_message_html);
          }
          console.log(list[0].scrollHeight);
          var l = $("#test-div");
          console.log(l[0].scrollHeight);
          console.log($(document).height());
          l.animate({ scrollTop: 10}, 1000);
//          list.animate({
//              scrollTop: list[0].scrollHeight
//            }, 1000);

      });
}




$(document).ready(function () {
  // Add event-handlers
  $("#send-button").click(sendMessage);

  $("#submit_message").keyup(function(event){
    if(event.keyCode == 13){
        $("#send-button").click();
    }
  });

   // chat box JS
    $(function(){
        $("#addClass").click(function () {
            $('#sidebar_secondary').addClass('popup-box-on');
        });

        $("#removeClass").click(function () {
            $('#sidebar_secondary').removeClass('popup-box-on');
        });
    })

//  $('.modal').modal();
  $('.modal-trigger').leanModal();

  // Periodically refresh list every 5 seconds
  window.setInterval(getUpdates, 1000);

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

  populateList();
});
