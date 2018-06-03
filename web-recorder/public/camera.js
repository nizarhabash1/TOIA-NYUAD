var this_video_name;

var video = document.createElement('video');
video.controls = false;
var mediaElement = getHTMLMediaElement(video, {
  title: 'Recording status: inactive',
  buttons: ['full-screen'/*, 'take-snapshot'*/],
  showOnMouseEnter: false,
  width: 640,
  height:355,
  onTakeSnapshot: function() {
    var canvas = document.createElement('canvas');
    canvas.width = 640;
    canvas.height = 355;
    // flip the image horizontally for better user experience
    canvas.scale(-1,1);

    var context = canvas.getContext('2d');
    context.drawImage(recordingPlayer, 0, 0, canvas.width, canvas.height);

    window.open(canvas.toDataURL('image/png'));
  }
});
document.getElementById('recording-player').appendChild(mediaElement);

var div = document.createElement('section');
mediaElement.media.parentNode.appendChild(div);
div.appendChild(mediaElement.media);

var recordingPlayer = mediaElement.media;
var recordingMedia = document.querySelector('.recording-media');
var mediaContainerFormat = document.querySelector('.media-container-format');
var mimeType = 'video/webm';
var fileExtension = 'webm';
var type = 'video';
var recorderType;
var defaultWidth;
var defaultHeight;


var question_index = 0;

var btnStartRecording = document.querySelector('#btn-start-recording');

window.onbeforeunload = function() {
  btnStartRecording.disabled = false;
  recordingMedia.disabled = false;
  mediaContainerFormat.disabled = false;
};

var gumVideo = document.querySelector('video#gum');

var constraints = {
  audio: true,
  video: true
};

function handleSuccess(stream) {
  recordButton.disabled = false;
  console.log('getUserMedia() got stream: ', stream);
  window.stream = stream;
  recordingPlayer.srcObject = stream;
}

function handleError(error) {
  console.log('navigator.getUserMedia error: ', error);
}

navigator.mediaDevices.getUserMedia(constraints).
then(handleSuccess).catch(handleError);


