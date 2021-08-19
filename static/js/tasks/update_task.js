(function($) {
    'use strict';

    const buttonUpdate = $('#update-task');
    
    buttonUpdate.on('click', function () {
        const taskId = $(this).attr('task-id');
        const url = '/' + taskId + '/update/'
        displayFormUpdateTask(url, taskId);
    })

    /**
     * Function to display the form update task and submit this.
     * @param {String} url to send the value in form update task
     * @param {String} taskId The id of current task to update this.
     * @returns the method ajax to send and update the task in database
     * 
     * Update too the next elements from the page "task/task_detail" : 
     * - button to cancel the update of current task
     * - The submit form update to send the informations and save in database
     * - The datepicker for the input deadline
     */
    window.displayFormUpdateTask = function (url, taskId) {
        let csrfToken = getCookie('csrftoken');
        let data = {'task_id': taskId}
        
        return ajaxMethod(csrfToken, 'post', url, data).then(response => {
            const containerMain = $('#main-task');
            const containerInfo = containerMain.find('.contain-header-info');
            containerInfo.css('display', 'none');
            
            containerMain.append(response.template);

            // Events with new DOM Elements
            $('#cancel-task').on('click', function (e) {
                e.preventDefault();
                cancelUpdateTask(containerInfo);
            })

            $('#delete-task').on('click', function () {
                const taskId = $(this).attr('task-id');
                const url = '/delete_task/'
                deleteTask(url, taskId);
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

            $('input[id*="created_at"]').datepicker({
                dateFormat: "dd/mm/yy",
            })
        })
    }


    window.getMessage = function (message) {
        $('#delete-task-modal').append('<p>' + message + '</p>');
        $('#delete-task-modal').modal('show');
        setTimeout(function () {
            $("#delete-task-modal").modal("hide");
        }, 3000);
    }

    /**
     * Function to cancel the updating current task
     * @param {jQuery} containerInfo is the div contains the information get in database
     * Show the template "task/task_detail.html" 
     */
    window.cancelUpdateTask = function (containerInfo) {
        $('.form-update-task').remove();
        containerInfo.css('display', 'block');
    }

    /**
     * Call in the function "displayFormUpdateTask"
     * when the user has clicked in "Save" button to update the current task
     * @param {String} url to send the information
     * @param {jQuery} form the form update task
     * The button update event is reload with the news DOM elements
     */
    window.updateTask = function (url, form) {
        submitForm(url, form).then(response => {

            if(response.error){
                let  htmlList = document.createElement('ul');
                $.each(response.error, (i, v) => {
                    let htmlLi = document.createElement('li');
                    htmlLi.append(i + ':' + v[0])
                    htmlList.append(htmlLi);
                })
                $('#task-modal').append(htmlList);
                $('#task-modal').modal('show');
                setTimeout(function () {
                    $("#task-modal").modal("hide");
                    $('.jquery-modal').hide();
                }, 5000);
            }

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

    /**
     * Events to control drag & drop
     */
    $('.js-list-sortable').sortable({
        connectWith: '#board',
    });
    $('.js-sortable').sortable({
        connectWith: '.main-list',
        stop: function (e, ui) {
            $('.container-project-task').updateOrderTask();
        }
    });

    /**
     * Function to update the tasks index into the database
     * @returns the news tasks index with ajax function
     */
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

    if (urlParam('success')) {
        getMessage('The task has been deleted');
    }
})(jQuery);
