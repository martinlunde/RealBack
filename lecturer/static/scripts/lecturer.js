
$(document).ready(function () {
    // Add click listeners
    $('#new_course_button').click(toggleShowCourseForm);
    $('#course_form_button').click(createCourse);

    updateCourseList();
});

function toggleShowCourseForm() {
    var new_course_form = $('#course_form');
    // Toggle visibility
    new_course_form.toggle();
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
        toggleShowCourseForm();
        updateCourseList();
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
                    style: '',
                    value: course.course_id
                });
                course_div.prepend(course.course_title);
                course_list_div.append(course_div);
            }
        }
    });
}