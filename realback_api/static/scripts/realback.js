
/* Active update timers */
var intervalTimerIDs = [];

/**
 * Clear all update timers
 */
function clearIntervalTimers() {
    console.log(intervalTimerIDs);
    for (var i = 0; i < intervalTimerIDs.length; i++) {
        clearInterval(intervalTimerIDs[i]);
    }
    intervalTimerIDs = [];
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

/**
 * Append a topic to the topic list
 *
 * @param topic             The topic to be appended
 * @param topic_list        The list to append topic to
 * @param click_callback    Callback on clicking the topic item
 */
function appendTopicToList(topic, topic_list, click_callback) {
    var inside_div = $('<div>');
    inside_div.addClass('topic_indicator');
    inside_div.data({
        topic_id: topic.topic_id,
        topic_title: topic.topic_title,
        topic_order: topic.topic_order
    });
    inside_div.attr('title', topic.topic_title);
    inside_div.text(topic.topic_order + 1);
    // Register click event only if a callback is supplied
    if (typeof click_callback === 'function') {
        inside_div.click(click_callback);
    }

    var li_el = $('<li>');
    li_el.addClass('topic_li_element');
    li_el.append(inside_div);
    topic_list.append(li_el);
    return inside_div;
}

/**
 * Calculate left position of topic list to center selected topic
 *
 * @param current_width         Width of the list element
 * @param current_topic_index   Index of currently selected topic
 * @returns {number}            Left position
 */
function calculateTopicListPosition(current_width, current_topic_index) {
    // half of list element width subtracting half of selected topic div width subtracting
    // count of topics left of selected multiplied by width of non-selected topic elements
    return current_width / 2 - 41 - current_topic_index * 66;
}
