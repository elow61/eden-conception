(function($) {
    'use strict';

    const buttonUpdate = $('#delete-task');
    buttonUpdate.on('click', function () {
        const taskId = $(this).attr('task-id');
        const url = '/delete_task/'
        deleteTask(url, taskId);
    })

    window.deleteTask = function (url, taskId) {
        let csrfToken = getCookie('csrftoken');
        let data = {'task_id': taskId}
        
        return ajaxMethod(csrfToken, 'post', url, data).then(response => {
            if (response.success) {
                window.location.replace(window.location.origin + '/project-' + response.project_id + '/?success=1');
            } else {
                $('#task-modal').append('<p>' + response.error + '</p>');
                $('#task-modal').modal('show');
                setTimeout(function () {
                    $("#task-modal").modal("hide");
                }, 3000);
            }

        })
    }

})(jQuery);