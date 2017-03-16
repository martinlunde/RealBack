
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
                console.log(cookie);
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

/**
 * Get list of questions for lecture
 */
function getQuestions() {
    var api_url = '/lectures/' + $('#pinInput').val() + '/questions/';
    $.getJSON(api_url, function (data) {
        console.log(data);
        if (data.success) {
            // TODO Update question list
            // Empty list of existing questions
            $("#question_list").empty();
            // Add questions to list
            for (var i = 0; i < data.questions.length; i++) {
                var question = data.questions[i];
                var list_element = $("<li>");
                var upvote_button = $("<button>");
                var glyphicon_up = $("<span>");
                glyphicon_up.attr({
                    class: 'glyphicon glyphicon-menu-up glyph-upvote'
                });
                upvote_button.attr({
                    type: 'button',
                    class: 'upvote-button',
                    onclick: 'upvoteQuestion.call(this)',
                    value: question.question_id
                });
                upvote_button.append(glyphicon_up);
                upvote_button.append(question.question_votes);
                list_element.append(upvote_button);
                list_element.append('- ');
                list_element.append(question.question_text);
                $("#question_list").append(list_element);
            }
            markQuestion();
        }
    });
}
