(function($) {
    'use strict';
    
    let projectName = $('.project-list').find('h4');

    // Display project details
    projectName.on('click', function () {
        const projectId = parseInt($(this).attr('project-id'));
        displayProjectDetails(projectId);
    })

    window.displayProjectDetails = function(projectId) {
        const projectDetail = $('.project-detail');

        if (!$('.container-create-project').hasClass('closed')) {
            $('.container-create-project').addClass('closed');
        }

        $.each(projectDetail, (i) => {
            if (!$(projectDetail[i]).hasClass('d-none')) {

                $(projectDetail[i]).addClass('d-none');
            }
        })

        $('#project-detail-' + projectId).toggleClass('d-none');
    }
    
})(jQuery);