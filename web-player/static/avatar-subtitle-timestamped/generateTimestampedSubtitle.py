
# -*- coding: utf-8 -*-

import subprocess
import json
import os
import codecs
import math


# Generate timestamped WebVTT files based on word counts in each sentence

# JsonToVtt reads from all_characters.json and maps each sentence
# to webVTT format based on an equal spacing dividing total duration
# of the video.
# It will generate all the WebVTT files in the current directory

def JSONToWebVTT():
    f = open('all_characters.json', 'r', encoding='utf-8')
    resp = json.load(f)
    for i in range(0, len(resp["rows"]) - 1, 1):
        if "arabic-answer" in resp["rows"][i]["doc"].keys():

            answer = json.dumps(resp["rows"][i]["doc"]["arabic-answer"].strip('"'), ensure_ascii=False)

            video = json.dumps(resp["rows"][i]["doc"]["video"]).strip('"')

            # change file extension of mp4 in video to vtt
            subtitle_file_name = 'arabic_' + os.path.splitext(video)[0] + '.vtt'
            cmd = "ffmpeg -i ../avatar-videos/" + video + " -f null - "
            video_duration = getDuration(cmd)

            # print("duration of the video is ")
            # print(video_duration)

            number_of_word = total_word_count(answer)
            number_of_segment = int(number_of_word/12)+1
            segment_duration = video_duration/number_of_segment
            # print("the segment duration is")
            # print(segment_duration)
            #
            # print(answer)
            # print(number_of_segment)

            WebVTTString = composeWebVTT(answer, segment_duration, number_of_segment,subtitle_file_name)

            writeWebVTT(subtitle_file_name, WebVTTString)


# Example command to run ffmpeg in command line
# cmd = "ffmpeg -i ../input.webm -f null - "

# getDuration returns the duration of each video in seconds
# We are taking the last two digits of seconds in time returned by ffmpeg command
# since all videos are within one minute long
def getDuration(cmd):
    args = cmd.split()

    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    videoDuration = ""

    for line in process.stdout:

        if (line.find("time") != -1 and line.find("times") == -1):
            # print(line)
            # print(line.split("time",1)[1][:9].strip("=")[6:])
            videoDuration = int(line.split("time", 1)[1][:9].strip("=")[6:])
            # print("hello ",videoDuration)
        # if the video is missing we set the duration to be 59 seconds
        if videoDuration == "":
            videoDuration = 59

    return videoDuration


def total_word_count(answer):
    return len(answer.split())-1


# Composes WebVTT based on the number of sentences and duration of video
def composeWebVTT(answer, segment_duration, number_of_segment,subtitle_file_name):
    WebVTTString = "WEBVTT\n\n"
    #print(answer)
    answer = answer.split()
    splitted_answer = []

    for i in range(number_of_segment):
        splitted_answer.append("")
    n = 12
    for i in range (0, len(answer)):
        answer[i] = answer[i] + " "
        splitted_answer[int(i/12)] += answer[i]

    # print("The splitted answer is ")
    # print(splitted_answer)

    # print("len(sentences): {0}, len(sentence_durations): {1}".format(len(sentences), len(sentence_durations)))
    # with codecs.open(subtitle_file_name, 'w', encoding='utf-8') as file:
    #     splitted_answer[0] = u''+ splitted_answer[0]
    #     file.write(splitted_answer[0])

    for num, one_segment in enumerate(splitted_answer):
        if one_segment:
            # print(sentence_durations[num])
            # zfill is used to pad single digit with left 0
            # print(num)
            startTime = "00:" + str(int(segment_duration * num)).zfill(2) + ".000" if num != 0 else "00:00.000"
            arrow = " --> "
            endTime = "00:" + str(int(segment_duration * (num+1))).zfill(2) + ".000"

            # If there is leading whitespace before the sentence we remove it
            one_segment = one_segment.lstrip()

            WebVTTString += startTime + arrow + endTime + "\n"
            WebVTTString += one_segment + "\n\n"



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

def writeWebVTT(subtitle_file_name, WebVTTString):
    with open(subtitle_file_name, 'wb') as file:
        WebVTTString = WebVTTString.strip('"')
        file.write(WebVTTString.encode('utf-8'))


JSONToWebVTT()
