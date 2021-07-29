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
            console.log(response)
            if(response.error){
                viewModal('#dash-modal', response.error);
            } else if (response.user_name) {
                let memberName = $('<li><h4 member-id=' + response.user_id + '>' + response.user_name + '</h4></li>').hide();
                $('.member-list').append(memberName);
                memberName.show('normal');

                $('#container-info-member').empty();
                $('#container-info-member').append(response.template);

                $.getScript("/static/js/personal_space.js");
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