var ctx = $("#countChart");
var attendees_list_count = [];
var lecture_list = [];
var URL = '/courses/19/stats/';
/* Change 19 to course id of whatever course the lecturer is viewing */

$.getJSON(URL, function (data) {
    if (data.success) {
        for(count in data.attendee_count) {
            attendees_list_count.push(data.attendee_count[count]);
            lecture_list.push(count);
        };
    };
});


var countChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: lecture_list,
        datasets: [{
            label: '# of Votes',
            data: attendees_list_count,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});