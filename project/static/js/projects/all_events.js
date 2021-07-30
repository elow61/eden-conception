(function($) {
    'use strict';

    /**
     * 
     * In project_detail.js
     * 
     */

     /**
     * Event to call the function "displayProjectDetails"
     * to view the project detail
     */
    let projectName = $('.project-list').find('h4');
    projectName.on('click', function () {
        const projectId = parseInt($(this).attr('project-id'));
        let collaboratorName = $('.member-list').find('h4');

        $.each(projectName, (i) => {
            if ($(projectName[i]).hasClass('selected')) {
                $(projectName[i]).removeClass('selected');
            }
        })
        $.each(collaboratorName, (i) => {
            if ($(collaboratorName[i]).hasClass('selected')) {
                $(collaboratorName[i]).removeClass('selected');
            }
        })
        $(this).addClass('selected');
        displayProjectDetails(projectId);
    })

})(jQuery);