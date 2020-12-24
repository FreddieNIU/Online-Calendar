function hIde() {
    document.getElementById("signup_popup").style.display = "none";
    document.getElementById("all_dark").style.display = "none";
}

function pop(){

    document.getElementById("signup_popup").style.display = "block";
    document.getElementById("all_dark").style.display = "block";

}

function sign_up(){

    var data = $('#signup_form').serializeArray();

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

    $.ajax("/signup/", {

                type: "POST",
                dataType: "json",
                data: data,
                success: function (data) {
                    console.log(data);
                    if(data.exit_note==0){
                        alert('Successfully signed up! Please login.')
                        location.href=""; //refresh
                    }else if(data.exit_note==1){
                        alert('Username already exist!')
                    }else{
                        alert('Error when creating an account. Please try again! ')
                    }
                },
                error : function() {
                    alert("Ajax: Sign up event error！");
                }
            });
}

