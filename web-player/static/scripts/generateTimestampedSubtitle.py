import subprocess
import json
import os
import math

# Generate timestamped WebVTT files based on word counts in each sentence

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

            # print("duration of the video is ")
            # print(video_duration)

            sentence_number = getSentenceCount(answer)

            sentence_proportions = proportion_time_for_sentences(wordCountInSentences(answer))
            sentence_durations = duration_each_sentence(sentence_proportions, video_duration)
            sentence_durations = duration_from_start_each_sentence(sentence_durations)
            # print("duration of each sentence is ")
            # print(sentence_durations)

            WebVTTString = composeWebVTT(answer, sentence_durations)
            # WebVTTString = composeWebVTT(answer,video_duration,sentence_number)
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

# Return an array of integers for number of words in each sentences of the answer
def wordCountInSentences(answer):
    word_counts = []
    sentences = answer.split('.')
    for sentence in sentences:
        if sentence != "":
            words = sentence.split(' ')
            word_counts.append(len(words))
    # print(word_counts)
    return word_counts

# Return an array of float for how much proportion each sentence should take as compared to the whole
def proportion_time_for_sentences(word_counts):
    total_words = sum(word_counts)
    sentence_proportions = []
    for word_count in word_counts:
        sentence_proportions.append(float(word_count)/float(total_words))
    # print(sentence_proportions)
    return sentence_proportions

# Return the duration of each sentence according to how many words it has
def duration_each_sentence(sentence_proportions, video_duration):
    sentence_durations = []
    for sentence_proprotion in sentence_proportions:
        sentence_durations.append(int(round(sentence_proprotion * video_duration)))
    return sentence_durations

# Return the duration of each sentence counting from the start
def duration_from_start_each_sentence(sentence_durations):
    for i in range(len(sentence_durations)):
        if i > 0:
            sentence_durations[i] = sentence_durations[i] + sentence_durations[i-1]
    return sentence_durations


# Composes WebVTT based on the number of sentences and duration of video
def composeWebVTT(answer, sentence_durations):
    WebVTTString = "WEBVTT\n\n"
    sentences = answer.split('.')

    # Filter out the empty strings
    sentences = list(filter(lambda s: s is not "" and s is not "\n", sentences))

    #print("len(sentences): {0}, len(sentence_durations): {1}".format(len(sentences), len(sentence_durations)))

    for num, sentence in enumerate (sentences):
        if(sentence):
            # print(sentence_durations[num])
            # zfill is used to pad single digit with left 0
            #print(num)
            startTime = "00:" + str(sentence_durations[num-1]).zfill(2) + ".000" if num != 0 else "00:00.000"
            arrow = " --> "
            endTime = "00:" + str(sentence_durations[num]).zfill(2) + ".000"

            # If there is leading whitespace before the sentence we remove it
            sentence = sentence.lstrip()

            WebVTTString += startTime + arrow + endTime + "\n"
            WebVTTString += sentence + "\n\n"

    return WebVTTString

# # Composes WebVTT based on the number of sentences and duration of video
# def composeWebVTT(answer,video_duration,sentence_number):
#     WebVTTString = "WEBVTT\n\n"
#     sentences = answer.split('.')
#     sentenceDuration = video_duration/sentence_number
#
#     for num, sentence in enumerate (sentences):
#         if(sentence):
#             # zfill is used to pad single digit with left 0
#             startTime = "00:" + str(sentenceDuration * num+1).zfill(2) + ".000"
#             arrow = " --> "
#             endTime = "00:" + str(sentenceDuration * (num+1)).zfill(2) + ".000"
#
#             # If there is leading whitespace before the sentence we remove it
#             sentence = sentence.lstrip()
#
#             WebVTTString += startTime + arrow + endTime + "\n"
#             WebVTTString += sentence + "\n\n"
#     return WebVTTString

def writeWebVTT(subtitle_file_name,WebVTTString):
    with open(subtitle_file_name,'w') as file:
        file.write(WebVTTString)


JSONToWebVTT()
