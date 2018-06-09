// fileName = "avatar-json/test.json";
// var first_time_upload = false;
//
// var current_selection_id=null;
// var prev_selection_id=null;
// var finished_video_id = null;
//
// var questions = [];
// var answers = [];
// $(document).ready(function() {
//     /* If we create a new avatar for the first time, upload the q & a to database */
//     if(first_time_upload){
//         $.ajax({
//             type: "GET",
//             url: fileName,
//             dataType: "json",
//             success: function(data) {
//                 makeQuestionObjects(data);}
//          });
//     }
//
//
//     /* When a question is clicked, we need to change the background color of UI to blue and
//         change the text color to white, we also need to keep track of which question it is */
//     $("#questionContainer").click(function(event){
//         console.log(event.target.id );
//         clicked_class = $(event.target).attr('class');
//
//         if(!isNaN(event.target.id)){
//             prev_selection_id = current_selection_id;
//             current_selection_id = event.target.id;
//             $("#"+current_selection_id).css(
//             {
//                 'background-color' : 'rgb(140,200,236)',
//                 'color': 'white'
//             });
//
//                 $("#"+prev_selection_id).css(
//                 {
//                     'background-color':'white',
//                     'color':'black'
//                 });
//
//             if(current_selection_id == prev_selection_id){
//                 current_selection_id = null;
//                 prev_selection_id == null;
//                 $("#"+prev_selection_id).css(
//                 {
//                     'background-color':'white',
//                     'color':'black'
//                 });
//             }
//         }
//     });
// });
//
// /* creating questions and answer */
// function makeQuestionObjects(allEntries){
//     console.log("making objects");
//     // console.log(allEntries);
//     // console.log(allEntries.Entries);
//     var questionObject;
//     for (var entry = 0; entry < allEntries.Entries.length; entry++) {
//         // console.log(allEntries.Entries[entry].question);
//         var current_question = allEntries.Entries[entry].question;
//         var current_answer = allEntries.Entries[entry].answer;
//         var current_index = allEntries.Entries[entry].index;
//         var current_character = allEntries.Entries[entry].character;
//
//         var timeStamp = new Date();
//         var data = {
//             index:current_index,
//             character:current_character,
//             video:"",
//             question:current_question,
//             answer:current_answer,
//             date:timeStamp
//         };
//
//         console.log(data);
//         setTimeout(saveData(data),500);
//     }}
