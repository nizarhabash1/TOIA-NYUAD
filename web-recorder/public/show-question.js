fileName = "avatar-json/test.json";

var current_selection_id=null;
var prev_selection_id=null;
var finished_video_id = null;

var questions = [];
var answers = [];
$(document).ready(function() {
    /* When a question is clicked, we need to change the background color of UI to blue and
        change the text color to white, we also need to keep track of which question it is */
    $("#questionContainer").click(function(event){
        console.log(event.target.id );
        clicked_class = $(event.target).attr('class');

        if(!isNaN(event.target.id)){
            prev_selection_id = current_selection_id;
            current_selection_id = event.target.id;
            $("#"+current_selection_id).css(
            {
                'background-color' : 'rgb(140,200,236)',
                'color': 'white'
            });

                $("#"+prev_selection_id).css(
                {
                    'background-color':'white',
                    'color':'black'
                });

            if(current_selection_id == prev_selection_id){
                current_selection_id = null;
                prev_selection_id == null;
                $("#"+prev_selection_id).css(
                {
                    'background-color':'white',
                    'color':'black'
                });
            }
        }
    });
});
