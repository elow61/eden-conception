(function($) {
    'use strict';

    /**
     * Event to display the form to create a list
     */
    const btnAddList = $('#btn-create-list');
    btnAddList.on('click', function () {
        $('.create-list').toggleClass('d-none');
    })

    /**
     * Control the event submit form create list
     * After the submit, reload the events for next elements :
     * - Form to delete a list
     * - Form to create a task
     * - Reload the drag & drop for the new list
     */
    let formCreate = $('.form-create-list');
    let url = '/create_list/'
    formCreate.submit((e) => {
        e.preventDefault();
        
        submitForm(url, formCreate).then(response => {
            if (response.list_name) {
                const containerLists = $('.container-project-list');
                containerLists.append(response.template);

                // Reload event with the new elements
                const formDelete = containerLists.find('#project-list-'+response.list_id).find('.form-delete-list');
                formDelete.submit(function (e) {
                    let url = '/delete_list/'
                    e.preventDefault();
                    deleteList(url, $(this));
                })

                const createTasks = containerLists.find('.create-task');
                const formCreate = containerLists.find('.form-create-task');
                createTasks.on('click', function (e) {
                    e.preventDefault();
                    $(this).modal({fadeDuration: 250});
                })
                formCreate.submit(function (e) {
                    let url = '/create_task/';
                    e.preventDefault();
                    createTask(url, $(this));
                });

                // Management drag & drop with the new list
                $('.js-sortable').sortable({
                    connectWith: '.main-list',
                    stop: function (e, ui) {
                        $('.container-project-task').updateOrderTask();
                    }
                });
            }
        })
    })
    formCreate[0].reset();

})(jQuery);