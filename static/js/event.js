
function showAddEvent() {
    document.getElementById('add_event_form').style.display = 'block';
}

function showSearchEvent() {
    document.getElementById('search_event_form').style.display = 'block';
}

function showEvnetOnCalendar() {
    var event = document.getElementById("event").value;
    var start = document.getElementById("start").value;
    var end = document.getElementById("end").value;

    // In January 2021
    var low = "2020-12-31T23:59";
    var high = "2021-02-01T00:00";
    var eventDate = start.substring(8,10);
    console.log(eventDate);

    if (start > end){
        alert("The event start time is later thant the event ending time !")
        document.getElementById("end").value = null;
    }else if (start>low && start<high) {
        // var date = document.getElementById("calendarTable").rows[1].cells[1];


        for(var i=1;i<7;i++){
            for(var j=0;j<7;j++){
                var td=document.getElementById("calendarTable").rows[i].cells[j];
                var date = td.getElementsByClassName('fc-day-number')[0].innerHTML;
                console.log(td.getElementsByClassName('fc-day-number')[0]);
                console.log(date);
                console.log(eventDate==date)
                if (eventDate == date){
                    td.getElementsByClassName('fc-day-content')[0].innerHTML ='<div style="position: relative; height: 25px;"><button onclick=add()> </button></div>'
                }
            }
        }

    }
}

function popup(event, start, end){


    document.getElementById("selkeydiv").style.display = "block";
    document.getElementById("all_light").style.display = "block";

    document.getElementById('event_popup').setAttribute('value',event);
    document.getElementById('start_popup').setAttribute('value',start);
    document.getElementById('end_popup').setAttribute('value',end);

}

function popup_to_share(){


    document.getElementById("share_popup").style.display = "block";
    document.getElementById("all_light").style.display = "block";

    // document.getElementById('event_popup').setAttribute('value',event);


}

function hide() {
    document.getElementById("selkeydiv").style.display = "none";
    document.getElementById("all_light").style.display = "none";
    document.getElementById("share_popup").style.display = "none";
    document.getElementById("client_calendar").style.display = "none";



}

function seeClientCalendar(host) {

    $.ajax("/submit_share_event/", {


                dataType: "json",
                data: {'user':host},
                success: function (data) {
                    // console.log(data.share_note);
                    if (data.share_note != "") {
                        alert(data.share_note);
                    }

                    if (data.rows!="") {
                        TBcontent = document.getElementById('client_calendar_tbody');
                        TBcontent.innerHTML = "<tr><th>User</th><th>Event</th><th>Start Time</th><th>End Time</th></tr>"

                        for (var row = 0; row < data.rows.length; row++) {
                            var start_time = data.rows[row]['start_time'];
                            var user = data.rows[row]['user'];
                            var event = data.rows[row]['event'];
                            var end_time = data.rows[row]['end_time'];

                            var tr = document.createElement("tr");
                            var xuser = document.createElement("td");
                            var xevent = document.createElement("td");
                            var xstart = document.createElement("td");
                            var xend = document.createElement("td");
                            xuser.innerHTML = "" + user;
                            xevent.innerHTML = "" + event;
                            xstart.innerHTML = "" + start_time;
                            xend.innerHTML = "" + end_time;
                            TBcontent.appendChild(tr)
                            tr.appendChild(xuser);
                            tr.appendChild(xevent);
                            tr.appendChild(xstart);
                            tr.appendChild(xend);

                            // TBcontent += "<tr> <td>"+user+"</td> <td>"+event+"</td> <td>"+start_time+"</td> <th>"+end_time+"</th> </tr></tbody>";
                            // document.getElementById('search_result').innerHTML = TBcontent;
                        }
                        document.getElementById('client_calendar').style.display = 'block';
                        document.getElementById("all_light").style.display = "block";
                    }
                    else{
                        TBcontent = document.getElementById('client_calendar_tbody');
                        TBcontent.innerHTML = "<tr><th>User</th><th>Event</th><th>Start Time</th><th>End Time</th></tr>"
                        alert("No event matched.");

                        document.getElementById('client_calendar').style.display = 'block';
                        document.getElementById("all_light").style.display = "block";
                    }

                },
                error : function() {
                    alert("Search shared calendar error！");
                }
    });
}


