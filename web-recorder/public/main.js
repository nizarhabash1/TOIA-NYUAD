var jsonData = [];
var current_question_len;
var UpdateJSONstion_index;
var scroll_id;
var scriptName;
var data_to_send;
var scriptList;

getScripts();

function capitalize(string) {
    return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
}

// Display all the question and answer entries retrieved from Node back-end
function getAllData(){
$.ajax({
		url: '/api/all',
		type: 'GET',
		dataType: 'json',
		contentType: 'application/json; charset=UTF-8',
		error: function(data){
			alert("Oh No! Try a refresh?");
		},
		success: function(data){
			console.log("We have data");
			console.log(data);

			/* The length of the current database */
			current_question_len = data.rows.length;
			if(data.rows.length == 0){
				jsonData = data;
				$('#questionContainer').html('');
				$('#questionContainer').innerText = "";
			}
			else{
				/* If we add a question, the new index will be */
				UpdateJSONstion_index = data.rows[current_question_len-1].doc.index+1;
				console.log("new question index is " + UpdateJSONstion_index);
	      jsonData = data;

				//Clear out current data on the page if any
				$('#questionContainer').html('');
				var htmlString = makeHTML(jsonData);
				$('#questionContainer').append(htmlString);
				//Bind events to each object
				jsonData.rows.forEach(function(d){
					setDeleteEvent(d);
					setUpdateEvent(d);
					setSaveEvent(d);
					setPlayEvent(d);
				});
			// TODO: add the following functionality back
			/* Scroll to last saved video */
			// $('#questionContainer').animate({
		  //       scrollTop: $(scroll_id).offset().top
		  //   });
		    //updateCharacter();
			}
		}
	});

}

// Making HTML texts based on information retrieved from JSON db
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
		htmlString += '</li>';
	});
	htmlString += '</ul';
	return htmlString;
}

// Setting save events for all the SAVE buttons on the page
// If a save button is clicked, it will trigger camera.js
// and fetch to save the video to local file system
// as well as save the new video name to the JSON db
function setSaveEvent(data){
		var theID = '#save_' + data.doc.index;
		scroll_id = '#save_' + data.doc.index;
		$(theID).click(function(){

			$.each(jsonData.rows,function(i){
				if(jsonData.rows[i].doc.index == data.doc.index){
					console.log("we are SAVING " + data.doc.index);
					// Update the video name to JSON database
					this_video_name= document.getElementById("nameForSaving").innerHTML + "_" + data.doc.index +
							"_" + data.doc._id + ".mp4";

					$("#save-to-disk").trigger('click');
					jsonData.rows[i].doc["video"] = this_video_name;
					sendUpdateJSONRequest();
					return false;
				}
			})

	});
}

// This function is called in camera.js after a blob file is recorded
function triggerSaveRequest(this_file){
	console.log("your file info is ");
	console.log(this_file);
	var fd = new FormData();
	fd.append('blob', this_file, this_video_name);
	console.log(fd);
	fetch('/save',
	{
	    method: 'post',
	    body: fd
	});
}

// Setting playback functionality for all the entries with videos recorded
function setPlayEvent(data){
		var theID = '#play_' + data.doc.index;

		$(theID).click(function(){
			var theObj = _.find(jsonData.rows, function(d){
				return d.doc.index == data.doc.index;
			});
			console.log("we are PLAYING " + data.doc.index);

			var play_video_name= "avatars/" + document.getElementById("nameForSaving").innerHTML + "/" + document.getElementById("nameForSaving").innerHTML+"_" + data.doc.index +
                            "_"+ theObj.doc._id + ".mp4";

			recordingPlayer.src = play_video_name;
			recordingPlayer.play();
	});
}

// Setting update functionality for avatar creater to update the answer of a question
function setUpdateEvent(data){
		var theID = '#' + data.doc._rev;

		$(theID).click(function(){
			$.each(jsonData.rows,function(i){
				if(jsonData.rows[i].doc._rev == data.doc._rev){
					var promptVal = prompt('Enter a new answer to the question "'
					   + jsonData.rows[i].doc["english-question"] + '":');
					jsonData.rows[i].doc["english-answer"] = promptVal;
					return false;
				}
			})
			sendUpdateJSONRequest();
		});
	}

