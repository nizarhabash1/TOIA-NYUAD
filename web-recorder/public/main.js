
var jsonData = [];
var current_question_len;
var new_question_index;
var scroll_id;

var this_character="test";

function getAllData(){
$.ajax({
		url: '/api/all',
		type: 'GET',
		dataType: 'json',
		error: function(data){
			alert("Oh No! Try a refresh?");
		},
		success: function(data){
			console.log("We have data");
			console.log(data);

			/* The length of the current database */
			current_question_len = data.rows.length;
			if(data.rows.length == 0){
				$('#questionContainer').html('');
				$('#questionContainer').innerText = "";
			}
			else{
				/* If we add a question, the new index will be */
				new_question_index = data.rows[current_question_len-1].doc.index+1;
				console.log("new question index is " + new_question_index);
				//You could do this on the server
	      jsonData = data;

				// sort and update the json so objects are sorted based on index number
				jsonData.rows.sort(function(a,b){
					return a.doc.index - b.doc.index;
				});
				sendDeleteOrUpdateRequest();

				//Clear out current data on the page if any
				$('#questionContainer').html('');
				var htmlString = makeHTML(jsonData);
				$('#questionContainer').append(htmlString);
				//Bind events to each object
				jsonData.rows.forEach(function(d){
					setDeleteEvent(d);
					setUpdateEvent(d);
					// setSaveEvent(d);
					// setPlayEvent(d);
				});
			/* Scroll to last saved video */
			// $('#questionContainer').animate({
		  //       scrollTop: $(scroll_id).offset().top
		  //   });
		    //updateCharacter();
			}
		}
	});

}

function makeHTML(theData){

	var htmlString = '<ul id="theDataList">';
	theData.rows.forEach(function(data_with_id_and_key){
    d = data_with_id_and_key.doc;
		htmlString += '<li id='+ d.index + '>' + d.index + '. ' + d['english-question']
		+ ' <br> ' + d['english-answer'];
		htmlString += '<br><button id=' + d._rev + ' class="updateButton">UPDATE</button>';
		htmlString += '<button id=' + d._id + ' class="deleteButton">DELETE</button>';
		// console.log("The video is " + d.video);
		if(d.video!=""){
			htmlString += '<button id=' + 'save_' + d.index + ' class="saveButton" style="background-color:#e7e7e7">SAVE</button>';
			htmlString += '<button id=' + 'play_' + d.index + ' class="playButton" >PLAY</button>';
		}
		else{
			htmlString += '<button id=' + 'save_' + d.index + ' class="saveButton">SAVE</button>';
			htmlString += '<button id=' + 'play_' + d.index + ' class="playButton" style="display:none">PLAY</button>';
		}

		// var blob_id = "blob_" + d.index;
		// htmlString += '<button id=' + blob_id + ' class="playBackButton">PLAYBACK</button>';
		htmlString += '</li>';
	});
	htmlString += '</ul';
	return htmlString;
}


// function setSaveEvent(data){
// 		var theID = '#save_' + data.doc.index;
// 		scroll_id = '#save_' + data.doc.index;
// 		$(theID).click(function(){
// 			var theObj = _.find(allData, function(d){
// 				return d.index == data.doc.index;
// 			});
// 			console.log("we are SAVING " + data.doc.index);
// 			//Change a value
// 			this_video_name= this_character + "_" + data.doc.index +
//                             "_.mp4";
// 			$("#save-to-disk").trigger('click');
//       //TODO:Please add this line back with correct format
// 			// theObj.video = this_video_name;
// 			sendUpdateRequest(theObj);
// 	});
// }

// function setPlayEvent(data){
// 		var theID = '#play_' + data.index;
// 		$(theID).click(function(){
// 			var theObj = _.find(allData, function(d){
// 				return d.index == data.index;
// 			});
// 			console.log("we are PLAYING " + data.index);
//       //TODO: maybe you need to update the following video name
// 			//Change a value
// 			var play_video_name= this_character + "-videos/" + this_character+"_" + data.index +
//                             "_"+ theObj._id + ".mp4";
//             // var gumVideo = document.querySelector('video#gum');
//             // gumVideo.src = play_video_name;
//             // gumVideo.play();
// 			recordingPlayer.src = play_video_name;
// 			recordingPlayer.play();
// 	});
// }

// function updateCharacter(data){
// 	for(var i = 1001; i < 1214; i++){
// 		var theObj = _.find(allData, function(d){
// 				return d.index == i;
// 			});
// 		if(theObj){
// 			//theObj.character="katarina";
// 			// sendUpdateRequest(theObj);
// 		}
// 	}
// }

//
function setUpdateEvent(data){
		var theID = '#' + data.doc._rev;
		$(theID).click(function(){
			$.each(jsonData.rows,function(i){
				if(jsonData.rows[i]._rev == data._rev){
					var promptVal = prompt('Enter a new answer to the question "'
					   + jsonData.rows[i].doc["english-question"] + '":');
					jsonData.rows[i].doc["english-answer"] = promptVal;
					return false;
				}
			})
			sendDeleteOrUpdateRequest();
			getAllData();
		});
	}


function setDeleteEvent(data){
	var theID = '#' + data.id;
  // if the delete button is clicked
	$(theID).click(function(){
    $.each(jsonData.rows,function(i){
      if(jsonData.rows[i].id == data.id){
        var conf = confirm("Are you sure you want to delete '" + jsonData.rows[i].doc["english-question"] + " : " + jsonData.rows[i].doc["english-answer"] + "' ?");
        if (!conf) return;
        jsonData.rows.splice(i,1);
        return false;
      }
    })
		sendDeleteOrUpdateRequest();
		getAllData();
	});
}

function sendDeleteOrUpdateRequest(){
	$.ajax({
		url: '/update',
		type: 'POST',
		contentType: 'application/json',
		data: JSON.stringify(jsonData),
		error: function(resp){
			console.log("Oh no...");
			console.log(resp);
		},
		success: function(resp){
			console.log('Deleted!');
			console.log(resp);
		}
	});
}

function saveData(obj){
  //TODO: replace with code to add entries to JSON on the go from browser
}

function addNewEntry(){
	var newQuestion = $('#new-question').val();
	var newAnswer = $('#new-answer').val();
	if(!newQuestion || !newAnswer){
		alert("Please enter question and answer");
	}
	else{
		/* update later */
		var data = {
			index: new_question_index,
				character:this_character,
				video:"",
				question:newQuestion,
				answer:newAnswer
		};

		//TODO add this data to json addNewEntry

		// questions[questions.length]=newQuestion;
		// console.log(questions.length);
		// console.log(data);
		// saveData(data);
		$('#new-question').val('');
		$('#new-answer').val('');
}
}

$(document).ready(function(){
	if (page === 'get all data'){
		getAllData();
	}
    //add new question here
    $("#add-question-button").click(function(){
			addNewEntry();
    });
});
