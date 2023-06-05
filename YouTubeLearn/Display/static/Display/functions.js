function ajaxRequest(method, url, data, dataType, callback) {
    $.ajax({
      type: method,
      url: url,
      data: data,
      dataType: dataType,
      beforeSend: function(xhr, settings) { // add this to set the CSRF token header
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      },
      success: function(response) {
        callback(null, response);
      },
      error: function(xhr, status, error) {
        callback(error, null);
      }
    });
  }

  // code to get cookie
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue + '; SameSite=None; Secure'; // add the SameSite and Secure attributes
  }

