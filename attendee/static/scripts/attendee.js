
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
    checkEnd();
    populateTopicList();

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
 * Populate topic list
 */
function populateTopicList() {
    var URL = '/lectures/' + lecture_pin + '/topics/';
    $.getJSON(URL, function (data) {
        console.log(data);
        if (data.success) {
            var topic_list = $('#topic_list');
            topic_list.empty();

            for (var i = 0; i < data.lecture_topics.length; i++) {
                var topic = data.lecture_topics[i];
                var topic_div = appendTopicToList(topic, topic_list, understandTopic);
                if (understood_topics.hasOwnProperty(topic.topic_id) && understood_topics[topic.topic_id]) {
                    topic_div.addClass('topic_indicator_understood');
                }
            }

            var current_topic_div = topic_list.find('div').eq(data.lecture.active_topic_index);
            $('#topic_title').text(current_topic_div.data('topic_title'));
            current_topic_div.addClass('topic_indicator_selected');
            // Center selected topic
            topic_list.css('left', calculateTopicListPosition(topic_list.width(), data.lecture.active_topic_index));
        }
    });
}

var understood_topics = {};

/**
 * Indicate that a topic is understood
 *
 * @param event     Click event
 */
function understandTopic(event) {
    var topic_div = $(this);
    var topic_id = topic_div.data('topic_id');
    var URL = '/lectures/' + lecture_pin + '/topics/' + topic_id + '/understanding/';
    var topic_understanding_form = $('#topic_understanding_form');
    var understood;

    if (understood_topics.hasOwnProperty(topic_id) && understood_topics[topic_id]) {
        understood = false;
        topic_understanding_form.children('input[name=understanding]').prop('checked', understood);
    } else {
        understood = true;
        topic_understanding_form.children('input[name=understanding]').prop('checked', understood);
    }

    csrfPOST(URL, topic_understanding_form, function (data) {
        console.log(data);
        if (data.success) {
            understood_topics[topic_id] = understood;
            if (understood) {
                topic_div.addClass('topic_indicator_understood');
            } else {
                topic_div.removeClass('topic_indicator_understood');
            }
        }
    })
}

/**
 * Get list of questions for lecture
 */
function getQuestions() {
    var api_url = '/lectures/' + lecture_pin + '/questions/';

    $.getJSON(api_url, function (data) {
        //console.log(data);
        if (data.success) {
            // Empty list of existing questions
            $("#question_list").empty();
            // Add questions to list
            for (var i = 0; i < data.questions.length; i++) {
                var question = data.questions[i];
                var list_element = $("<li>");
                var upvote_button = $("<button>");
                var glyphicon_up = $("<span>");
                var upvote_count = $("<div>");
                glyphicon_up.addClass('glyphicon glyphicon-menu-up glyph-upvote');
                upvote_count.addClass('upvote_count');
                upvote_count.text(question.question_votes);
                upvote_button.addClass('upvote-button').attr({
                    type: 'button',
                    title: 'Up-vote this question',
                    onclick: 'upvoteQuestion.call(this)',
                    value: question.question_id
                });
                upvote_button.append(glyphicon_up);
                upvote_button.append(upvote_count);
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
        //console.log(data);
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
    var form_action = '/lectures/' + lecture_pin + '/volume/?vote=';
    var form = $('#volume_form');
    var volume_element = $('#id_volume');
    var query = '';
    runagain = false;
    runagain_value = false;

    //Gir knappene radio butten funksjonalitet
    if(increase) {
      if(volume_up) {
        volume_up = false;
        document.getElementById("volume_up").style.backgroundColor = "#f2f2f2";
        volume_element.prop('checked', true);
      }else {
        if (volume_down) {
          volume_down = false
          document.getElementById("volume_down").style.backgroundColor = "#f2f2f2";
          volume_element.prop('checked', false);
          //kjører det dobbelt
          runagain = true;
          runagain_value = true;
        }else {
          volume_up = true
          document.getElementById("volume_up").style.backgroundColor = "#cfcfcf";
          volume_element.prop('checked', true);
          query = 'true'
        }
      }
    }else {
      if(volume_down) {
        volume_down = false
        document.getElementById("volume_down").style.backgroundColor = "#f2f2f2";
        volume_element.prop('checked', false);
      }else {
        if (volume_up) {
          volume_up = false
          document.getElementById("volume_up").style.backgroundColor = "#f2f2f2";
          volume_element.prop('checked', true);
          //kjører det dobbelt
          runagain = true;
          runagain_value = false;
        }else {
          volume_down = true;
          document.getElementById("volume_down").style.backgroundColor = "#cfcfcf";
          volume_element.prop('checked', false);
          query = 'true'
        }
      }
    }

   form_action += query;

   csrfPOST(form_action, form, function (data) {
       console.log(data);
       if (data.success) {
           $('#current_volume_value').text(data.lecture.lecture_volume);
       }
    });

    if (runagain) {
       setTimeout(function(){
         updateVolume(runagain_value);
       }, 10);
    }
}

//Keeps track of which buttons have been pressed
pace_up = false;
pace_down = false;

/**
 * Increase or decrease lecture pace preference
 */
function updatePace(increase) {
    var form_action = '/lectures/' + lecture_pin + '/pace/?vote=';
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
      setTimeout(function(){
        updatePace(runagain_value);
      }, 10);
    }
}

function checkEnd() {
     var URL = '/lectures/' + lecture_pin;
    $.getJSON(URL, function (data) {
        if (data.success) {
            if(data.lecture.rating_active){
                $('#myModal').modal('show');
                var URL = '/lectures/'+ lecture_pin + '/reset_rating/';
                $.getJSON(URL, function (data) {
                    if (data.success) {console.log("reset success")}
                });
            }
        }
    });
}

$( document ).ready(function() {
    $(".transp_btn").mouseover(function() {
        for (i = 1; i <= parseInt(this.name); i++) {
            $('span[name=' + i + "]").addClass('glyphicon-star');
            $('span[name=' + i + "]").removeClass('glyphicon-star-empty');
        }
    });

    $(".transp_btn").mouseleave(function() {
        $(".transp_btn").children('span').removeClass('glyphicon-star');
        $(".transp_btn").children('span').addClass('glyphicon-star-empty');
    });
})

function rate(rating) {
    var form_action = '/lectures/' + lecture_pin + '/rate/';
    var form = $('<form>');
    var input = $('<input>');
    input.val(rating);
    input.attr('name','rating');
    form.append(input);

    csrfPOST(form_action, form, function (data) {
        if (data.success) {
            console.log("form passed");
        }
    });
}



