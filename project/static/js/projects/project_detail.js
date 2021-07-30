(function($) {
    'use strict';

    let projectName = $('.project-list').find('h4');

    /**
     * Event to call the function "displayProjectDetails"
     * to view the project detail
     */
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

    /**
     * Function to display the project's detail in the dashboard
     * @param {*} projectId The project id clicked
     */
    window.displayProjectDetails = function(projectId) {
        const projectDetail = $('.project-detail');
        const containerProjectDetail = $('.container-projects-details');
        
        hideElement($('#container-info-member'), 'closed');
        hideElement($('#container-create-project'), 'closed');
        hideElement($('#container-add-member'), 'closed');
        hideElement($('#container-info-user'), 'closed');

        $.each(projectDetail, (i) => {
            if (!$(projectDetail[i]).hasClass('d-none')) {
                $(projectDetail[i]).addClass('d-none');
            }
        })

        containerProjectDetail.removeClass('d-none');
        $('.element-dashboard').removeClass('is-height');
        $('#project-detail-' + projectId).toggleClass('d-none');

        const formDelete = containerProjectDetail.find('#project-detail-' + projectId).find('.form-delete-project');
        formDelete.submit(function (e) {
            let url = '/delete_project/';
            e.preventDefault();
            deleteProject(url, $(this));
        })

        // Get the datas and Generate statistics for projects
        let csrfToken = getCookie('csrftoken');
        let datas = {'project_id': projectId};

        return ajaxMethod(csrfToken, 'post', '/get_statistics/', datas).then((response) => {
            console.log(' - I Get the stats - in project_detail.js ')
            get_stats(response.nb_task, datas['project_id']);
            get_time(response.time, datas['project_id']);
            get_history(response.history, datas['project_id']);
        })
    }

    /**
     * Method to view automatically the first project info in the dashboard
     * @returns a call AJAX to get and display the statistics of the current project
     */
    window.viewDashboard = function() {
        let containerProjects = $('.container-projects-details');
        const containerCreateProject = $('#container-create-project');
        const projectNameList = $('.project-list');

        if (containerProjects.children().length > 0) {
            containerCreateProject.addClass('closed');
            containerProjects.removeClass('d-none');
            containerProjects.children(':first').removeClass('d-none');
            $('.element-dashboard').removeClass('is-height');
            projectNameList.find('h4:first').addClass('selected');
            const projectId = projectNameList.find('h4:first').attr('project-id');

            // Get the datas and Generate statistics for projects
            let csrfToken = getCookie('csrftoken');
            let datas = {'project_id': projectId};

            return ajaxMethod(csrfToken, 'post', '/get_statistics/', datas).then((response) => {
                console.log(' - I Get the stats - in viewDashboard ')
                get_stats(response.nb_task, datas['project_id']);
                get_time(response.time, datas['project_id']);
                get_history(response.history, datas['project_id']);
            })
        }
    }
    
})(jQuery);