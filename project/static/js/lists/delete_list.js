(function($) {
    'use strict';
    
    let formDelete = $('.form-delete-list');
    formDelete.submit(function (e) {
        let url = '/delete_list/'
        e.preventDefault();
        deleteList(url, $(this));
    })

    window.deleteList = function (url, form) {
        submitForm(url, form).then(response => {
            if (response.list_id) {
                $('#project-list-' + response.list_id).remove();
            }
        })
    }

})(jQuery);