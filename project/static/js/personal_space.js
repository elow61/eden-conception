(function($) {
    "use strict";

    const button = $('.personal_space');
    button.on('click', function () {
        const projectDetail = $('.project-detail');

        $.each(projectDetail, (i) => {
            hideElement($(projectDetail[i]), 'd-none');
        })

        hideElement($('.container-projects-details'), 'd-none');
        hideElement($('#container-create-project'), 'closed');
        hideElement($('#container-add-member'), 'closed');
        hideElement($('#container-info-member'), 'closed');

        $('.element-dashboard').removeClass('is-height');
        $('#container-info-user').toggleClass('closed');
    })

    let collaboratorName = $('.member-list').find('h4');
    let projectName = $('.project-list').find('h4');

    collaboratorName.on('click', function () {
        const userId = $(this).attr('member-id');
        $.each(collaboratorName, (i) => {
            if ($(collaboratorName[i]).hasClass('selected')) {
                $(collaboratorName[i]).removeClass('selected');
            }
        })
        $.each(projectName, (i) => {
            if ($(projectName[i]).hasClass('selected')) {
                $(projectName[i]).removeClass('selected');
            }
        })
        $(this).addClass('selected');
        displayInfoCollaborator(userId);
    });

    window.displayInfoCollaborator = function (userId) {
        const projectDetail = $('.project-detail');
        const memberDetail = $('.member-detail');

        $.each(projectDetail, (i) => {
            hideElement($(projectDetail[i]), 'd-none');
        })
        $.each(memberDetail, (i) => {
            if (!$(memberDetail[i]).hasClass('d-none')) {
                $(memberDetail[i]).addClass('d-none');
            }
        })

        hideElement($('.container-projects-details'), 'd-none');
        hideElement($('#container-create-project'), 'closed');
        hideElement($('#container-add-member'), 'closed');
        hideElement($('#container-info-user'), 'closed');

        $('#member-detail-' + userId).toggleClass('d-none');
        $('.element-dashboard').removeClass('is-height');
        $('#container-info-member').removeClass('closed');
    }
    
})(jQuery);