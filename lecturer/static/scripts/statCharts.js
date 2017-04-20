function createCharts(course_id) {
    var ctx = $("#countChart");
    var ctx2 = $("#activityChart");
    var ctx3 = $("#questionPie");
    var ctx4 = $("#ratingChart");
    var attendees_list_count = [];
    var lecture_list = [];
    var URL = '/courses/' + String(course_id) + '/stats/';

    $.getJSON(URL, function (data) {
        if (data.success) {
            //--------Count Chart--------//
            for (count in data.attendee_count) {
                attendees_list_count.push(data.attendee_count[count]);
                lecture_list.push(count);
            };
                attendees_list_count = attendees_list_count.reverse();
                lecture_list = lecture_list.reverse();
                var lectures = [];
                for(var x = 0; x < lecture_list.length; x++){
                    var temp = lecture_list[x]
                    temp = temp.substring(0, 22)
                    lectures.push(temp);
                }

                var countChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: lectures,
                    datasets: [{
                        label: '# of attendants',
                        data: attendees_list_count,
                        backgroundColor: ["#2F9E92"],
                        borderColor: ["#007D70"],
                        borderWidth: 2,
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });
            //--------Activity Chart--------//
                var activity_list = [];

                for (count in data.lecture_activity) {
                    activity_list.push(data.lecture_activity[count]);
                };
                activity_list.reverse();

                var ActivityChart = new Chart(ctx2, {
                type: 'line',
                data: {
                    labels: lectures,
                    datasets: [{
                        label: '# of activity-points',
                        data: activity_list,
                        backgroundColor: ["#0D998A"],
                        borderColor: ["#007d70"],
                        borderWidth: 2,
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });
            //--------Question per lecture Chart--------//
            var questionCount_list = [];

                for (count in data.question_count) {
                    questionCount_list.push(data.question_count[count]);
                };
                questionCount_list.reverse();
                console.log(questionCount_list);

                var questionPie = new Chart(ctx3, {
                type: 'line',
                data: {
                    labels: lectures,
                    datasets: [{
                        label: '# of activity-points',
                        data: questionCount_list,
                        backgroundColor: ["#00665B"],
                        borderColor: ["#007d70"],
                        borderWidth: 2,
                    }]
                },
            });

            //--------Lecture Ratings--------//
            var lecture_ratings = [];

                for (count in data.rating) {
                    lecture_ratings.push(data.rating[count]);
                };
                lecture_ratings.reverse();
                console.log(lecture_ratings);

                var ratingChart = new Chart(ctx4, {
                type: 'line',
                data: {
                    labels: lectures,
                    datasets: [{
                        label: '# of activity-points',
                        data: lecture_ratings,
                        backgroundColor: ["#00665B"],
                        borderColor: ["#007d70"],
                        borderWidth: 2,
                    }]
                },
            });
        };
    });
};