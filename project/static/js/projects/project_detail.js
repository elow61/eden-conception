(function($) {
    'use strict';
    
    let projectName = $('.project-list').find('h4');

    /**
     * Event to call the function "displayProjectDetails"
     * to view the project detail
     */
    projectName.on('click', function () {
        const projectId = parseInt($(this).attr('project-id'));
        displayProjectDetails(projectId);
    })

    /**
     * Function to display the project's detail in the dashboard
     * @param {*} projectId The project id clicked
     */
    window.displayProjectDetails = function(projectId) {
        const projectDetail = $('.project-detail');
        const formCreateProject = $('.container-create-project');
        const containerProjectDetail = $('.container-projects-details');

        if (!formCreateProject.hasClass('closed')) {
            formCreateProject.addClass('closed');
        }

        $.each(projectDetail, (i) => {
            if (!$(projectDetail[i]).hasClass('d-none')) {
                $(projectDetail[i]).addClass('d-none');
            }
        })

        containerProjectDetail.removeClass('d-none');
        $('#project-detail-' + projectId).toggleClass('d-none');

        const formDelete = containerProjectDetail.find('#project-detail-' + projectId).find('.form-delete-project');
        formDelete.submit(function (e) {
            let url = '/delete_project/';
            e.preventDefault();
            deleteProject(url, $(this));
        })
    }
    
})(jQuery);