$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                let cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    let cookie = jQuery.trim(cookies[i]);
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

$(".newVote").click(function (e) {
    let elem = e.target;
    if (elem !== this) {
        elem = elem.parentNode;
    }
    let data_type = elem.getAttribute('data-type');
    let action = elem.getAttribute('data-action');
    let data_id = elem.getAttribute('data-id');
    let data_all = {'data_type': data_type, 'action': action,  'data_id': data_id};
    $.ajax({
            url: '/ajax/vote/',
            type: 'POST',
            data: data_all,
            success: function (response) {
                if (data_type === 'comment')
                    $('#voteComment' + data_id).html(response);
                else
                    $('#votePost' + data_id).html(response);
            },
            error: function () {
                alert(0)
            }
        }
    );
});
