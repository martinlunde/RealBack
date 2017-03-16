
$(document).ready(function () {
    // Add click listeners
    $('#new_course_button').click(toggleShowCourseForm);
    $('#course_form_back').click(toggleShowCourseForm);
    $('#course_form_button').click(createCourse);

    updateCourseList();
});

function toggleShowCourseForm() {
    var new_course_form = $('#course_form');
    var new_course_button = $('#new_course_button');
    // Toggle visibility
    new_course_form.toggle();
    new_course_button.toggle();
    if (new_course_form.is(':visible')) {
        $('#course_form input').focus();
        console.log('Focused on new course form input');
    } else {
        $('#course_form input').val('');
    }
}

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
                // Insert title after first glyph icon
                course_div.children('.glyphicon')[0].after(course.course_title);
                course_list_div.append(course_div);
            }
        }
    });
}

function createLecture() {
    var course_div = $(this).parent();
    var URL = '/courses/' + course_div.data('course_id') + '/lectures/';

    csrfPOST(URL, $("<form>"), function (data) {
        console.log(data);
        if (data.success) {
            // TODO update lecture list for this course
        }
    })
}

function toggleLectureList() {
    var course_div = $(this);
    var lecture_list = course_div.children('ul');
    var glyph_span = course_div.children('span').first();

    if (lecture_list.is(':visible')) {
        lecture_list.hide();
        glyph_span.removeClass('glyphicon-menu-down').addClass('glyphicon-menu-right');
    } else {
        lecture_list.show();
        glyph_span.removeClass('glyphicon-menu-right').addClass('glyphicon-menu-down');
    }

    console.log('Lecture list toggled');
}