// Seeting deleting functionality for all question/ answer pairs
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
		sendUpdateJSONRequest();
	});
}

// Call this function when we need to sync the jsonData and write it to the actual JSON file
function sendUpdateJSONRequest(){
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
	getAllData();
}

// Call this function to make a directory
// Call this function when we need to sync the jsonData and write it to the actual JSON file
function makeDirectory(avatarName){
	jsonData = {"name": avatarName};
	$.ajax({
		url: '/makedir',
		type: 'POST',
		contentType: 'application/json',
		data: JSON.stringify(jsonData),
		error: function(resp){
			console.log("Oh no...");
			console.log(resp);
		},
		success: function(resp){
			console.log('Created directory!');
			console.log(resp);
		}
	});
}

// This function allows avatar makers to add new question and answer entry
// Also sorts the jsonData
function addNewEntry(){
	var newQuestion = $('#new-question').val();
	var newAnswer = $('#new-answer').val();
	if(!newQuestion || !newAnswer){
		alert("Please enter question and answer");
	}
	else{
		console.log(jsonData.rows);
		// sort jsonData, call this following lines if needed to sort jsonData
		if(jsonData.length != 0){
			jsonData.rows.sort(function(a,b){
				return a.doc.index - b.doc.index;
			});
		}

		// s4 and unique_id generate 32 digit random characters for unique id and unique rev
		function s4() {
			return Math.floor((1 + Math.random()) * 0x10000)
				.toString(16)
				.substring(1);
		}
		function unique_id(){
			return s4()+s4()+s4()+s4()+s4()+s4()+s4()+s4();
		}

		var new_unique_id = unique_id();
		var new_unique_rev = "3-" + unique_id();
		// the new index number will be one increment from the largest one so far
		if(jsonData.rows.length != 0){
			var new_index_number = jsonData.rows[jsonData.rows.length-1].doc.index+1;
		}
		else{
			new_index_number = 1;
		}

		// TODO: get the language option from avatar maker
		// currently defaulting to english
		var data = {
			key:new_unique_id,
			doc:{
					index: new_index_number,
					character:document.getElementById("nameForSaving").innerHTML,
					video:"",
					"english-question":newQuestion,
					"english-answer":newAnswer,
					"arabic-question":"",
					"arabic-answer":"",
					"video-type":"regular",
					language:"English",
					_id: new_unique_id,
					_rev: new_unique_rev
				},
			id:new_unique_id,
			value:{rev:new_unique_rev}
		};

		jsonData.rows.push(data);
		console.log("inside add new entry");
		sendUpdateJSONRequest();

		$('#new-question').val('');
		$('#new-answer').val('');
	}
}

$("#scriptType").submit(function(e) {
	console.log("HI");
    e.preventDefault();
});

$("#templateType").submit(function(e) {
	console.log("YOS");
    e.preventDefault();
});

$("#selectScript").submit(function(e) {
	console.log("HI");
    e.preventDefault();
});

$("#avatarOptions").submit(function(e) {
	console.log("HI");
    e.preventDefault();
});

$("#nameAvatar").submit(function(e) {
	console.log("HI");
    e.preventDefault();
});

$("#selectPrevious").submit(function(e) {
	console.log("HI");
    e.preventDefault();
});

// Call this function when we need to sync the jsonData and write it to the actual JSON file
function sendFileName(){
	console.log("YEAH IN HERE");
	console.log(scriptName);
	data_to_send={"name": scriptName};
	data_to_send=JSON.stringify(data_to_send);
	$.ajax({
		url: '/filename',
		type: 'POST',
		data: data_to_send,
		contentType: 'application/json; charset=utf-8',
		error: function(resp){
			console.log("Oh no...");
			console.log(data_to_send);
			console.log(resp);
		},
		success: function(resp){
			console.log('Sent file name!');
			console.log(resp);
		}
	});

	getAllData();
}

function avatarOptions() {
	console.log("YO WTF");
	var avatarType = document.querySelector('input[name="avatar"]:checked').value;
	if (avatarType === "previousAvatar") {
		document.getElementById("selectAvatarType").style.display='none';
		document.getElementById("selectPrevious").style.display='';
	} else if (avatarType === "newAvatar") {
		document.getElementById("selectAvatarType").style.display='none';
		document.getElementById("selectScript").style.display='';
	}
}

