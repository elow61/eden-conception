(function($) {
    'use strict';

    const buttonUpdate = $('#update-task');
    
    buttonUpdate.on('click', function () {
        const taskId = $(this).attr('task-id');
        const url = '/' + taskId + '/update/'
        displayFormUpdateTask(url, taskId);
    })

    window.displayFormUpdateTask = function (url, taskId) {
        let csrfToken = getCookie('csrftoken');
        let data = {'task_id': taskId}
        
        return ajaxMethod(csrfToken, 'post', url, data).then(response => {
            const containerMain = $('#main-task');
            const containerInfo = containerMain.find('.contain-header-info');
            containerInfo.css('display', 'none');
            
            containerMain.append(response.template);

            // Events with new DOM Elements
            const buttonCanceled = $('#cancel-task');
            buttonCanceled.on('click', function (e) {
                e.preventDefault();
                cancelUpdateTask(containerInfo);
            })

            $('#form-update-task').submit(function (e) {
                let url = '/update_task/';
                e.preventDefault();
                updateTask(url, $(this));
            });

            // Management calendar for input date
            $("#id_deadline").datepicker({
                dateFormat: "dd/mm/yy",
            });
        })
    }

    window.cancelUpdateTask = function (containerInfo) {
        $('.form-update-task').remove();
        containerInfo.css('display', 'block');
    }

    window.updateTask = function (url, form) {
        submitForm(url, form).then(response => {

            const containerMain = $('#main-task');
            containerMain.find('#form-update-task').remove();
            containerMain.find('.contain-header-info').remove();
            containerMain.append(response.template);

            // Reload events
            const buttonUpdate = $('#update-task');
            buttonUpdate.on('click', function () {
                const url = '/' + response.task_id + '/update/'
                displayFormUpdateTask(url, response.task_id);
            })
        })
    }

    // Manage drag & drop
    $('.js-list-sortable').sortable({
        connectWith: '#board',
    });
    $('.js-sortable').sortable({
        connectWith: '.main-list',
        stop: function (e, ui) {
            $('.container-project-task').updateOrderTask();
        }
    });

    $.fn.updateOrderTask = function () {
        let datas = {}
        let $elements = $(this);
        let csrfToken = getCookie('csrftoken');
        let infos = []
        
        $elements.each(function (e) {
            let currentTaskId = this.getAttribute('task-id');
            let listId = this.parentElement.getAttribute('list-id');

            let infoDict = {
                'task_id': currentTaskId,
                'list_id': listId,
                'index': e + 1,
            };
            infos.push(infoDict);

        })
        datas['datas'] = JSON.stringify(infos)

        return ajaxMethod(csrfToken, 'post', '/update_order_task/', datas);
    }

})(jQuery);
