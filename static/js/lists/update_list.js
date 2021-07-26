(function($) {
    'use strict';

    const buttonUpdate = $('.fa-pencil-alt');

    buttonUpdate.on('click', function () {
        console.log('coucou')
        const listId = $(this).attr('list-id');
        const url = '/' + listId + '/update_list_form/'
        displayFormUpdateList(url, listId);
    })

        /**
     * Function to display the form update list and submit this.
     * @param {String} url to send the value in form update list
     * @param {String} listId The id of current list to update this.
     * @returns the method ajax to send and update the list in database
     */
    window.displayFormUpdateList = function (url, listId) {
        let csrfToken = getCookie('csrftoken');
        let data = {'list_id': listId}
        console.log(data)
        return ajaxMethod(csrfToken, 'post', url, data).then(response => {
            const containerMain = $("#project-list-" + response.list_id);
            const containerName = containerMain.find('.header-list');
            containerName.children().css('display', 'none');
            containerName.append(response.template);

            $('#form-update-list').submit(function (e) {
                let url = '/update_list/';
                e.preventDefault();
                updateList(url, $(this));
            });
        })
    }

    /**
     * Call in the function "displayFormUpdateList"
     * when the user has clicked in "Save" button to update the current list
     * @param {String} url to send the information
     * @param {jQuery} form the form update list
     * The button update event is reload with the news DOM elements
     */
     window.updateList = function (url, form) {
        submitForm(url, form).then(response => {

            const containerMain = $("#project-list-" + response.list_id);
            const containerName = containerMain.find('.header-list');
            containerName.find('.form-update-list').remove();
           
            containerName.children().removeAttr('style');
            containerName.css('display', 'flex');
            containerName.find('h4').html(response.list_name);

            // Reload events
            const buttonUpdate = $('#edit-list');
            buttonUpdate.on('click', function () {
                const url = '/' + response.list_id + '/update/'
                displayFormUpdateList(url, response.list_id);
            })
        })
    }

})(jQuery);