(function($) {
    'use strict';

    let formCreate = $('.form-create-task');

    formCreate.submit(function (e) {
        let url = '/create_task/';
        e.preventDefault();
        createTask(url, $(this));
    });

    window.createTask = function (url, form) {
        submitForm(url, form).then(response => {
            console.log('yooo')
            /**
             * response.task_name
             * response.task_id
             * response.list_id
             * response.template
             */
            if (response.task_id) {
                let containerList = $('#project-list-' + response.list_id).find('.main-list');
                containerList.append(response.template);
            }
        })
    }

})(jQuery);