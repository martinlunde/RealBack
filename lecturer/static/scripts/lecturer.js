
/* Document finished loading */
$(document).ready(function () {
    // Add click listeners
    $('#new_course_button').click(toggleShowCourseForm);
    $('#course_form_back').click(toggleShowCourseForm);
    $('#course_form_button').click(createCourse);
    $('#lecture_title').click(toggleLectureTitleForm);
    $('#cancel_change_lecture_title').click(toggleLectureTitleForm);
    $('#change_lecture_title_button').click(changeLectureTitle);
    $('#lecture_pin').click(blowUpLecturePin);
    $('#lecture_pin_large').click(blowUpLecturePin);

    // Back button manipulation
    window.onpopstate = function (event) {
        if ('state' in event && event.state.hasOwnProperty('callback')) {
            // console.log(event.state);
            viewStateCallbacks[event.state.callback]();
        }
    };

    updateCourseList();
});

/* Valid states for browser navigation */
var viewStateCallbacks = {
    'backToCourseList': backToCourseList,
    'forwardToLecturePage': forwardToLecturePage,
    'forwardToStatPage': forwardToStatPage
};

/**
 * Go back to course overview from lecture page or statistics page
 *
 * This must define a complete view state that can be pushed to browser history
 */
function backToCourseList() {
    $('#stat_page').hide();
    $('#lecture_page').hide();
    $('#course_overview_page').show();

    hideAllLectureLists();
    clearIntervalTimers();

    // Clear necessary data
    //lecture_pin = '';
}

/**
 * Navigate with the back button on the page
 */
function pageBackButton() {
    history.back();
}


/* --- Course list overview page related stuff --- */

/**
 * Toggle between showing new course button or new course form
 */
function toggleShowCourseForm() {
    var new_course_form = $('#course_form');
    var new_course_button = $('#new_course_button');
    // Toggle visibility
    new_course_form.toggle();
    new_course_button.toggle();
    if (new_course_form.is(':visible')) {
        $('#course_form input[name=title]').focus();
    } else {
        $('#course_form input[name=title]').val('');
    }
}

/**
 * Create a new course
 *
 * @param event     Submit event object
 */
function createCourse(event) {
    var form_action = '/courses/';
    var form = $('#course_form');

    csrfPOST(form_action, form, function (data) {
        console.log(data);
        if (data.success) {
            document.getElementById("course_error_message").innerHTML = ""
            toggleShowCourseForm();
            updateCourseList();
        }else if (data.message == "Course with this title already exists") {
            document.getElementById("course_error_message").innerHTML = "This course already exists"
        }else if (data.errors.title[0].slice(0, 43) == "Ensure this value has at least 3 characters") {
            document.getElementById("course_error_message").innerHTML = "Course name needs to be atleast 3 characters"
        }
    });

    event.preventDefault();
}

/**
 * Update list of courses
 */
function updateCourseList() {
    var URL = '/courses/';

    $.getJSON(URL, function (data) {
        console.log(data);
        if (data.success) {
            var course_list = data.courses;
            var course_list_div = $('#course_list');
            var prototype_course_div = $('#prototype_course_div');
            course_list_div.empty();

            for (var i = 0; i < course_list.length; i++) {
                var course = course_list[i];
                var course_div = prototype_course_div.clone();
                course_div.attr({
                    id: '',
                    style: ''
                });
                course_div.data('course_id', course.course_id);
                course_div.data('delete_permission', false);
                // Insert title after first glyph icon
                course_div.find('span').first().append(course.course_title);
                course_list_div.append(course_div);
            }
        }
    });
}

/**
 * Create a new lecture for a course
 *
 * `this` will be the button that called the function
 */
function createLecture() {
    var course_div = $(this).parent().parent().parent();
    var URL = '/courses/' + course_div.data('course_id') + '/lectures/';
    event.stopImmediatePropagation();

    csrfPOST(URL, $("<form>"), function (data) {
        console.log(data);
        if (data.success) {
            // TODO update lecture list for this course
            var context = course_div.find('span').first();
            toggleLectureList(context, true);
        }
    })
}

