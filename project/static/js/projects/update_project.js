(function($) {
    'use strict';

    const buttonUpdate = $('#edit-project');
    
    buttonUpdate.on('click', function () {
        const projectId = $(this).attr('project-id');
        const url = '/' + projectId + '/update/'
        displayFormUpdateProject(url, projectId);
    })

        /**
     * Function to display the form update project and submit this.
     * @param {String} url to send the value in form update task
     * @param {String} projectId The id of current project to update this.
     * @returns the method ajax to send and update the project in database
     * 
     * Update too the next elements from the page "project/project_detail" : 
     * - The submit form update to send the informations and save in database
     */
    window.displayFormUpdateProject = function (url, projectId) {
        let csrfToken = getCookie('csrftoken');
        let data = {'project_id': projectId}
        
        return ajaxMethod(csrfToken, 'post', url, data).then(response => {
            const containerMain = $("#project-detail-" + response.project_id);
            const containerName = containerMain.find('.header-project-detail');
            containerName.children().css('display', 'none');
            containerName.css('display', 'block');
            
            containerName.append(response.template);

            $('#form-update-project').submit(function (e) {
                let url = '/update_project/';
                e.preventDefault();
                updateProject(url, $(this));
            });
        })
    }

    /**
     * Call in the function "displayFormUpdateTask"
     * when the user has clicked in "Save" button to update the current task
     * @param {String} url to send the information
     * @param {jQuery} form the form update task
     * The button update event is reload with the news DOM elements
     */
     window.updateProject = function (url, form) {
        submitForm(url, form).then(response => {

            const containerMain = $("#project-detail-" + response.project_id);
            containerMain.find('#form-update-project').remove();
            
            const containerName = containerMain.find('.header-project-detail');
            containerName.children().removeAttr('style');
            containerName.css('display', 'flex');
            containerName.find('h2').html(response.project_name);
            
            const projectNameList = $('.project-list');
            const projectName = projectNameList.find("h4[project-id='" + response.project_id + "']")
            projectName.html(response.project_name);
            
            projectName.on('click', function () {
                displayProjectDetails(response.project_id);
            })
            
            // Reload events
            const buttonUpdate = $('#edit-project');
            buttonUpdate.on('click', function () {
                const url = '/' + response.project_id + '/update/'
                displayFormUpdateProject(url, response.project_id);
            })
        })
    }

})(jQuery);