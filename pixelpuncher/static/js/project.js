/* Project specific Javascript goes here. */

$('#post-form').on('submit', function(event){
    event.preventDefault();
    create_post();
});

// AJAX for posting
function create_post() {
    console.log("create post is working!") // sanity check
    $.ajax({
        url : "/npc/talk/1", // the endpoint
        type : "POST", // http method
        data : { talktext : $('#talktext').val() }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#talktext').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console

            txt = $("#responseMsg").html();
            $("#responseMsg").html(txt + json['message'])
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};


$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();

    $('.shuffle-text').each(function(){
      var container = $(".shuffle-text");

      container.shuffleLetters({
        "text": container.val()
      });
    });

});

$('form').submit(function(){
    $(this).find('button[type=submit]').prop('disabled', true);
});

function increase(id)
{
    var value = parseInt(document.getElementById(id).value, 10);
    value = isNaN(value) ? 0 : value;
    available_points = document.getElementById("id_attribute_points").value;

    if (available_points > 0) {
        value++;
        available_points--;

        document.getElementById('id_attribute_points').value = available_points;
    }

    document.getElementById(id).value = value;
}


function decrease(id, min)
{
    var value = parseInt(document.getElementById(id).value, 10);
    value = isNaN(value) ? 0 : value;
    value--;

    available_points = document.getElementById("id_attribute_points").value;

    if (value < min) {
        value = min;
    }
    else {
        available_points++;
        document.getElementById('id_attribute_points').value = available_points;
    }

    document.getElementById(id).value = value;
}