btnStartRecording.onclick = function(event) {

  var button = btnStartRecording;
  $("#face-outline").show();

  if(button.innerHTML === 'Stop Recording') {
    btnPauseRecording.style.display = 'none';
    button.disabled = true;
    button.disableStateWaiting = true;
    setTimeout(function() {
      button.disabled = false;
      button.disableStateWaiting = false;
    }, 2000);

    button.innerHTML = 'Start Recording';

    function stopStream() {
      if(button.stream && button.stream.stop) {
        button.stream.stop();
        button.stream = null;
      }

      if(button.stream instanceof Array) {
        button.stream.forEach(function(stream) {
          stream.stop();
        });
        button.stream = null;
      }

      videoBitsPerSecond = null;
      var html = 'Recording status: stopped';
      html += '<br>Size: ' + bytesToSize(button.recordRTC.getBlob().size);
      recordingPlayer.parentNode.parentNode.querySelector('h2').innerHTML = html;
    }

    if(button.recordRTC) {
      if(button.recordRTC.length) {
        button.recordRTC[0].stopRecording(function(url) {
          if(!button.recordRTC[1]) {
            button.recordingEndedCallback(url);
            stopStream();

            saveToDiskOrOpenNewTab(button.recordRTC[0]);
            return;
          }

          button.recordRTC[1].stopRecording(function(url) {
            button.recordingEndedCallback(url);
            stopStream();
          });
        });
      }
      else {
        button.recordRTC.stopRecording(function(url) {
          if(button.blobs && button.blobs.length) {
            var blob = new File(button.blobs, getFileName(fileExtension), {
              type: mimeType
            });

            button.recordRTC.getBlob = function() {
              return blob;
            };

            url = URL.createObjectURL(blob);
          }

          button.recordingEndedCallback(url);
          saveToDiskOrOpenNewTab(button.recordRTC);
          stopStream();
        });
      }
    }

    return;
  }

  if(!event) return;

  button.disabled = true;

  var commonConfig = {
    onMediaCaptured: function(stream) {
      button.stream = stream;
      if(button.mediaCapturedCallback) {
        button.mediaCapturedCallback();
      }

      button.innerHTML = 'Stop Recording';
      button.disabled = false;
    },
    onMediaStopped: function() {
      button.innerHTML = 'Start Recording';

      if(!button.disableStateWaiting) {
        button.disabled = false;
      }
    },
    onMediaCapturingFailed: function(error) {
      console.error('onMediaCapturingFailed:', error);

      if(error.toString().indexOf('no audio or video tracks available') !== -1) {
        alert('RecordRTC failed to start because there are no audio or video tracks available.');
      }

      if(DetectRTC.browser.name === 'Safari') return;

      if(error.name === 'PermissionDeniedError' && DetectRTC.browser.name === 'Firefox') {
        alert('Firefox requires version >= 52. Firefox also requires HTTPs.');
      }

      commonConfig.onMediaStopped();
    }
  };

  if(mediaContainerFormat.value === 'h264') {
    mimeType = 'video/webm\;codecs=h264';
    fileExtension = 'mp4';

    // video/mp4;codecs=avc1
    if(isMimeTypeSupported('video/mpeg')) {
      mimeType = 'video/mpeg';
    }
  }

  if(mediaContainerFormat.value === 'mkv' && isMimeTypeSupported('video/x-matroska;codecs=avc1')) {
    mimeType = 'video/x-matroska;codecs=avc1';
    fileExtension = 'mkv';
  }

  if(mediaContainerFormat.value === 'vp8' && isMimeTypeSupported('video/webm\;codecs=vp8')) {
    mimeType = 'video/webm\;codecs=vp8';
    fileExtension = 'webm';
    recorderType = null;
    type = 'video';
  }

  if(mediaContainerFormat.value === 'vp9' && isMimeTypeSupported('video/webm\;codecs=vp9')) {
    mimeType = 'video/webm\;codecs=vp9';
    fileExtension = 'webm';
    recorderType = null;
    type = 'video';
  }

  if(mediaContainerFormat.value === 'pcm') {
    mimeType = 'audio/wav';
    fileExtension = 'wav';
    recorderType = StereoAudioRecorder;
    type = 'audio';
  }

  if(mediaContainerFormat.value === 'opus' || mediaContainerFormat.value === 'ogg') {
    if(isMimeTypeSupported('audio/webm')) {
      mimeType = 'audio/webm';
      fileExtension = 'webm'; // webm
    }

    if(isMimeTypeSupported('audio/ogg')) {
      mimeType = 'audio/ogg; codecs=opus';
      fileExtension = 'ogg'; // ogg
    }

    recorderType = null;
    type = 'audio';
  }

  if(mediaContainerFormat.value === 'whammy') {
    mimeType = 'video/webm';
    fileExtension = 'webm';
    recorderType = WhammyRecorder;
    type = 'video';
  }

  if(mediaContainerFormat.value === 'gif') {
    mimeType = 'image/gif';
    fileExtension = 'gif';
    recorderType = GifRecorder;
    type = 'gif';
  }

  if(mediaContainerFormat.value === 'default') {
    // mimeType = 'video/webm';
    // fileExtension = 'webm';
    // recorderType = null;
    // type = 'video';
    mimeType: 'video/mp4; codecs="mpeg4, aac"';
    fileExtension = 'mp4';
    recorderType = null;
    type = 'video';
  }

  if(recordingMedia.value === 'record-audio') {
    captureAudio(commonConfig);

    button.mediaCapturedCallback = function() {
      var options = {
        type: type,
        mimeType: mimeType,
        leftChannel: params.leftChannel || false,
        disableLogs: params.disableLogs || false
      };

      if(params.sampleRate) {
        options.sampleRate = parseInt(params.sampleRate);
      }

      if(params.bufferSize) {
        options.bufferSize = parseInt(params.bufferSize);
      }

      if(recorderType) {
        options.recorderType = recorderType;
      }

      if(videoBitsPerSecond) {
        options.videoBitsPerSecond = videoBitsPerSecond;
      }

      if(DetectRTC.browser.name === 'Edge') {
        options.numberOfAudioChannels = 1;
      }

      options.ignoreMutedMedia = false;
      button.recordRTC = RecordRTC(button.stream, options);

      button.recordingEndedCallback = function(url) {
        setVideoURL(url);
      };

      button.recordRTC.startRecording();
      btnPauseRecording.style.display = '';
    };
  }

  if(recordingMedia.value === 'record-audio-plus-video') {
    captureAudioPlusVideo(commonConfig);

    button.mediaCapturedCallback = function() {
      if(typeof MediaRecorder === 'undefined') { // opera or chrome etc.
        button.recordRTC = [];

        if(!params.bufferSize) {
          // it fixes audio issues whilst recording 720p
          // CHANGED: added two zeros at the end
          params.bufferSize = 1638400;
        }

        var options = {
          type: 'audio', // hard-code to set "audio"
          leftChannel: params.leftChannel || false,
          disableLogs: params.disableLogs || false,
          video: recordingPlayer
        };

        if(params.sampleRate) {
          options.sampleRate = parseInt(params.sampleRate);
        }

        if(params.bufferSize) {
          options.bufferSize = parseInt(params.bufferSize);
        }

        if(params.frameInterval) {
          options.frameInterval = parseInt(params.frameInterval);
        }

        if(recorderType) {
          options.recorderType = recorderType;
        }

        if(videoBitsPerSecond) {
          options.videoBitsPerSecond = videoBitsPerSecond;
        }

        options.ignoreMutedMedia = false;
        var audioRecorder = RecordRTC(button.stream, options);

        options.type = type;
        var videoRecorder = RecordRTC(button.stream, options);

        // to sync audio/video playbacks in browser!
        videoRecorder.initRecorder(function() {
          audioRecorder.initRecorder(function() {
            audioRecorder.startRecording();
            videoRecorder.startRecording();
            btnPauseRecording.style.display = '';
          });
        });

        button.recordRTC.push(audioRecorder, videoRecorder);

        button.recordingEndedCallback = function() {
          var audio = new Audio();
          audio.src = audioRecorder.toURL();
          audio.controls = true;
          audio.autoplay = true;

          recordingPlayer.parentNode.appendChild(document.createElement('hr'));
          recordingPlayer.parentNode.appendChild(audio);

          if(audio.paused) audio.play();
        };
        return;
      }

      var options = {
        type: type,
        mimeType: mimeType,
        disableLogs: params.disableLogs || false,
        getNativeBlob: false, // enable it for longer recordings
        video: recordingPlayer
      };

      if(recorderType) {
        options.recorderType = recorderType;

        if(recorderType == WhammyRecorder || recorderType == GifRecorder) {
          options.canvas = options.video = {
            // UPDATE TO YOUR OWN RESOLUTION NEEDED
            width: defaultWidth || 1920,
            height: defaultHeight || 1080
          };
        }
      }

      if(videoBitsPerSecond) {
        options.videoBitsPerSecond = videoBitsPerSecond;
      }

      if(timeSlice && typeof MediaRecorder !== 'undefined') {
        options.timeSlice = timeSlice;
        button.blobs = [];
        options.ondataavailable = function(blob) {
          button.blobs.push(blob);
        };
      }

      options.ignoreMutedMedia = false;
      button.recordRTC = RecordRTC(button.stream, options);

      button.recordingEndedCallback = function(url) {
        setVideoURL(url);
      };

      button.recordRTC.startRecording();
      btnPauseRecording.style.display = '';
      recordingPlayer.parentNode.parentNode.querySelector('h2').innerHTML = '<img src="https://cdn.webrtc-experiment.com/images/progress.gif">';
    };
  }
}

