console.log('Junior Journey is now using JS! exciting.');
console.log('GitHub is up to date.');

// function subscribe(pub_id, sub_id) {
//   console.log(`${pub_id} subscribed to ${sub_id}`);
// }

function subscribe(pub_id, sub_id) {
  console.log(`${pub_id} subscribed to ${sub_id}`);
  $.ajax({
    type: 'POST',
    url: '/subscriptions/subscribe/',
    data: {
      pub_id: pub_id,
      sub_id: sub_id,
      csrfmiddlewaretoken: getCookie('csrftoken'), // Fetch CSRF token
    },
    success: function (response) {
      if (response.status == 'success') {
        alert(response.message);
      } else {
        alert('Error: ' + response.message);
      }
    },
    error: function (xhr, errmsg, err) {
      alert('AJAX request failed: ' + errmsg);
    },
  });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function deleteApplication(id) {
  console.log(`delete application ${id}`);
  $.ajax({
    type: 'POST',
    url: '/applications/delete/',
    data: {
      application_id: id,
      csrfmiddlewaretoken: getCookie('csrftoken'), // Fetch CSRF token
    },
    success: function (response) {
      if (response.status == 'success') {
        alert(response.message);
      } else {
        alert('Error: ' + response.message);
      }
      location.reload();
    },
    error: function (xhr, errmsg, err) {
      alert('AJAX request failed: ' + errmsg);
      location.reload();
    },
  });
}
