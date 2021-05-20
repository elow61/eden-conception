
(function($) {
    "use strict";
    
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

        return $.ajax({
            headers: {'X-CSRFToken': csrfToken},
            method: 'POST',
            url: url,
            data: data,
        });
    }
})(jQuery);