function captureAudioPlusVideo(config) {
  captureUserMedia({video: true, audio: true}, function(audioVideoStream) {
    config.onMediaCaptured(audioVideoStream);

    if(audioVideoStream instanceof Array) {
      audioVideoStream.forEach(function(stream) {
        addStreamStopListener(stream, function() {
          config.onMediaStopped();
        });
      });
      return;
    }

    addStreamStopListener(audioVideoStream, function() {
      config.onMediaStopped();
    });
  }, function(error) {
    config.onMediaCapturingFailed(error);
  });
}


var videoBitsPerSecond;

function setVideoBitrates() {
  var select = document.querySelector('.media-bitrates');
  var value = select.value;

  if(value == 'default') {
    videoBitsPerSecond = null;
    return;
  }

  videoBitsPerSecond = parseInt(value);
}

function getFrameRates(mediaConstraints) {
  if(!mediaConstraints.video) {
    return mediaConstraints;
  }

  var select = document.querySelector('.media-framerates');
  var value = select.value;

  if(value == 'default') {
    return mediaConstraints;
  }

  value = parseInt(value);

  if(DetectRTC.browser.name === 'Firefox') {
    mediaConstraints.video.frameRate = value;
    return mediaConstraints;
  }

  if(!mediaConstraints.video.mandatory) {
    mediaConstraints.video.mandatory = {};
    mediaConstraints.video.optional = [];
  }

  var isScreen = recordingMedia.value.toString().toLowerCase().indexOf('screen') != -1;
  if(isScreen) {
    mediaConstraints.video.mandatory.maxFrameRate = value;
  }
  else {
    mediaConstraints.video.mandatory.minFrameRate = value;
  }

  return mediaConstraints;
}

