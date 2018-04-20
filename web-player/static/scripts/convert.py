
# This file updates the video type of videos.
# A regular avatar video will have video-type regular
# And a filler avatar video will have video-type filler

import json

f = open("all_characters.json", "r")

fw = open('all_characters-new.json', 'w')

resp = json.load(f)

filler_list = [338, 339, 340, 341, 342, 1210, 1211, 1212, 1213, 1214, 2269, 2270, 2271, 2272, 2273, 2284, 2285, 2286,
               2287, 2288, 3210, 3211, 3212, 3213, 3214]

for i in range(0, len(resp["rows"]) - 1, 1):
    if "character" in resp["rows"][i]["doc"].keys():
        resp["rows"][i]["doc"]["video-type"] = "regular"

        if resp["rows"][i]["doc"]["index"] in filler_list:
            resp["rows"][i]["doc"]["video-type"] = "filler"

json.dump(resp, fw)

f.close()
