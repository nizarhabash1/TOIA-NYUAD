var recordButton = document.getElementById("record-button");
var playButton = document.getElementById("play-button");
var pauseButton = document.getElementById("pause-button");
var stopButton = document.getElementById("stop-button");
var downloadButton = document.getElementById("download-button");
var saveButton = document.getElementById("saveButton");



recordButton.onclick = function () {
	// buttonsStateRecording;
	if(current_selection_id == null){
		alert("Please choose a question first");
	}
	else{
		recordButton.style.display = "none";
		playButton.style.display = "none";
		pauseButton.style.display = "none";
		// downloadButton.style.display = "none";
		stopButton.style.display = "inline"; 
		$("#btn-start-recording").trigger('click');
		// $("#recording-gif").show();
	}

};
stopButton.onclick = function () {
	// buttonsStateStopped; 
	recordButton.style.display = "inline";
	playButton.style.display = "none";
	// downloadButton.style.display = "inline";
	pauseButton.style.display = "none";
	stopButton.style.display = "none"; 
	// $("#recording-gif").hide();

};
playButton.onclick = function () {
	// buttonsStatePlaying;
	recordButton.style.display = "inline";
	playButton.style.display = "none";
	pauseButton.style.display = "inline";
	stopButton.style.display = "none"; 
};
pauseButton.onclick = function () {
	// buttonsStateStopped; 
	recordButton.style.display = "inline";
	playButton.style.display = "inline";
	pauseButton.style.display = "none";
	stopButton.style.display = "none"; 
};


// $('#record-button').click(function(event){
//     $("#btn-start-recording").trigger('click');
// })
var btnStartRecording = document.querySelector('#btn-start-recording');
var button = btnStartRecording;

$('#stop-button').click(function(event){
    if(button.innerHTML === 'Stop Recording'){
        $("#btn-start-recording").trigger('click');
    }
});

$('#play-button').click(function(event){
    recordingPlayer.play();
});
$('#pause-button').click(function(event){
    recordingPlayer.pause();
});
