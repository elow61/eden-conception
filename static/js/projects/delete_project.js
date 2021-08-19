(function($) {
    'use strict';

    // Event to delete project
    let formDelete = $('.form-delete-project');
    formDelete.submit(function (e) {
        let url = '/delete_project/';
        e.preventDefault();
        deleteProject(url, $(this));
    })

    /**
     * Function to delete a project
     * @param {string} url to send data into the back
     * @param {jQuery} form to submit project_id to delete this
     */
    window.deleteProject = function (url, form) {
        submitForm(url, form).then(response => {
            console.log(response)
            let projectList = $('.project-list').find('h4');
            if (response.project_id) {
                $('#project-detail-' + response.project_id).remove();

                for (let i = 0; i < projectList.length; i++) {
                    if (projectList[i].getAttribute('project-id') == response.project_id) {
                        projectList[i].remove();
                    }
                }
            }
        })
    }
})(jQuery);