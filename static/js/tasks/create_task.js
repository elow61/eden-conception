(function($) {
    'use strict';

    let formCreate = $('.form-create-task');

    /**
     * Open a modal to view the form create task
     */
    $('.create-task').on('click', function (e) {
        e.preventDefault();
        $(this).modal({fadeDuration: 250});
    })

    /**
     * Control the event submit form create task
     * to call function "createTask"
     */
    formCreate.submit(function (e) {
        let url = '/create_task/';
        e.preventDefault();
        createTask(url, $(this));
    });

    /**
     * Function to create a task with the submit form
     * @param {*} url 
     * @param {*} form 
     */
    window.createTask = function (url, form) {
        let datas = form.serializeArray()
        $('#create-task-in-' + datas[2]['value']).modal('hide');
        submitForm(url, form).then(response => {
            if (response.task_id) {
                let containerList = $('#project-list-' + response.list_id).find('.main-list');
                containerList.append(response.template);
            }
        })
    }

})(jQuery);