function loadEvents(user){

    $.ajax('/load_events/',{
        data:{
            'user':user
        },
        dataType: 'json',
        success:function (data) {

            for(var row=0; row<data.rows.length; row++){
                var start_time = data.rows[row]['start_time'];
                var start_date = data.rows[row]['start'];
                var event = data.rows[row]['event'];
                var end_time = data.rows[row]['end_time'];
                for(var i=1;i<7;i++){
                    for(var j=0;j<7;j++){
                        var td=document.getElementById("calendarTable").rows[i].cells[j];
                        var date = td.getElementsByClassName('fc-day-number')[0].innerHTML;
                        if (start_date == date){
                            var content = td.getElementsByClassName('fc-day-content')[0].innerHTML;
                            content +='<div style="position: relative; height: 25px;overflow: scroll;overflow-x: hidden;"><button onclick="popup(\''+event+'\',\''+start_time+'\',\''+end_time+'\')" style="width: 100px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">'+event+'</button></div>'
                            // console.log(content);
                            td.getElementsByClassName('fc-day-content')[0].innerHTML =content;
                        }
                    }
                }
            }
            var news_num = data.news.length;
            for(var i=0;i<news_num;i++){
                var host = data.news[i];

                var ul = document.getElementById('unread_list');
                var li = document.createElement('li');
                li.innerHTML = "<li><a><span class='label label-success'>New</span><button class='host_button' onclick='seeClientCalendar(\""+host+"\");'>"+host+" shared calendar</button></a></li>"
                ul.appendChild(li);
            }
            document.getElementById('unread').innerHTML = news_num;
        }
    })
}

function searchEvents(){

    $.ajax("/submit_search_event/", {

                type: "POST",
                dataType: "json",
                data: $('#search_event_form').serialize(),
                success: function (data) {
                    // console.log(data);
                    if (data.search_note != "") {
                        alert(data.search_note);
                    }
                    if (data.rows!="") {
                        TBcontent = document.getElementById('search_result_tbody');
                        TBcontent.innerHTML = "<tr><th>User</th><th>Event</th><th>Start Time</th><th>End Time</th></tr>"

                        for (var row = 0; row < data.rows.length; row++) {
                            var start_time = data.rows[row]['start_time'];
                            var user = data.rows[row]['user'];
                            var event = data.rows[row]['event'];
                            var end_time = data.rows[row]['end_time'];

                            var tr = document.createElement("tr");
                            var xuser = document.createElement("td");
                            var xevent = document.createElement("td");
                            var xstart = document.createElement("td");
                            var xend = document.createElement("td");
                            xuser.innerHTML = "" + user;
                            xevent.innerHTML = "" + event;
                            xstart.innerHTML = "" + start_time;
                            xend.innerHTML = "" + end_time;
                            TBcontent.appendChild(tr)
                            tr.appendChild(xuser);
                            tr.appendChild(xevent);
                            tr.appendChild(xstart);
                            tr.appendChild(xend);


                            // TBcontent += "<tr> <td>"+user+"</td> <td>"+event+"</td> <td>"+start_time+"</td> <th>"+end_time+"</th> </tr></tbody>";
                            // document.getElementById('search_result').innerHTML = TBcontent;
                            document.getElementById('search_result').style.display = 'block';
                        }
                    }
                    else{
                        TBcontent = document.getElementById('search_result_tbody');
                        TBcontent.innerHTML = "<tr><th>User</th><th>Event</th><th>Start Time</th><th>End Time</th></tr>"
                        alert("No event matched.");
                    }
                },
                error : function() {
                    alert("Search event error！");
                }
            });
}

function editEvents() {

    // alert($('#edit_event_form').serialize());
    var data = $('#edit_event_form').serializeArray();
    var init_start = document.getElementById('start_popup').getAttribute('value');
    data.push({name: "init", value: init_start});

    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            // if not safe, set csrftoken
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.ajax("/submit_edit_event/", {

                type: "POST",
                dataType: "json",
                data: data,
                success: function (data) {
                    console.log(data);
                    alert(data.edit_note);
                    location.href="/index/"; //refresh to update calendar
                },
                error : function() {
                    alert("Edit event error！");
                }
            });
}

function removeEvents() {
    var data = $('#edit_event_form').serializeArray();

    $.ajax("/submit_remove_event/", {

                type: "POST",
                dataType: "json",
                data: data,
                success: function (data) {
                    // console.log(data);
                    alert(data.remove_note);
                    location.href="/index/"; //refresh to update calendar
                },
                error : function() {
                    alert("Remove event error！");
                }
            });
}

function shareEvents() {

    var data = $('#share_event_form').serializeArray();

    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            // if not safe, set csrftoken
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.ajax("/share_event/", {

                type: "POST",
                dataType: "json",
                data: data,
                success: function (data) {
                    console.log(data);
                    alert(data.share_note);
                    if(data.exit_code==0){
                        location.href="/index/"; //refresh
                    }
                },
                error : function() {
                    alert("Ajax: Share event error！");
                }
            });
}



