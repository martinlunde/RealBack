
/**
 * Get details for lecture with PIN
 *
 * @param PIN       Lecture PIN
 * @param success   Function callback on received response
 */
function getLectureDetails(PIN, success) {
    var URL = '/lectures/' + PIN + '/';
    $.getJSON(URL, success);
}

/**
 * Find a cookie
 *
 * @param name  Name of the cookie to find
 * @return      Cookie value as string or null if cookie does not exist
 */
function getCookie(name) {
    var cookieVal = null;
    if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieVal = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieVal;
}

/**
 * POST a form with csrftoken header
 *
 * @param action    URL to post to
 * @param form_el   DOM form element to send
 * @param success   Function callback on received response
 */
function csrfPOST(action, form_el, success) {
    var csrftoken = getCookie("csrftoken");
    if (csrftoken === null) {
        console.log("CSRF cookie not found!");
        return;
    }
    $.ajax({
        url: action,
        type: "POST",
        headers: {"X-CSRFToken": csrftoken},
        data: form_el.serialize(),
        dataType: "json",
        success: success
    });
}

/**
 * DELETE something at URL
 *
 * @param URL       URL to item to delete
 * @param success   Function callback on received response
 */
function csrfDELETE(URL, success) {
    var csrftoken = getCookie("csrftoken");
    if (csrftoken === null) {
        console.log("CSRF cookie not found!");
        return;
    }
    $.ajax({
        url: URL,
        type: "DELETE",
        headers: {"X-CSRFToken": csrftoken},
        dataType: "json",
        success: success
    });
}
