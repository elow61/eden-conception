(function($) {
    'use strict';

    let formCreate = $('.form-create-task');

    // Open modal to create a task
    $('.create-task').on('click', function (e) {
        e.preventDefault();
        $(this).modal({fadeDuration: 250});
    })

    formCreate.submit(function (e) {
        let url = '/create_task/';
        e.preventDefault();
        createTask(url, $(this));
    });

    window.createTask = function (url, form) {
        submitForm(url, form).then(response => {
            if (response.task_id) {
                let containerList = $('#project-list-' + response.list_id).find('.main-list');
                containerList.append(response.template);
            }
        })
    }

})(jQuery);