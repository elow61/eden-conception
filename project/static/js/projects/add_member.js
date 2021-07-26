(function($) {
    'use strict';

    let formAddMember = $('.form-add-member');
    let url = '/add_member/';

    /**
     * Submit the form to add a member into a project.
     */
     formAddMember.submit((e) =>  {
        e.preventDefault();
        submitForm(url, formAddMember).then(response => {
            console.log(response);
        });
    });

    /**
    * Event to display the form add member
    */
    const buttonAddMember = $('#btn-add-member');
    buttonAddMember.on('click', () => {
        const projectDetail = $('.project-detail');

        $.each(projectDetail, (i) => {
            hideElement($(projectDetail[i]), 'd-none');
            $('.element-dashboard').removeClass('is-height');
        })
        
        hideElement($('.container-projects-details'), 'd-none');
        hideElement($('#container-create-project'), 'closed');
        hideElement($('#container-info-user'), 'closed');
        hideElement($('#container-info-member'), 'closed');

        $('.element-dashboard').addClass('is-height');
        $('#container-add-member').toggleClass('closed');
    });
})(jQuery);