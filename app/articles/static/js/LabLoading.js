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

const Pending = 'pending',
    Running = 'running',
    Success = 'success',
    Canceled = 'canceled',
    Failed = 'failed';


(function poll() {
    const max_retries = 10;
    let elem = document.getElementsByClassName('task-status')[0];
    let lab_desc = document.getElementById('lab-description');
    if (elem == null) {
        return;
    }
    let id = elem.getAttribute('id');
    let ids = id.split('_')
    let user_id = ids[0];
    let task_id = ids[1];
    let poller = setTimeout(function () {
        poll();
    }, 500000);
    let retries = 0;
    $.ajax({
        url: `/task_status/${user_id}&${task_id}`,
        type: "POST",
        success: function (resp) {
            let json = $.parseJSON(resp);
            if (lab_desc == null) {
                lab_desc = document.getElementById('lab-description');
            }
            switch (json['status']) {
                case Pending:
                    lab_desc.innerHTML = 'Задача в очереди на обработку...'
                    break;
                case Running:
                    retries += 1;
                    lab_desc.innerHTML = 'Запускаем скрипты инициализации...'
                    console.log(retries);
                    if (retries > max_retries)
                        console.log("stop polling");
                    clearTimeout(poller);
                    break;
                case Success:
                case Canceled:
                case Failed:
                    let spinner = document.getElementById(`lab-load-spin-${task_id}`);
                    spinner.style.display = 'none';
                    lab_desc.innerHTML = `Возникла ошибка при выполнении скриптов инициализации ЛР: ${json['exception']}`
            }
            clearTimeout(poller);
        },
        error: function (e) {
            console.log('something went wrong on server:', e)
        },
        complete: poller,
        timeout: 2000
    })
})();