# -*- coding: utf-8 -*-

# Generate timestamped WebVTT subtitles displaying at most 12 words at a time

# JsonToVtt reads from all_characters.json and generates subtitles
# by dividing each answer into 12 words segments and mapping
# them with equal amount of time over the total duration of video

# It will generate all the WebVTT files in the current directory

import subprocess
import json
import os

num_of_word_in_segment = 12


def json_to_webvtt():
    f = open('all_characters.json', 'r', encoding='utf-8')
    resp = json.load(f)
    for i in range(0, len(resp["rows"]) - 1, 1):
        if "arabic-answer" in resp["rows"][i]["doc"].keys():

            answer = json.dumps(resp["rows"][i]["doc"]["arabic-answer"].strip('"'), ensure_ascii=False)

            video = json.dumps(resp["rows"][i]["doc"]["video"]).strip('"')

            # change file extension of mp4 in video to vtt
            subtitle_file_name = 'arabic_' + os.path.splitext(video)[0] + '.vtt'
            cmd = "ffmpeg -i ../avatar-videos/" + video + " -f null - "
            video_duration = get_duration(cmd)

            number_of_word = total_word_count(answer)
            number_of_segment = int(number_of_word/num_of_word_in_segment)+1
            segment_duration = video_duration/number_of_segment

            web_vtt_string = compose_web_vtt(answer, segment_duration, number_of_segment)

            write_web_vtt(subtitle_file_name, web_vtt_string)


# Example command to run ffmpeg in command line
# cmd = "ffmpeg -i ../input.webm -f null - "

# getDuration returns the duration of each video in seconds
# We are taking the last two digits of seconds in time returned by ffmpeg command
# since all videos are within one minute long
def get_duration(cmd):
    args = cmd.split()

    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    video_duration = ""

    for line in process.stdout:

        if line.find("time") != -1 and line.find("times") == -1:
            video_duration = int(line.split("time", 1)[1][:9].strip("=")[6:])

        # if the video is missing we set the duration to be 59 seconds
        if video_duration == "":
            video_duration = 59

    return video_duration


def total_word_count(answer):
    return len(answer.split())-1


# Composes WebVTT based on the number of sentences and duration of video
def compose_web_vtt(answer, segment_duration, number_of_segment):
    web_vtt_string = "WEBVTT\n\n"
    answer = answer.split()
    splitted_answer = []

    for i in range(number_of_segment):
        splitted_answer.append("")

    for i in range (0, len(answer)):
        answer[i] = answer[i] + " "
        splitted_answer[int(i/num_of_word_in_segment)] += answer[i]

    for num, one_segment in enumerate(splitted_answer):
        if one_segment:
            start_time = "00:" + str(int(segment_duration * num)).zfill(2) + ".000" if num != 0 else "00:00.000"
            arrow = " --> "
            end_time = "00:" + str(int(segment_duration * (num+1))).zfill(2) + ".000"

            # If there is leading whitespace before the sentence we remove it
            one_segment = one_segment.lstrip()

            web_vtt_string += start_time + arrow + end_time + "\n"
            web_vtt_string += one_segment + "\n\n"
    return web_vtt_string


def write_web_vtt(subtitle_file_name, web_vtt_string):
    with open(subtitle_file_name, 'wb') as file:
        web_vtt_string = web_vtt_string.strip('"')
        file.write(web_vtt_string.encode('utf-8'))


json_to_webvtt()