function setGetFromLocalStorage(selectors) {
  selectors.forEach(function(selector) {
    var storageItem = selector.replace(/\.|#/g, '');
    if(localStorage.getItem(storageItem)) {
      document.querySelector(selector).value = localStorage.getItem(storageItem);
    }

    addEventListenerToUploadLocalStorageItem(selector, ['change', 'blur'], function() {
      localStorage.setItem(storageItem, document.querySelector(selector).value);
    });
  });
}

function addEventListenerToUploadLocalStorageItem(selector, arr, callback) {
  arr.forEach(function(event) {
    document.querySelector(selector).addEventListener(event, callback, false);
  });
}

setGetFromLocalStorage(['.media-resolutions', '.media-framerates', '.media-bitrates', '.recording-media', '.media-container-format']);

function getVideoResolutions(mediaConstraints) {
  if(!mediaConstraints.video) {
    return mediaConstraints;
  }

  // var select = document.querySelector('.media-resolutions');
  // var value = select.value;

  // UPDATE TO YOUR OWN RESOLUTION
  var value = "1920x1080";
  // var value = "640x480";
  // var value = "1280x720";


  // console.log("Our media constraint value is!!! " + select.value);

  if(value == 'default') {
    return mediaConstraints;
  }

  value = value.split('x');

  if(value.length != 2) {
    return mediaConstraints;
  }

  defaultWidth = parseInt(value[0]);
  defaultHeight = parseInt(value[1]);

  if(DetectRTC.browser.name === 'Firefox') {
    mediaConstraints.video.width = defaultWidth;
    mediaConstraints.video.height = defaultHeight;
    return mediaConstraints;
  }

  if(!mediaConstraints.video.mandatory) {
    mediaConstraints.video.mandatory = {};
    mediaConstraints.video.optional = [];
  }

  var isScreen = recordingMedia.value.toString().toLowerCase().indexOf('screen') != -1;

  if(isScreen) {
    mediaConstraints.video.mandatory.maxWidth = defaultWidth;
    mediaConstraints.video.mandatory.maxHeight = defaultHeight;
  }
  else {
    mediaConstraints.video.mandatory.minWidth = defaultWidth;
    mediaConstraints.video.mandatory.minHeight = defaultHeight;
  }

  return mediaConstraints;
}

function captureUserMedia(mediaConstraints, successCallback, errorCallback) {
  if(mediaConstraints.video == true) {
    mediaConstraints.video = {};
  }

  setVideoBitrates();

  mediaConstraints = getVideoResolutions(mediaConstraints);
  mediaConstraints = getFrameRates(mediaConstraints);

  var isBlackBerry = !!(/BB10|BlackBerry/i.test(navigator.userAgent || ''));
  if(isBlackBerry && !!(navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia)) {
    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
    navigator.getUserMedia(mediaConstraints, successCallback, errorCallback);
    return;
  }

  navigator.mediaDevices.getUserMedia(mediaConstraints).then(function(stream) {
    successCallback(stream);

    setVideoURL(stream, true);
  }).catch(function(error) {
    if(error && error.name === 'ConstraintNotSatisfiedError') {
      alert('Your camera or browser does NOT supports selected resolutions or frame-rates. \n\nPlease select "default" resolutions.');
    }

    errorCallback(error);
  });
}

function setMediaContainerFormat(arrayOfOptionsSupported) {
  var options = Array.prototype.slice.call(
    mediaContainerFormat.querySelectorAll('option')
  );

  var localStorageItem;
  if(localStorage.getItem('media-container-format')) {
    localStorageItem = localStorage.getItem('media-container-format');
  }

  var selectedItem;
  options.forEach(function(option) {
    option.disabled = true;

    if(arrayOfOptionsSupported.indexOf(option.value) !== -1) {
      option.disabled = false;

      if(localStorageItem && arrayOfOptionsSupported.indexOf(localStorageItem) != -1) {
        if(option.value != localStorageItem) return;
        option.selected = true;
        selectedItem = option;
        return;
      }

      if(!selectedItem) {
        option.selected = true;
        selectedItem = option;
      }
    }
  });
}

function isMimeTypeSupported(mimeType) {
  if(DetectRTC.browser.name === 'Edge' || DetectRTC.browser.name === 'Safari' || typeof MediaRecorder === 'undefined') {
    return false;
  }

  if(typeof MediaRecorder.isTypeSupported !== 'function') {
    return true;
  }

  return MediaRecorder.isTypeSupported(mimeType);
}

recordingMedia.onchange = function() {
  if(recordingMedia.value === 'record-audio') {
    var recordingOptions = [];

    if(isMimeTypeSupported('audio/webm')) {
      recordingOptions.push('opus');
    }

    if(isMimeTypeSupported('audio/ogg')) {
      recordingOptions.push('ogg');
    }

    recordingOptions.push('pcm');

    setMediaContainerFormat(recordingOptions);
    return;
  }

  var isChrome = !!window.chrome && !(!!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0);

  var recordingOptions = ['vp8']; // MediaStreamRecorder with vp8

  if(isMimeTypeSupported('video/webm\;codecs=vp9')) {
    recordingOptions.push('vp9'); // MediaStreamRecorder with vp9
  }

  if(isMimeTypeSupported('video/webm\;codecs=h264')) {
    recordingOptions.push('h264'); // MediaStreamRecorder with h264
  }

  if(isMimeTypeSupported('video/x-matroska;codecs=avc1')) {
    recordingOptions.push('mkv'); // MediaStreamRecorder with mkv/matroska
  }

  recordingOptions.push('gif'); // GifRecorder

  if(isChrome) {
    recordingOptions.push('whammy'); // WhammyRecorder
  }

  recordingOptions.push('default'); // Default mimeType for MediaStreamRecorder

  setMediaContainerFormat(recordingOptions);
};
recordingMedia.onchange();

function stringify(obj) {
  var result = '';
  Object.keys(obj).forEach(function(key) {
    if(typeof obj[key] === 'function') {
      return;
    }

    if(result.length) {
      result += ',';
    }

    result += key + ': ' + obj[key];
  });

  return result;
}

function mediaRecorderToStringify(mediaRecorder) {
  var result = '';
  result += 'mimeType: ' + mediaRecorder.mimeType;
  result += ', state: ' + mediaRecorder.state;
  result += ', audioBitsPerSecond: ' + mediaRecorder.audioBitsPerSecond;
  result += ', videoBitsPerSecond: ' + mediaRecorder.videoBitsPerSecond;
  if(mediaRecorder.stream) {
    result += ', streamid: ' + mediaRecorder.stream.id;
    result += ', stream-active: ' + mediaRecorder.stream.active;
  }
  return result;
}

function getFailureReport() {
  var info = 'RecordRTC seems failed. \n\n' + stringify(DetectRTC.browser) + '\n\n' + DetectRTC.osName + ' ' + DetectRTC.osVersion + '\n';

  if (typeof recorderType !== 'undefined' && recorderType) {
    info += '\nrecorderType: ' + recorderType.name;
  }

  if (typeof mimeType !== 'undefined') {
    info += '\nmimeType: ' + mimeType;
  }

  Array.prototype.slice.call(document.querySelectorAll('select')).forEach(function(select) {
    info += '\n' + (select.id || select.className) + ': ' + select.value;
  });

  if (btnStartRecording.recordRTC) {
    info += '\n\ninternal-recorder: ' + btnStartRecording.recordRTC.getInternalRecorder().name;

    if(btnStartRecording.recordRTC.getInternalRecorder().getAllStates) {
      info += '\n\nrecorder-states: ' + btnStartRecording.recordRTC.getInternalRecorder().getAllStates();
    }
  }

  if(btnStartRecording.stream) {
    info += '\n\naudio-tracks: ' + btnStartRecording.stream.getAudioTracks().length;
    info += '\nvideo-tracks: ' + btnStartRecording.stream.getVideoTracks().length;
    info += '\nstream-active? ' + !!btnStartRecording.stream.active;

    btnStartRecording.stream.getAudioTracks().concat(btnStartRecording.stream.getVideoTracks()).forEach(function(track) {
      info += '\n' + track.kind + '-track-' + (track.label || track.id) + ': (enabled: ' + !!track.enabled + ', readyState: ' + track.readyState + ', muted: ' + !!track.muted + ')';

      if(track.getConstraints && Object.keys(track.getConstraints()).length) {
        info += '\n' + track.kind + '-track-getConstraints: ' + stringify(track.getConstraints());
      }

      if(track.getSettings && Object.keys(track.getSettings()).length) {
        info += '\n' + track.kind + '-track-getSettings: ' + stringify(track.getSettings());
      }
    });
  }

  if(timeSlice && btnStartRecording.recordRTC) {
    info += '\ntimeSlice: ' + timeSlice;

    if(btnStartRecording.recordRTC.getInternalRecorder().getArrayOfBlobs) {
      var blobSizes = [];
      btnStartRecording.recordRTC.getInternalRecorder().getArrayOfBlobs().forEach(function(blob) {
        blobSizes.push(blob.size);
      });
      info += '\nblobSizes: ' + blobSizes;
    }
  }

  else if(btnStartRecording.recordRTC && btnStartRecording.recordRTC.getBlob()) {
    info += '\n\nblobSize: ' + bytesToSize(btnStartRecording.recordRTC.getBlob().size);
  }

  if(btnStartRecording.recordRTC && btnStartRecording.recordRTC.getInternalRecorder() && btnStartRecording.recordRTC.getInternalRecorder().getInternalRecorder && btnStartRecording.recordRTC.getInternalRecorder().getInternalRecorder()) {
    info += '\n\ngetInternalRecorder: ' + mediaRecorderToStringify(btnStartRecording.recordRTC.getInternalRecorder().getInternalRecorder());
  }

  return info;
}

function saveToDiskOrOpenNewTab(recordRTC) {
  if(!recordRTC.getBlob().size) {
    var info = getFailureReport();
    console.log('blob', recordRTC.getBlob());
    console.log('recordrtc instance', recordRTC);
    console.log('report', info);

    if(mediaContainerFormat.value !== 'default') {
      alert('RecordRTC seems failed recording using ' + mediaContainerFormat.value + '. Please choose "default" option from the drop down and record again.');
    }
    else {
      alert('RecordRTC seems failed. Unexpected issue. You can read the email in your console log. \n\nPlease report using disqus chat below.');
    }

    if(mediaContainerFormat.value !== 'vp9' && DetectRTC.browser.name === 'Chrome') {
      alert('Please record using VP9 encoder. (select from the dropdown)');
    }
  }

  var fileName = getFileName(fileExtension);

  document.querySelector('#save-to-disk').parentNode.style.display = 'block';
  document.querySelector('#save-to-disk').onclick = function() {
    if(!recordRTC) return alert('No recording found.');

    var theObj = _.find(allData, function(d){
      return d.index == current_selection_id;
    });


    /* getting the unique id for each entry from cloudant */
    var database_unique_id = theObj._id;

    // this_video_name= "margarita_" + current_selection_id +
    //         "_"+ database_unique_id + ".mp4";

    /* We need to update background based on the question just saved */
    /* We update the boolean value if we save a video */

    finished_video_id = current_selection_id;
    /* update the corresponding value in allData */
    var clicked_index_in_allData = allData.indexOf(theObj);

    allData[clicked_index_in_allData]["video_saved"] = true;

    var file = new File([recordRTC.getBlob()], this_video_name, {
      type: mimeType
    });

    invokeSaveAsDialog(file, file.name);

  };
}

// change this function!
function getFileName(fileExtension) {
  var d = new Date();
  var year = d.getUTCFullYear();
  var month = d.getUTCMonth();
  var date = d.getUTCDate();
  return 'RecordRTC-' + year + month + date + '-' + getRandomString() + '.' + fileExtension;
}

function SaveFileURLToDisk(fileUrl, fileName) {
  var hyperlink = document.createElement('a');
  hyperlink.href = fileUrl;
  hyperlink.target = '_blank';
  hyperlink.download = fileName || fileUrl;

  (document.body || document.documentElement).appendChild(hyperlink);
  hyperlink.onclick = function() {
    (document.body || document.documentElement).removeChild(hyperlink);

    // required for Firefox
    window.URL.revokeObjectURL(hyperlink.href);
  };

  var mouseEvent = new MouseEvent('click', {
    view: window,
    bubbles: true,
    cancelable: true
  });

  hyperlink.dispatchEvent(mouseEvent);
}

function getURL(arg) {
  var url = arg;

  if(arg instanceof Blob || arg instanceof File) {
    url = URL.createObjectURL(arg);
  }

  if(arg instanceof RecordRTC || arg.getBlob) {
    url = URL.createObjectURL(arg.getBlob());
  }

  if(arg instanceof MediaStream || arg.getTracks || arg.getVideoTracks || arg.getAudioTracks) {
    // url = URL.createObjectURL(arg);
  }

  return url;
}

function setVideoURL(arg, forceNonImage) {
  console.log("we are setting the video url as " + arg);
  var url = getURL(arg);

  var parentNode = recordingPlayer.parentNode;
  parentNode.removeChild(recordingPlayer);
  parentNode.innerHTML = '';

  var elem = 'video';
  if(type == 'gif' && !forceNonImage) {
    elem = 'img';
  }
  if(type == 'audio') {
    elem = 'audio';
  }

  recordingPlayer = document.createElement(elem);

  if(arg instanceof MediaStream) {
    recordingPlayer.muted = true;
  }

  recordingPlayer.addEventListener('loadedmetadata', function() {
    if(navigator.userAgent.toLowerCase().indexOf('android') == -1) return;

    // android
    setTimeout(function() {
      if(typeof recordingPlayer.play === 'function') {
        recordingPlayer.play();
      }
    }, 2000);
  }, false);

  recordingPlayer.poster = '';

  if(arg instanceof MediaStream) {
    recordingPlayer.srcObject = arg;
  }
  else {
    console.log("OUR RECORDER SOURCE IS A URL: " + url);
    recordingPlayer.src = url;
    /* add an if statement here to check the selected is a thing but not a button */
    /* from current_selection_id we need to find the id in allData */
    var theObj = _.find(allData, function(d){
      return d.index == current_selection_id;
    });

    var clicked_index_in_allData = allData.indexOf(theObj);
    /* display the corresponding playbackbutton button */
    // allData[clicked_index_in_allData].blob=url;
    // $('#blob_'+current_selection_id).show();
    console.log("we updated " + "question " + current_selection_id + " with url " + url);
  }

  if(typeof recordingPlayer.play === 'function') {
    recordingPlayer.play();
  }

  recordingPlayer.addEventListener('ended', function() {
    url = getURL(arg);

    if(arg instanceof MediaStream) {
      recordingPlayer.srcObject = arg;
    }
    else {
      recordingPlayer.src = url;
    }

    // ADDED funciontality of streaming after a playback
    // navigator.mediaDevices.getUserMedia(constraints).
    //     then(handleSuccess).catch(handleError);
  });
  // ADDED ends

  parentNode.appendChild(recordingPlayer);
}
