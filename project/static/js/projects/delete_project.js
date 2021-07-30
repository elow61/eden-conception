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
            if (response.success) {
                $('#project-detail-' + response.project_id).remove();
                let projectList = $('.project-list').find('h4');

                for (let i = 0; i < projectList.length; i++) {
                    if (projectList[i].getAttribute('project-id') == response.project_id) {
                        projectList[i].remove();
                    }
                }

                if (response.remove_all_members) {
                    $('.member-list').empty();
                } else {
                    if (response.member_to_remove) {
                        for (let i=0; i < response.member_to_remove.length; i++) {
                            let memberName = $('.member-list').find('h4');
                            for (let j = 0; j < memberName.length; j++) {
                                if (memberName[j].getAttribute('member-id') == response.member_to_remove[i]) {
                                    memberName[j].remove();
                                }
                            }
                        }
                    }

                    // Update the member page information
                    $('#container-info-member').empty();
                    $('#container-info-member').append(response.template);
                    $.getScript("/static/js/personal_space.js");
                }

                // Reload the add member form
                $('#container-add-member').empty();
                $('#container-add-member').append(response.template_add_member);
                $('#btn-add-member').off();
                $.getScript("/static/js/projects/add_member.js");
                viewModal('#dash-modal', response.success);
            } else {
                viewModal('#dash-modal', response.error);
            }
        })
    }
})(jQuery);