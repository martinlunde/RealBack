
$(document).ready(function () {
    $('#landing_page').css("display", "none");
    $('#frontpage_attendee').css("display", "block");
    $('.footer').css("display", "block");

    $('#joinButton').click(onJoin);
    $('#pinInput').focus();
    $('#question_submit_button').click(sendQuestion);
});

var lecture_pin = '';

/**
 * Actions to perform after a lecture is joined
 */
function onJoin(event) {
    var PIN = $('#pinInput').val().trim().toUpperCase();
    var URL = '/lectures/' + PIN + '/join/';
    $.getJSON(URL, function (data) {
        console.log(data);
        if (data.success) {
            lecture_pin = PIN;
            $('#landing_page').show();
            $('#frontpage_attendee').hide();
            $('.footer').hide();

            // Populate the page contents
            updatePageContents(data.lecture);
            var timerID = setInterval(updatePageContents, 10000);
            console.log(timerID);
            intervalTimerIDs.push(timerID);
        }
    });

    var question_input = $('#question_form textarea');
    question_input.keypress(function (event) {
        if (event.key == 'Enter' && !event.shiftKey) {
            $('#question_submit_button').click();
            event.preventDefault();
        }
    });
    function question_length(event) {
        $('#question_length').html($('<div>').text(question_input.val().length + '/160'));

        if (question_input.val().length >= 160) {
            $('#question_length').children('div').css({
                'animation-name': 'flash_text',
                'animation-timing-function': 'linear',
                'animation-duration': '2s'
            });
        }
    }
    question_input.keyup(question_length);
    question_input.keydown(question_length);
    question_input.keyup();

    event.preventDefault();
}

/**
 * Update the contents of the page
 */
function updatePageContents(lecture) {
    // Populate question list
    getQuestions();
    checkReset();
    // TODO update other contents
    // Lecture details
    if (typeof lecture === 'undefined') {
        var URL = '/lectures/' + lecture_pin + '/';
        $.getJSON(URL, function (data) {
            if (data.success) {
                var lecture = data.lecture;
                $('.lecture_title').text(lecture.lecture_title.toUpperCase());
            }
        })
    } else {
        $('.lecture_title').text(lecture.lecture_title.toUpperCase());
    }
}

/**
 * Get list of questions for lecture
 */
function getQuestions() {
    var api_url = '/lectures/' + lecture_pin + '/questions/';
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
                list_element.append('- ' + question.question_text);
                $("#question_list").append(list_element);
            }
            markQuestion();
        }
    });
}

/**
 * Post a new question
 */
function sendQuestion(event) {
    var form_action = '/lectures/' + lecture_pin + '/questions/';
    var form_el = $("#question_form");

    csrfPOST(form_action, form_el, function (data) {
        console.log(data);
        // Empty question text box
        $("#id_text").val('');
        $("#id_text").keyup();
        // Reload question list
        getQuestions();
    });
    event.preventDefault();
}

//Keeps track of upvoted questions
upvotedQuestions=[];

/**
 * Up vote a question
 *
 * `this` will be the element (button) that called the function
 */
function upvoteQuestion() {
    upvotedQuestions.push($(this).val());
    console.log('upvote:' + $(this).val());
    var form_action = '/lectures/' + lecture_pin + '/questions/' + $(this).val() + '/vote/';
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
function markQuestion(){
    var question_list = document.getElementById("question_list");
    var list_item = question_list.getElementsByTagName("button");

    for (var i=0; i < list_item.length; i++) {
        if (upvotedQuestions.includes(list_item[i].value)) {
            list_item[i].disabled = true;
            list_item[i].getElementsByTagName("span")[0].style.color = "#007d70";
        }
  }
}

//Checks if volume or pace has been reset
volume_reset_timestamp = 0;
pace_reset_timestamp = 0;

/**
 * Increase or decrease lecture volume preference
 */
function checkReset() {
    var URL = '/lectures/'+ lecture_pin + '/';
    $.getJSON(URL, function (data) {
        console.log(data);
        if (data.success) {
            if (data.lecture.volume_reset_timestamp != volume_reset_timestamp) {
                console.log("volume reset");
                volume_reset_timestamp = data.lecture.volume_reset_timestamp;
                volume_up = false
                volume_down = false
                document.getElementById("volume_up").style.backgroundColor = "#f2f2f2";
                document.getElementById("volume_down").style.backgroundColor = "#f2f2f2";
            }
            if (data.lecture.pace_reset_timestamp != pace_reset_timestamp) {
                pace_reset_timestamp = data.lecture.pace_reset_timestamp;
                pace_up = false
                pace_down = false
                document.getElementById("pace_up").style.backgroundColor = "#f2f2f2";
                document.getElementById("pace_down").style.backgroundColor = "#f2f2f2";
            }
        }
    });
}

//Keeps track if which buttons have been pressed
volume_up = false;
volume_down = false;

/**
 * Increase or decrease lecture volume preference
 */
function updateVolume(increase) {
    var form_action = '/lectures/' + lecture_pin + '/volume/';
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


//Keeps track of which buttons have been pressed
pace_up = false;
pace_down = false;

/**
 * Increase or decrease lecture pace preference
 */
function updatePace(increase) {
    var form_action = '/lectures/' + $('#pinInput').val() + '/pace/?vote=';
    var form = $('#pace_form');
    var pace_element = $('#id_pace');
    var query = '';
    runagain = false;
    runagain_value = false;

    //Gir knappene radio butten funksjonalitet
    if(increase) {
      if(pace_up) {
        pace_up = false;
        document.getElementById("pace_up").style.backgroundColor = "#f2f2f2";
        pace_element.prop('checked', true);
      }else {
        if (pace_down) {
          pace_down = false
          document.getElementById("pace_down").style.backgroundColor = "#f2f2f2";
          pace_element.prop('checked', false);
          //kjører det dobbelt
          runagain = true;
          runagain_value = true;
        }else {
          pace_up = true
          document.getElementById("pace_up").style.backgroundColor = "#cfcfcf";
          pace_element.prop('checked', true);
          query = 'true'
        }
      }
    }else {
      if(pace_down) {
        pace_down = false
        document.getElementById("pace_down").style.backgroundColor = "#f2f2f2";
        pace_element.prop('checked', false);
      }else {
        if (pace_up) {
          pace_up = false
          document.getElementById("pace_up").style.backgroundColor = "#f2f2f2";
          pace_element.prop('checked', true);
          //kjører det dobbelt
          runagain = true;
          runagain_value = false;
        }else {
          pace_down = true;
          document.getElementById("pace_down").style.backgroundColor = "#cfcfcf";
          pace_element.prop('checked', false);
          query = 'true'
        }
      }
    }

    form_action += query;

    csrfPOST(form_action, form, function (data) {
        console.log(data);
        if (data.success) {
            $('#current_pace_value').text(data.lecture.lecture_pace);
        }
    });

    if (runagain) {
        updatePace(runagain_value);
    }
}