/**
 * Toggle visibility of the lecture list for a course and update list if it's not visible
 *
 * @param click_context       The element that called the function
 * @param force_show    Force lecture list to be shown and updated
 */
function toggleLectureList(click_context, force_show) {
    event.stopImmediatePropagation();
    // Set parameter default to false
    force_show = (typeof force_show !== 'undefined') ? force_show : false;

    click_context = $(click_context);
    var course_div = click_context.parent().parent();
    var lecture_list = course_div.children('ul');
    var glyph_span = click_context.children('span').first();
    var border_radius = course_div.children('div').first();

    if (force_show || ! lecture_list.is(':visible')) {
        // Hide all other lists first
        hideAllLectureLists();
        // Show the list we want to show
        lecture_list.show();
        glyph_span.removeClass('glyphicon-menu-right').addClass('glyphicon-menu-down');
        border_radius.addClass('bars-change-border-radius');
        var course_id = course_div.data('course_id');
        updateLectureList(course_id, lecture_list);

    } else {
        lecture_list.hide();
        glyph_span.removeClass('glyphicon-menu-down').addClass('glyphicon-menu-right');
        border_radius.removeClass('bars-change-border-radius');
    }
}

function toggleLectureListParent(click_context, force_show) {
    event.stopImmediatePropagation();
    toggleLectureList(jQuery(click_context).find(".wraptext"), force_show);
}

/**
 * Hide all the lecture lists from the course overview page
 */
function hideAllLectureLists() {
    $('#course_list > div > ul').hide();
    $('#course_list div.bars').removeClass('bars-change-border-radius');
    $('#course_list span.glyphicon-menu-down').removeClass('glyphicon-menu-down').addClass('glyphicon-menu-right');
}

/**
 * Populate the list of lectures for course with course_id
 *
 * @param course_id     ID of the course to get lectures for
 * @param lecture_ul    The list element to populate
 */
function updateLectureList(course_id, lecture_ul) {
    var URL = '/courses/' + course_id + '/lectures/';

    $.getJSON(URL, function (data) {
        console.log(data);
        if (data.success) {
            lecture_ul.empty();
            var prototype_li_el = $('#prototype_lecture_list li');
            for (var i = 0; i < data.lectures.length; i++) {
                var lecture = data.lectures[i];
                var li_element = prototype_li_el.clone();
                // Store PIN so we can get it when lecture is clicked
                li_element.data({
                    'lecture_pin': lecture.lecture_pin,
                    'delete_permission': false
                });
                li_element.children('span').first().text(lecture.lecture_title);
                lecture_ul.append(li_element);
            }
        }
    });
}

/**
 * Delete a course (with all its associated lectures)
 *
 * `this` will be the delete button
 */
function deleteCourse() {
    var course_div = $(this).parent().parent().parent();
    var course_id = course_div.data('course_id');
    event.stopImmediatePropagation();

    // Check if we have asked for permission
    if (course_div.data('delete_permission')) {
        // Go ahead and delete
        csrfDELETE('/courses/' + course_id + '/', function (data) {
            console.log(data);
            if (data.success) {
                course_div.remove();
            }
        });

    } else {
        // Ask for permission
        $(this).text('SURE?').css({
            'animation-name': 'warning_text',
            'animation-duration': '2s',
            'animation-iteration-count': 'infinite'
        });
        course_div.data('delete_permission', true);
    }
}

/**
 * Delete a lecture
 *
 * `this` will be the delete button
 */
function deleteLecture() {
    var lecture_el = $(this).parent();
    var lecture_pin = lecture_el.data('lecture_pin');
    event.stopImmediatePropagation();

    // Check if we have asked for permission
    if (lecture_el.data('delete_permission')) {
        // Go ahead and delete
        csrfDELETE('/lectures/' + lecture_pin + '/', function (data) {
            console.log(data);
            if (data.success) {
                // TODO update lecture list
                lecture_el.remove();
            }
        });

    } else {
        // Ask for permission
        $(this).text('SURE?').css({
            'animation-name': 'warning_text',
            'animation-duration': '2s',
            'animation-iteration-count': 'infinite'
        });
        lecture_el.data('delete_permission', true);
    }
}


