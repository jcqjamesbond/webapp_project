function sendEmail() {
    var username = $("#username").val();
    $.post("/linterest/forgotpwd", {username: username})
      .done(function(data) {
          if (data.form_error === "success") {
            Materialize.toast("An email has already been sent to your mailbox. Please check your email!", 4000);
          } else {
            Materialize.toast(data.form_error, 4000);
          }
      });
}


$(document).ready(function () {
  // Add event-handlers
  $("#send-button").click(sendEmail);

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