function chosenAvatar() {
	scriptFolder = document.querySelector('input[name="avatarFolderName"]:checked').value;
	console.log(document.querySelector('input[name="avatarFolderName"]:checked').value);
	document.getElementById("nameForSaving").innerHTML = scriptFolder;
	document.getElementById("title").innerHTML += ": "+ capitalize(scriptFolder);
	document.getElementById("pageTitle").innerHTML += ": "+ capitalize(scriptFolder);
	scriptName = '../web-recorder/public/avatars/'+scriptFolder+'/script.json';
	console.log(scriptName);
	document.getElementById("selectPrevious").style.display="none";
	document.getElementById("recorder").style.display='';
	sendFileName();
	console.log("YES");
}

function nameAvatar() {
	var avatarName = document.getElementById("avatarName").value.toLowerCase();
	console.log(avatarName);
	console.log(scriptList);
	if($.inArray(avatarName, scriptList) != -1){
     	alert('Name already in use! Pick new name.');
	} else {
    	makeDirectory(avatarName);
    	document.getElementById("nameForSaving").innerHTML = avatarName;
    	document.getElementById("title").innerHTML += ": "+ capitalize(avatarName);
    	document.getElementById("pageTitle").innerHTML += ": "+ capitalize(avatarName);
    	document.getElementById("nameAvatar").style.display='none';
    	document.getElementById("scriptType").style.display='';
	}
}

function scriptOptions(){
	document.getElementById("selectScript").style.display="none";
	document.getElementById("recorder").style.display="";
	scriptName = document.querySelector('input[name="script"]:checked').value;
	if(scriptName === "scratch") {
		scriptName = '../web-recorder/public/template-scripts/template-empty.json';
	} else if(scriptName === "template-narrative") {
		scriptName = '../web-recorder/public/template-scripts/template-narrative.json';
	} else if (scriptName === "template-factual") {
		scriptName = '../web-recorder/public/template-scripts/template-factual.json';
	}
	console.log(scriptName);
	sendFileName();
	console.log("YO");
}

function goToRecorder() {
	window.location.replace("/");
}

function makeRadioButton(name, value, text) {
	var label = document.createElement("label");
	var radio = document.createElement("input");
	label.classList.add("scriptRadio");
	radio.type = "radio";
	radio.name = name;
	radio.value = value;
	label.appendChild(radio);
	label.appendChild(document.createTextNode(text));
	return label;
}

// Get the script names
function getScripts(){
	console.log("IN HERE");
	$.ajax({
		url: '/scripts',
		type: 'GET',
		datatype: 'json',
		error: function(data){
			alert("Oh No! Try a refresh?");
		},
		success: function(data){
			console.log("We have data!");
			console.log(data);
			console.log(typeof data );
			var data = JSON.parse(data);
			scriptList = data;
			console.log(data);
			var scriptForm = document.getElementById("previousAvatar");
			for (var i = 0; i < data.length; i++ ) {
				if (data[i] != ".DS_Store") {
					var scriptName = makeRadioButton("avatarFolderName",data[i],data[i]);
					scriptForm.appendChild(scriptName);
					scriptForm.innerHTML += "<br>";
				}
			}
			scriptForm.innerHTML += '<br> <input type="submit" value="Submit"></input>';
		}
	});
}

//getScripts();

$("#save-script").click(function() {
	var saveAvatar = {"name":document.getElementById("nameForSaving").innerHTML};
	$.ajax({
		url: '/saveAvatar',
		type: 'POST',
		data: JSON.stringify(saveAvatar),
		contentType: 'application/json; charset=utf-8',
		error: function(resp){
			console.log("Oh no...");
			console.log(resp);
		},
		success: function(resp){
			console.log('Sent folder name!');
			console.log(resp);
		}
	});
});

$(document).ready(function(){
	/*if (page === 'get all data'){
		getAllData();
	}*/
  //add new question and answer pair
  $("#add-question-button").click(function(){
		addNewEntry();
  });
});

$("#selectFiles").change(function() {
  filename = this.files[0].name;
  console.log(filename);
});



