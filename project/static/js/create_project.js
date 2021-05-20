
(function($) {
    'use strict';

    let form = $('.form-create-project');

    let url = '/create_project/';
    form.submit((e) =>  {
        e.preventDefault();
        submitForm(url, form).then(response => {

            if (response.product) {
                // Management project name in list
                let projectName = $('<li><h4 project-id=' + response.product_id + '>' + response.product + '</h4></li>').hide();
                $('.container-create-project').toggleClass('closed');
                $('.project-list').append(projectName);
                projectName.show('normal');

                // Management project detail view
                const containerProjectDetail = $('.container-projects-details');
                containerProjectDetail.empty();
                containerProjectDetail.append(response.template);
                
                // Reload event in the new elements
                projectName.on('click', function () {
                    displayProjectDetails(response.product_id);
                })
            } else {
                console.log(response.error);
            }
        });
    });

    // Display the create project form
    const buttonToCreateProject = $('#btn-create-project');
    buttonToCreateProject.on('click', () => {
        $('.container-create-project').toggleClass('closed');
    });
})(jQuery);