/* --- Lecture page related stuff --- */

var lecture_pin = '';

/**
 * Show the lecture page for a lecture
 *
 * `this` will be the clicked element
 */
function showLecturePage() {
    lecture_pin = $(this).data('lecture_pin');
    console.log(lecture_pin);

    history.replaceState({callback: 'backToCourseList'}, 'Lecture');
    history.pushState({callback: 'forwardToLecturePage'}, 'Lecture');
    forwardToLecturePage();
    // Get lecture
    populateLecturePage();
}

/**
 * Navigate to lecture page
 *
 * This must define a complete view state that can be pushed to browser history
 */
function forwardToLecturePage() {
    // Show and hide elements
    $('#course_overview_page').hide();
    $('#stat_page').hide();
    $('#lecture_pin_large').hide();
    $('#lecture_page_body').show();
    $('#lecture_page').show();

    var timerID = setInterval(populateLecturePage, 2000);
    console.log(timerID);
    intervalTimerIDs.push(timerID);
}

/**
 * Fill in contents in lecture page
 */
function populateLecturePage() {
    var URL = '/lectures/'+ lecture_pin + '/';

    $.getJSON(URL, function (data) {
        console.log(data);
        if (data.success) {
            $('#lecture_title').children('h1').first().text(data.lecture.lecture_title).append(
                ' <span class="glyphicon glyphicon-edit glyph-align-with-text"></span>');

            if ($('#lecture_page_body').is(':visible')) {
                $('#lecture_pin').children('h2').first().text(data.lecture.lecture_pin).append(
                    ' <span class="glyphicon glyphicon-resize-full glyph-font-size-20"></span>');
            }
        }
    });
    populateRecentQuestionsLecturePage();
    populateTopQuestionsLecturePage();
    getPace();
}

/**
 * Fill recent in questions in lecture page
 */
function populateRecentQuestionsLecturePage() {
    var URL = '/lectures/'+ lecture_pin + '/questions/?order=latest';

    $.getJSON(URL, function (data) {
        console.log(data);
        if (data.success) {
          $("#question_list_recent").empty();
          for (var i = 0; i < data.questions.length; i++) {
              var question = data.questions[i];
              var list_element = $("<li>");
              list_element.append(' ' + question.question_text);
              $("#question_list_recent").append(list_element);
          }
        }
  });
}

/**
 * Fill in top questions in lecture page
 */
function populateTopQuestionsLecturePage() {
    var URL = '/lectures/'+ lecture_pin + '/questions/?order=votes';

    $.getJSON(URL, function (data) {
        console.log(data);
        if (data.success) {
          $("#question_list_top").empty();
          for (var i = 0; i < Math.min(5, data.questions.length); i++) {
              var question = data.questions[i];
              var list_element = $("<li>");
              list_element.append(' ' + question.question_text);
              $("#question_list_top").append(list_element);
          }
        }
  });
}

/**
 * Reset volume for lecture
 */
function lectureResetVolume() {
    var URL = '/lectures/'+ lecture_pin + '/reset/volume/';

    $.getJSON(URL, function (data) {
        console.log(data);
        if (data.success) {
          //do something
        }
  });
}

/**
 * Reset pace for lecture
 */
function lectureResetPace() {
    var URL = '/lectures/'+ lecture_pin + '/reset/pace/';

    $.getJSON(URL, function (data) {
        console.log(data);
        if (data.success) {
          //do something
        }
  });
}

/**
 * Update pace for lecture
 */
function getPace() {
    var URL = '/lectures/'+ lecture_pin + '/pace/';
    $.getJSON(URL, function (data) {
      console.log(data);
        if (data.success) {
            $('#pace_upvotes').empty()
            $('#pace_upvotes').append(data.lecture.lecture_pace_up)
            $('#pace_downvotes').empty()
            $('#pace_downvotes').append(data.lecture.lecture_pace_down)
        }
    })
}

/**
 * Show title form to edit lecture title
 */
