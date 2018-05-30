
var allData = [];
var current_question_len;
var new_question_index;
var scroll_id;

var this_character="test";

// recordingPlayer.addEventListener('ended', function() {
//
//     // ADDED funciontality of streaming after a playback
//     navigator.mediaDevices.getUserMedia(constraints).
//         then(handleSuccess).catch(handleError);
//         });

function getAllData(){
$.ajax({
		url: '/api/all',
		type: 'GET',
		dataType: 'json',
		error: function(data){
			console.log(data);
			alert("Oh No! Try a refresh?");
		},
		success: function(data){
			console.log("We have data");
			console.log(data);

			/* The length of the current database */
			current_question_len = data.rows.length;
      console.log("data length is " + current_question_len);
			/* If we add a question, the new index will be */
			new_question_index = data.rows[current_question_len-1].doc.index+1;
			console.log("new question index is " + new_question_index);
			//You could do this on the server
			allData = data.rows.map(function(d){
				return d;
			});
			//Clear out current data on the page if any
			$('#questionContainer').html('');
			var htmlString = makeHTML(allData);

			// console.log(htmlString);
			$('#questionContainer').append(htmlString);
			//Bind events to each object
			allData.forEach(function(d){
				setDeleteEvent(d);
				setUpdateEvent(d);
				// d.blob="";
				// setUpdateBlobEvent(d);
				setSaveEvent(d);
				setPlayEvent(d);
			});
			/* Scroll to last saved video */
			$('#questionContainer').animate({
		        scrollTop: $(scroll_id).offset().top
		    });
		    //updateCharacter();
		}
	});

}

function makeHTML(theData){

	var htmlString = '<ul id="theDataList">';
	theData.forEach(function(d){
		htmlString += '<li id='+ d.doc.index + '>' + d.doc.index + '. ' + d.doc['english-question']
		+ ' <br> ' + d.doc['english-answer'];
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

function saveData(obj){
	$.ajax({
		url: '/save',
		type: 'POST',
		contentType: 'application/json',
		data: JSON.stringify(obj),
		error: function(resp){
			console.log("Oh no...");
			console.log(resp);
		},
		success: function(resp){
			console.log('WooHoo!');
			console.log(resp);
			getAllData();
		}
	});
}


function setSaveEvent(data){
		var theID = '#save_' + data.index;
		scroll_id = '#save_' + data.index;
		$(theID).click(function(){
			var theObj = _.find(allData, function(d){
				return d.index == data.index;
			});
			console.log("we are SAVING " + data.index);
			//Change a value
			this_video_name= this_character + "_" + data.index +
                            "_"+ theObj._id + ".mp4";
			$("#save-to-disk").trigger('click');
			theObj.video = this_video_name;
			sendUpdateRequest(theObj);


	});
}

function setPlayEvent(data){
		var theID = '#play_' + data.index;
		$(theID).click(function(){
			var theObj = _.find(allData, function(d){
				return d.index == data.index;
			});
			console.log("we are PLAYING " + data.index);
			//Change a value
			var play_video_name= this_character + "-videos/" + this_character+"_" + data.index +
                            "_"+ theObj._id + ".mp4";
            // var gumVideo = document.querySelector('video#gum');
            // gumVideo.src = play_video_name;
            // gumVideo.play();
			recordingPlayer.src = play_video_name;
			recordingPlayer.play();


	});
}

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


function setUpdateEvent(data){
		var theID = '#' + data._rev;
		$(theID).click(function(){
			var theObj = _.find(allData, function(d){
				return d._rev == data._rev;
			});
			//Change a value
			var promptVal = prompt('Enter a new answer to the question "' + theObj.question + '":');
			if (!promptVal) return;
			theObj.answer = promptVal;
			sendUpdateRequest(theObj);
	});
}

function sendUpdateRequest(obj){
	$('#questionContainer').html('<div id="loading">Data is being updated...</div>');
	console.log(obj);
	$.ajax({
		url: '/update',
		type: 'POST',
		contentType: 'application/json',
		data: JSON.stringify(obj),
		error: function(resp){
			console.log("Oh no...");
			console.log(resp);
		},
		success: function(resp){
			console.log('Updated!');
			console.log(resp);
			getAllData();
		}
	});
}


// function setUpdateBlobEvent(data){
// 		var theID = '#blob' + data.index;
// 		var theObj = _.find(allData, function(d){
// 			return d.index == data.index;
// 		});
// 		recordingPlayer.src = theObj.blob;
// }

// function sendUpdateBlobRequest(obj){
// 	$('#questionContainer').html('<div id="loading">Blob data is being updated...</div>');
// 	console.log(obj);
// 	$.ajax({
// 		url: '/update',
// 		type: 'POST',
// 		contentType: 'application/json',
// 		data: JSON.stringify(obj),
// 		error: function(resp){
// 			console.log("Oh no...");
// 			console.log(resp);
// 		},
// 		success: function(resp){
// 			console.log('Updated!');
// 			console.log(resp);
// 			getAllData();
// 		}
// 	});
// }


function setDeleteEvent(data){
	var theID = '#' + data._id;
	$(theID).click(function(){
		var theObj = _.find(allData, function(d){
			return d._id == data._id;
		});
		console.log(theObj);
		sendDeleteRequest(theObj);
	});
}

function sendDeleteRequest(obj){
	console.log(obj);
	//Make sure you want to delete
	var conf = confirm("Are you sure you want to delete '" + obj.question + " : " + obj.answer + "' ?");
	if (!conf) return;
	//Proceed if confirm is true
	$('#dataContainer').html('<div id="loading">Data is being deleted...</div>');
	$.ajax({
		url: '/delete',
		type: 'POST',
		contentType: 'application/json',
		data: JSON.stringify(obj),
		error: function(resp){
			console.log("Oh no...");
			console.log(resp);
		},
		success: function(resp){
			console.log('Deleted!');
			console.log(resp);
			getAllData();

			/*----------------------------------------
			//ALT APPROACH - Avoid extra request to db
			//Remove deleted obj from allData array
			allData = _.reject(allData, function(d){
				return d._id == obj._id;
			});
			//Clear out current data on the page if any
			$('#dataContainer').html('');
			var htmlString = makeHTML(allData);
			$('#dataContainer').append(htmlString);
			//Bind events to each object
			allData.forEach(function(d){
				setDeleteEvent(d);
				setUpdateEvent(d);
			});
			----------------------------------------*/
		}
	});
}

$(document).ready(function(){

	if (page === 'get all data'){
		getAllData();
	}
    //add new question here
    $("#add-question-button").click(function(){
        var newQuestion = $('#new-question').val();
        var newAnswer = $('#new-answer').val();
        if(!newQuestion || !newAnswer){
        	alert("Please enter question and answer");
        }
        else{
	        var timeStamp = new Date();
	        /* update later */
	        var data = {
	        	index: new_question_index,
	            character:this_character,
	            video:"",
	            question:newQuestion,
	            answer:newAnswer,
	            date:timeStamp,
	        };
	        questions[questions.length]=newQuestion;
	        console.log(questions.length);
	        console.log(data);
	        saveData(data);
	        $('#new-question').val('');
	        $('#new-answer').val('');
	    }

    });



});
