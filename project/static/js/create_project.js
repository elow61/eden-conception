
(function($) {
    'use strict';

    let form = $('.form-create-project');
    let url = '/create_project/';

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
    });

    // Display the create project form
    const buttonToCreateProject = $('#btn-create-project');
    buttonToCreateProject.on('click', () => {
        const projectDetail = $('.project-detail');

        $.each(projectDetail, (i) => {
            if (!$(projectDetail[i]).hasClass('d-none')) {

                $(projectDetail[i]).addClass('d-none');
            }
        })
        $('.container-create-project').toggleClass('closed');
    });

    // Delete project
    let urlDelete = '/delete_project/'
    let formDelete = $('.form-delete-project');

    formDelete.submit(function (e) {
        e.preventDefault();

        submitForm(urlDelete, $(this)).then(response => {
            if (response.list_id) {
                $('#project-list-' + response.list_id).remove();
            }
        })
    })
})(jQuery);
