
(function($) {
    "use strict";
    
    /**
     * Function call when you submit a form by ajax request
     * @param {String} url It's the url call to send the data in back
     * @param {jQuery} element It's the form element that will be submitted
     * @returns ajax method with next params : headers, method, url, data
     */
    window.submitForm = function(url, element) {
        const dataForm = element.serializeArray();
        let csrfToken;
        let data = {}

        $.each(dataForm, (i, v) => {
            if (v.name === 'csrfmiddlewaretoken') {
                csrfToken = v.value;
            } else {
                data[v.name] = v.value;
            }
        })
        // If no csrfToken in form
        if (csrfToken === undefined) {
            csrfToken = getCookie('csrftoken');
        }

        return ajaxMethod(csrfToken, 'post', url, data)
    }

    /**
     * Function to send datas in back to ajax request
     * @param {string} token It's the csrf token for protected requests
     * @param {string} method It's the used method (frequentely used 'POST')
     * @param {string} url It's the url called to send the datas
     * @param {json} data It's the datas send
     * @returns The datas into the backend Django
     */
    window.ajaxMethod = function (token, method, url, data) {
        return $.ajax({
            headers: {'X-CSRFToken': token},
            method: method,
            url: url,
            data: data,
        })
    }

    /**
     * Function to get a cookie already create
     * @param {string} name cookie's name
     * @returns the cookie's value
     */
    window.getCookie = function (name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Management modals
    let btnCreateTask = $('.create-task');
    btnCreateTask.on('click', function (e) {
        e.preventDefault();
        $(this).modal({fadeDuration: 250});
    })
})(jQuery);