function toggleLectureTitleForm() {
    var lecture_title = $('#lecture_title');
    var change_lecture_title_form = $('#change_lecture_title_form');
    var title_input = $('#change_lecture_title_form input[name=title]');

    if (lecture_title.is(':visible')) {
        lecture_title.hide();
        title_input.val(lecture_title.children('h1').first().text().trim());
        change_lecture_title_form.show();
        title_input.focus();
        title_input.attr('id', 'title_enter');
        title_input.addClass("form-control");

    } else {
        change_lecture_title_form.hide();
        change_lecture_title_form.children('input[name=title]').val('');
        lecture_title.show();
    }
}

/**
 * Submit change lecture title form
 */
function changeLectureTitle(event) {
    var action = '/lectures/' + lecture_pin + '/';
    var title_form = $('#change_lecture_title_form');

    csrfPOST(action, title_form, function (data) {
        console.log(data);
        if (data.success) {
            $('#lecture_title > h1').first().text(data.lecture.lecture_title).append(
                ' <span class="glyphicon glyphicon-edit glyph-align-with-text"></span>');
            toggleLectureTitleForm();
        }
    });
    event.preventDefault();
}

/**
 * Show lecture PIN in a large view
 */
function blowUpLecturePin() {
    var lecture_page_body = $('#lecture_page_body');
    var lecture_pin_large = $('#lecture_pin_large');

    if(lecture_page_body.is(':visible')) {
        lecture_page_body.hide();
        lecture_pin_large.show();
        $('#lecture_pin_large_text').text(lecture_pin);
        $('#lecture_pin > h2 > span.glyphicon').first().removeClass(
            'glyphicon-resize-full').addClass('glyphicon-resize-small');
    } else {
        lecture_page_body.show();
        lecture_pin_large.hide();
        $('#lecture_pin > h2 > span.glyphicon').first().removeClass(
            'glyphicon-resize-small').addClass('glyphicon-resize-full');
    }
}

/**
 * Toggle timer
 */
var time;
function updateDisplay() {
    var seconds, minute, hours;
    var value = $('#stopWatch').html();
    seconds = parseInt(value.split(':')[2]);
    minute = parseInt(value.split(':')[1]);
    hours = parseInt(value.split(':')[0]);
    seconds++;

    if(seconds<10){
        seconds = "0" + String(seconds);
    }
    if(minute<10){
        minute = "0" + String(minute);
    }
    if(hours<10){
        hours = "0" + String(hours)
    }
    if(seconds === 60){
        seconds = 0;
        minute++;
    }
    if(minute === 60){
        minute = 0;
        hours++;
    }
    seconds = String(seconds);
    minute = String(minute);
    hours = String(hours);
    time = hours + ":" + minute + ":" + seconds
    $('#stopWatch').html(time);
}

var stopTimer;
var timerToggle = false;
function timerController(){
    var URL = '/lectures/'+ lecture_pin + '/timer/';
    $.getJSON(URL, function (data) {
        if (data.success) {
            if(timerToggle == false){
                timerToggle = true;
                $('#timerToggleButton').html('END LECTURE');
                if(!data.active) {
                    var URL = '/lectures/' + lecture_pin + '/start_timer/';
                    $.getJSON(URL, function (data2) {
                        console.log(data2);
                    });
                    stopTimer = setInterval(updateDisplay, 1000);
                }
            }else{
                timerToggle = false;
                $('#timerToggleButton').html('START');

                var URL = '/lectures/'+ lecture_pin + '/stop_timer/';
                $.getJSON(URL, function (data2) {
                    console.log(data2);
                });
                clearInterval(stopTimer);
            }
        }
  });
}

/* --- Statistics page related stuff --- */

/**
 * Show the statistics page for a course
 */
function showStatPage() {
    event.stopImmediatePropagation();
    var course_id = $(this).parent().parent().parent().data('course_id');

    history.replaceState({callback: 'backToCourseList'}, 'Lecture');
    history.pushState({callback: 'forwardToStatPage'}, 'Lecture');
    forwardToStatPage();

    createCharts(course_id);
}

/**
 * Navigate to stats page
 *
 * This must define a complete view state that can be pushed to browser history
 */
function forwardToStatPage() {
    $('#lecture_page').hide();
    $('#course_overview_page').hide();
    $('#stat_page').show();
}
