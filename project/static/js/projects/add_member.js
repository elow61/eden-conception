(function($) {
    'use strict';

    let formAddMember = $('.form-add-member');
    let url = '/add_member/';

    /**
     * Submit the form to create a new project.
     * After submit, reload events for the nextelements:
     * - Event to view a project detail when we click on the project name.
     * - The submit form to delete a project
     */
     formAddMember.submit((e) =>  {
        e.preventDefault();
        submitForm(url, formAddMember).then(response => {

            if (response.user_name) {
                // Management project name in list
                // let projectName = $('<li><h4 project-id=' + response.project_id + '>' + response.project_name + '</h4></li>').hide();
                // $('.container-create-project').toggleClass('closed');
                // $('.project-list').append(projectName);
                // projectName.show('normal');

                // // Management project detail view
                // const containerProjectDetail = $('.container-projects-details');
                // containerProjectDetail.empty();
                // containerProjectDetail.append(response.template);
                
                // Reload event in the new elements
                console.log(response);
            } else {
                console.log(response.error);
            }
        });
    });

    /**
        * Event to display the form add member
        */
    const buttonAddMember = $('#btn-add-member');
    buttonAddMember.on('click', () => {
        const projectDetail = $('.project-detail');

        $.each(projectDetail, (i) => {
            if (!$(projectDetail[i]).hasClass('d-none')) {
                $(projectDetail[i]).addClass('d-none');
            }
        })

        if (!$('.container-projects-details').hasClass('d-none')) {
            $('.container-projects-details').addClass('d-none');
        }

        if (!$('#container-create-project').hasClass('closed')) {
            $('#container-create-project').addClass('closed');
        }

        $('#container-add-member').toggleClass('closed');
    });
})(jQuery);