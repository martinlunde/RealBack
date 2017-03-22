
$(document).ready(function () {
    // Add click listeners
    $('#new_course_button').click(toggleShowCourseForm);
    $('#course_form_back').click(toggleShowCourseForm);
    $('#course_form_button').click(createCourse);

    updateCourseList();
});

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
        $('#course_form input').focus();
    } else {
        $('#course_form input').val('');
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
    // Set parameter default to false
    force_show = (typeof force_show !== 'undefined') ? force_show : false;

    click_context = $(click_context);
    var course_div = click_context.parent().parent();
    var lecture_list = course_div.children('ul');
    var glyph_span = click_context.children('span').first();

    if (force_show || ! lecture_list.is(':visible')) {
        lecture_list.show();
        glyph_span.removeClass('glyphicon-menu-down').addClass('glyphicon-menu-up');
        var course_id = course_div.data('course_id');
        updateLectureList(course_id, lecture_list);

    } else {
        lecture_list.hide();
        glyph_span.removeClass('glyphicon-menu-up').addClass('glyphicon-menu-down');
    }
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

    // Check if we have asked for permission
    if (course_div.data('delete_permission')) {
        // Go ahead and delete
        csrfDELETE('/courses/' + course_id + '/', function (data) {
            console.log(data);
            if (data.success) {
                updateCourseList();
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

var lecture_pin = '';

/**
 * Show the lecture page for a lecture
 *
 * `this` will be the clicked span element
 */
function showLecturePage() {
    lecture_pin = $(this).parent().data('lecture_pin');
    console.log(lecture_pin);

    // Show and hide elements
    $('#course_overview_page').hide();
    $('#lecture_page').show();

    // Get lecture
    populateLecturePage();
}

/**
 * Fill in contents in lecture page
 */
function populateLecturePage() {
    var URL = '/lectures/'+ lecture_pin + '/';

    $.getJSON(URL, function (data) {
        console.log(data);
        if (data.success) {
            $('#lecture_title').text(data.lecture.lecture_title);
            $('#lecture_pin').text(data.lecture.lecture_pin);
        }
    })

}

/**
 * Show the statistics page for a course
 */
function showStatPage() {
    var course_id = $(this).parent().parent().parent().data('course_id');
    $('#course_overview_page').hide();
    $('#stat_page').show();
    createCharts(course_id);
}

/**
 * Go back to course overview from lecture page or statistics page
 */
function backToCourseList() {
    $('#stat_page').hide();
    $('#lecture_page').hide();
    $('#course_overview_page').show();

    // Clear necessary data
    lecture_pin = '';
}
