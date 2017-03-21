function initMap() {
    var latField = $("#lat-field").val();
    var lngField = $("#lng-field").val();
    var center = {lat: parseFloat(latField), lng: parseFloat(lngField)};
    var businesses = $("#business-list");
    var all_business = businesses.children("div.well");

    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 11,
      center: center
    });

    var infowindow = new google.maps.InfoWindow();
    for (var i = 0; i < all_business.length; i ++) {
        var marker = new google.maps.Marker({
            position: {lat: parseFloat($(all_business[i]).attr("latitude")), lng: parseFloat($(all_business[i]).attr("longitude"))},
            map: map
        });
        // var addresses = $("#address-list");
        // var all_address = addresses.children("div.display");
        // for (var j = 0; j < all_address.length; j ++) {
        //     console.log($(all_address[j]).attr("address"));
        // }
        google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
                var img_src = $(all_business[i]).attr("img_src");
                var url = $(all_business[i]).attr("url");
                var name = $(all_business[i]).attr("name");
                var contentString = '<div><img src = ' + img_src + ' class = "business_picture">' +
                    '<div class = "post_content"><a href = ' + url + '>' + name + '</a></div>' + '</div>';
                infowindow.setContent(contentString);
                infowindow.open(map, marker);
            }
        })(marker, i));
    }
}


function populateList() {
    console.log("populating list");
    var username = $('#root').attr('username');

    var list = $("#chat-field");
    var group_or_event = list.attr("eog");
    if (group_or_event === "event") {
        var url = "/linterest/get-changes-message/";
    } else {
        var url = "/linterest/get-changes-message-group/";
    }

    $.post(url, {event_id: $('#chat-field').attr("event_id")} )
      .done(function(data) {
          getUpdates();
      });
}

function sendMessage(){
    var message = $("#submit_message").val();
    if (message == "") {
        return;
    }

    var list = $("#chat-field");
    var group_or_event = list.attr("eog");
    if (group_or_event === "event") {
        var url = "/linterest/sendMessage/";
    } else {
        var url = "/linterest/sendGroupMessage/";
    }
    console.log("sending: " + message);
    console.log($('#chat-field').attr("event_id"));
    $.post(url, {message: message, event_id: $('#chat-field').attr("event_id")})
      .done(function(data) {
        console.log('message sent successfully');
        $("#submit_message").val("").focus();

          // scroll down to bottom of chat field
            var chatbox = $('#chat');
            chatbox.scrollTop(chatbox[0].scrollHeight);
      });
}


function getUpdates() {
    var list = $("#chat-field");
    var max_time = list.data("max-time");
    var group_or_event = list.attr("eog");
    if (group_or_event === "event") {
        var url = "/linterest/get-changes-message/";
    } else {
        var url = "/linterest/get-changes-message-group/";
    }
    $.post(url, {event_id: list.attr("event_id"), max_time: max_time})
      .done(function(data) {
          list.data('max-time', data['max-time']);
          // update the posts (prepend new posts to the current list)
          console.log(data);
          console.log(data.messages);
          for (var i = 0; i < data.messages.length; i++) {
              var message = data.messages[i];
              var new_message_html = $(message.html);
              if (new_message_html.attr("username") === list.attr("username")) {
                new_message_html.addClass("chat_message_right");
              }
              list.append(new_message_html);
          }
          if (data.messages.length != 0) {
            // scroll down to bottom of chat field
            var chatbox = $('#chat');
            chatbox.scrollTop(chatbox[0].scrollHeight);
          }
      });
}


// chat box JS
    function initChat(){
        $("#addClass").click(function () {
            $('#sidebar_secondary').addClass('popup-box-on');
        });

        $("#removeClass").click(function () {
            $('#sidebar_secondary').removeClass('popup-box-on');
        });
    }

$(document).ready(function () {
  // Add event-handlers
  $("#send-button").click(sendMessage);
  initMap();
  initChat();

  $("#submit_message").keyup(function(event){
    if(event.keyCode == 13){
        $("#send-button").click();
    }
  });



//  $('.modal').modal();
  $('.modal-trigger').leanModal();

  // Periodically refresh list every 0.3 seconds
  window.setInterval(getUpdates, 300);

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


