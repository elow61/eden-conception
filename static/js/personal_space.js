(function($) {
    "use strict";

    const button = $('.personal_space');
    button.on('click', function () {
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

        if (!$('#container-add-member').hasClass('closed')) {
            $('#container-add-member').addClass('closed');
        }

        $('.element-dashboard').removeClass('is-height');
        $('#container-info-user').toggleClass('closed');
    })
    
})(jQuery);