(function($) {
    'use strict';

    const btnAddList = $('#btn-create-list');
    
    btnAddList.on('click', function () {
        $('.create-list').toggleClass('d-none');
    })

    let formCreate = $('.form-create-list');
    let url = '/create_list/'

    formCreate.submit((e) => {
        e.preventDefault();
        
        submitForm(url, form).then(response => {
            if (response.list_name) {
                const containerLists = $('.container-project-list');
                containerLists.append(response.template);
            }
        })
    })

    let urlDelete = '/delete_list/'
    let formDelete = $('.form-delete-list')
    formDelete.submit((e) => {
        e.preventDefault();

        submitForm(urlDelete, formDelete).then(response => {
            
        })
    })


})(jQuery);