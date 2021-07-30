(function($) {
    'use strict';

    let form = $('.form-create-project');
    let url = '/create_project/';

    /**
     * Submit the form to create a new project.
     * After submit, reload events for the nextelements:
     * - Event to view a project detail when we click on the project name.
     * - The submit form to delete a project
     */
    form.submit((e) =>  {
        e.preventDefault();
        submitForm(url, form).then(response => {
            if (response.project_name) {
                // Management project name in list
                let projectName = $('<li><h4 project-id=' + response.project_id + '>' + response.project_name + '</h4></li>').hide();
                $('.container-create-project').toggleClass('closed');
                $('.project-list').append(projectName);
                projectName.show('normal');

                // Management project detail view
                const containerProjectDetail = $('.container-projects-details');
                containerProjectDetail.empty();
                containerProjectDetail.append(response.template);

                displayProjectDetails(response.project_id);
                
                // Reload events
                // $.getScript("/static/js/projects/project_detail.js");
                let projectNames = $('.project-list').find('h4');
                projectName.on('click', function () {
                    let collaboratorName = $('.member-list').find('h4');
            
                    $.each(projectNames, (i) => {
                        if ($(projectNames[i]).hasClass('selected')) {
                            $(projectNames[i]).removeClass('selected');
                        }
                    })
                    $.each(collaboratorName, (i) => {
                        if ($(collaboratorName[i]).hasClass('selected')) {
                            $(collaboratorName[i]).removeClass('selected');
                        }
                    })
                    $(this).find('h4').addClass('selected');
                    displayProjectDetails(response.project_id);
                })

                const buttonUpdate = containerProjectDetail.find('.edit-project > i');
                buttonUpdate.on('click', function () {
                    const projectId = $(this).attr('project-id');
                    const url = '/' + projectId + '/update_form/'
                    displayFormUpdateProject(url, projectId);
                })

                // Reload the add member form
                $('#container-add-member').empty();
                $('#container-add-member').append(response.template_add_member);
                $('#btn-add-member').off();
                $.getScript("/static/js/projects/add_member.js");

            } else {
                viewModal('#dash-modal', response.error);
            }
        }); 
    });

    /**
     * Event to display the form create project
     */
    const buttonToCreateProject = $('#btn-create-project');
    buttonToCreateProject.on('click', () => {
        const projectDetail = $('.project-detail');

        $.each(projectDetail, (i) => {
            hideElement($(projectDetail[i]), 'd-none');
        })

        hideElement($('.container-projects-details'), 'd-none')
        hideElement($('#container-add-member'), 'closed');
        hideElement($('#container-info-user'), 'closed');
        hideElement($('#container-info-member'), 'closed');

        $('.element-dashboard').addClass('is-height');
        $('.container-create-project').toggleClass('closed');
    });
})(jQuery);
