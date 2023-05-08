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


$(document).ready(function () {
    let multi_select = $('.js-example-basic-multiple');
    let multi_select_parent = $('#multi-select');
    let form_group_linked_post = $("div[id=div_id_linked_post]")[0];

    if (!form_group_linked_post) {
        return;
    }
    multi_select.select2();

    form_group_linked_post.style.display = 'none'

    $("input[name=pinned]").change(function (e) {
        let elem = e.target;
        if (elem !== this) {
            elem = elem.parentNode;
        }
        if (elem.checked) {
            multi_select_parent[0].style.display = ''
        } else {
            multi_select_parent[0].style.display = 'none'
        }
        multi_select.select2({
            ajax: {
                delay: 1000,
                url: '/get_posts/',
                data: function (params) {
                    // Query parameters will be ?search=[term]&page=[page]
                    return {
                        search: params.term || '',
                        page: params.page || 1
                    };
                },
                processResults: function (data) {
                    if (data) {
                        return $.parseJSON(data);
                    }
                    return {results: []}
                },
                cache: true,
            },
            minimumInputLength: 3,
            maximumSelectionLength: 1
        });
    });

});


$(document).ready(function () {
    let form = $('#new_lab_form');
    if (!form[0]) {
        return;
    }
    let lab_btn = $('#new_lab_btn_save');
    lab_btn[0].addEventListener("click", function () {
        let multi_select = $('.js-example-basic-multiple');
        let linked_post = $("input[name=linked_post]")[0];

        if (multi_select[0].value != null) {
            linked_post.value = multi_select[0].value;
            lab_btn[0].setAttribute('type', 'submit')
        }
    })
})


