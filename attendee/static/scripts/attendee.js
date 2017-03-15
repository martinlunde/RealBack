/**
 * Created by K on 15.03.2017.
 */

$(document).ready(function () {
    $('#landing_page').css("display", "none");
    $('#frontpage_attendee').css("display", "block");
    $('.footer').css("display", "block");
});

/**
 * Actions to perform after a lecture is joined
 */
function onJoin() {
    var PIN = $('#pinInput').val();
    getLectureDetails(PIN, function (json) {
        if (json.success == false) {
            $('#landing_page').css("display", "none");
            $('#frontpage_attendee').css("display", "block");
            $('.footer').css("display", "block");

        } else if (json.success == true) {
            $('#landing_page').css("display", "block");
            $('#frontpage_attendee').css("display", "none");
            $('.footer').css("display", "none");

            // Populate the page contents
            updatePageContents(json.lecture);
            // TODO add update timer
        }
    })
}

/**
 * Update the contents of the page
 */
function updatePageContents(lecture) {
    // Populate question list
    getQuestions();
    // TODO update other contents
    // Lecture details
    if (typeof lecture === 'undefined') {
        getLectureDetails($('#pinInput').val(), function (data) {
            if (data.success) {
                var lecture = data.lecture;
                $('.lecture_title').text(lecture.lecture_title.toUpperCase());
                $('#current_volume_value').text(lecture.lecture_volume);
                $('#current_pace_value').text(lecture.lecture_pace);
            }
        })
    } else {
        $('.lecture_title').text(lecture.lecture_title.toUpperCase());
        $('#current_volume_value').text(lecture.lecture_volume);
        $('#current_pace_value').text(lecture.lecture_pace);
    }
}

/**
 * Post a new question
 */
function sendQuestion() {
    var form_action = '/lectures/' + $('#pinInput').val() + '/questions/';
    var form_el = $("#question_form");

    csrfPOST(form_action, form_el, function (data) {
        console.log(data);
        // Empty question text box
        $("#id_text").val('');
        // Reload question list
        getQuestions();
    });
}

/**
 * Up vote a question
 *
 * `this` will be the element (button) that called the function
 */
function upvoteQuestion() {
    console.log('upvote:' + $(this).val());
    var form_action = '/lectures/' + $('#pinInput').val() + '/questions/' + $(this).val() + '/vote/';
    csrfPOST(form_action, $("<form>"), function (data) {
        console.log(data);
        if (data.success) {
            // Reload question list
            getQuestions();
        }
    });
}

/**
 * Increase or decrease lecture volume preference
 */

//Holder styr på om knappene er blitt trykket på
volume_up = false;
volume_down = false;

function updateVolume(increase) {
    var form_action = '/lectures/' + $('#pinInput').val() + '/volume/';
    var form = $('#volume_form');
    var volume_element = $('#id_volume');

    //Gir knappene radio butten funksjonalitet
    if(increase) {
      if(volume_up) {
        volume_up = false;
        document.getElementById("volume_up").style.backgroundColor = "#f2f2f2";
        volume_element.prop('checked', false);
      }else {
        if (volume_down) {
          volume_down = false
          document.getElementById("volume_down").style.backgroundColor = "#f2f2f2";
          volume_element.prop('checked', true);
          //kjører det dobbelt
          updateVolume(true)
        }else {
          volume_up = true
          document.getElementById("volume_up").style.backgroundColor = "#cfcfcf";
          volume_element.prop('checked', true);
        }
      }
    }else {
      if(volume_down) {
        volume_down = false
        document.getElementById("volume_down").style.backgroundColor = "#f2f2f2";
        volume_element.prop('checked', true);
      }else {
        if (volume_up) {
          volume_up = false
          document.getElementById("volume_up").style.backgroundColor = "#f2f2f2";
          volume_element.prop('checked', false);
          //kjører det dobbelt
          updateVolume(false)
        }else {
          volume_down = true;
          document.getElementById("volume_down").style.backgroundColor = "#cfcfcf";
          volume_element.prop('checked', false);
        }
      }
    }

    csrfPOST(form_action, form, function (data) {
        console.log(data);
        if (data.success) {
            $('#current_volume_value').text(data.lecture.lecture_volume);
            console.log(data.lecture.lecture_volume);
        }
    });
}

/**
 * Increase or decrease lecture pace preference
 */

 //Holder styr på om knappene er blitt trykket på
 pace_up = false;
 pace_down = false;

function updatePace(increase) {
    var form_action = '/lectures/' + $('#pinInput').val() + '/pace/';
    var form = $('#pace_form');
    var pace_element = $('#id_pace');

    //Gir knappene radio butten funksjonalitet
    if(increase) {
      if(pace_up) {
        pace_up = false;
        document.getElementById("pace_up").style.backgroundColor = "#f2f2f2";
        pace_element.prop('checked', false);
      }else {
        if (pace_down) {
          pace_down = false
          document.getElementById("pace_down").style.backgroundColor = "#f2f2f2";
          pace_element.prop('checked', true);
          //kjører det dobbelt
          updatePace(true)
        }else {
          pace_up = true
          document.getElementById("pace_up").style.backgroundColor = "#cfcfcf";
          pace_element.prop('checked', true);
        }
      }
    }else {
      if(pace_down) {
        pace_down = false
        document.getElementById("pace_down").style.backgroundColor = "#f2f2f2";
        pace_element.prop('checked', true);
      }else {
        if (pace_up) {
          pace_up = false
          document.getElementById("pace_up").style.backgroundColor = "#f2f2f2";
          pace_element.prop('checked', false);
          //kjører det dobbelt
          updatePace(false)
        }else {
          pace_down = true;
          document.getElementById("pace_down").style.backgroundColor = "#cfcfcf";
          pace_element.prop('checked', false);
        }
      }
    }


    csrfPOST(form_action, form, function (data) {
        console.log(data);
        if (data.success) {
            $('#current_pace_value').text(data.lecture.lecture_pace);
        }
    });
}
