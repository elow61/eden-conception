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
                
                // Reload event in the new elements
                projectName.on('click', function () {
                    displayProjectDetails(response.project_id);
                })

            } else {
                console.log(response.error);
            }
        });
        form[0].reset();
    });

    /**
     * Event to display the form create project
     */
    const buttonToCreateProject = $('#btn-create-project');
    buttonToCreateProject.on('click', () => {
        const projectDetail = $('.project-detail');

        $.each(projectDetail, (i) => {
            if (!$(projectDetail[i]).hasClass('d-none')) {
                $(projectDetail[i]).addClass('d-none');
                $('.element-dashboard').addClass('is-height');
            }
        })
        if (!$('.container-projects-details').hasClass('d-none')) {
            $('.container-projects-details').addClass('d-none');
        }

        if (!$('#container-add-member').hasClass('closed')) {
            $('#container-add-member').addClass('closed');
        }

        $('.container-create-project').toggleClass('closed');
    });
})(jQuery);
