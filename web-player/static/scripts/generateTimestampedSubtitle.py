import subprocess
import json
import os

# Generate timestamped WebVTT files based on

# JsonToVtt reads from all_characters.json and maps each sentence
# to webVTT format based on an equal spacing dividing total duration
# of the video.
# It will generate all the WebVTT files in the current directory

def JSONToWebVTT():
    f= open('all_characters.json', 'r')

    resp = json.load(f)
    for i in range (0, len(resp["rows"])-1, 1):
        if("question" in resp["rows"][i]["doc"].keys()):
            answer = json.dumps(resp["rows"][i]["doc"]["answer"]).strip('"')
            video = json.dumps(resp["rows"][i]["doc"]["video"]).strip('"')

            # change file extension of mp4 in video to vtt
            subtitle_file_name = os.path.splitext(video)[0] + '.vtt'
            cmd = "ffmpeg -i ../avatar-videos/" + video + " -f null - "
            video_duration = getDuration(cmd)
            sentence_number = getSentenceCount(answer)

            WebVTTString = composeWebVTT(answer,video_duration,sentence_number)
            writeWebVTT(subtitle_file_name,WebVTTString)

# Example command to run ffmpeg in command line
# cmd = "ffmpeg -i ../input.webm -f null - "

# getDuration returns the duration of each video in seconds
# We are taking the last two digits of seconds in time returned by ffmpeg command
# since all videos are within one minute long
def getDuration(cmd):
    args = cmd.split()

    process = subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=True)
    videoDuration = ""

    for line in process.stdout:

        if(line.find("time")!=-1 and line.find("times") == -1):
            # print(line)
            # print(line.split("time",1)[1][:9].strip("=")[6:])
            videoDuration = int(line.split("time",1)[1][:9].strip("=")[6:])
            # print("hello ",videoDuration)
        # if the video is missing we set the duration to be 59 seconds
        if videoDuration == "":
            videoDuration = 59

    return videoDuration

# Get number of sentences in one answer
# If we don't see period we set default count to 1
def getSentenceCount(answer):
    return answer.count(".") if answer.count(".")!=0 else 1

# Composes WebVTT based on the number of sentences and duration of video
def composeWebVTT(answer,video_duration,sentence_number):
    WebVTTString = "WEBVTT\n\n"
    sentences = answer.split('.')
    sentenceDuration = video_duration/sentence_number

    for num, sentence in enumerate (sentences):
        if(sentence):
            # zfill is used to pad single digit with left 0
            startTime = "00:" + str(sentenceDuration * num+1).zfill(2) + ".000"
            arrow = " --> "
            endTime = "00:" + str(sentenceDuration * (num+1)).zfill(2) + ".000"

            # If there is leading whitespace before the sentence we remove it
            sentence = sentence.lstrip()

            WebVTTString += startTime + arrow + endTime + "\n"
            WebVTTString += sentence + "\n\n"
    return WebVTTString

def writeWebVTT(subtitle_file_name,WebVTTString):
    with open(subtitle_file_name,'w') as file:
        file.write(WebVTTString)


JSONToWebVTT()
