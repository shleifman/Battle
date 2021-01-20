import simplejson as json
import os

if os.path.isfile("./Ages.json") and os.stat("./Ages.json").st_size != 0:
    old_file = open("./Ages.json", "r+")
    data = json.loads(old_file.read())
    print("current Age is ", data["Age"], "-- adding a year.")
    data["Age"] += 1
    print("New Age is ", data["Age"])
else:
    old_file = open("./Ages.json", "w+")
    data = {"Name": "Nick", "Age": 27}
    print("No file found, setting default Age to ", data["Age"])

old_file.seek(0)
old_file.write(json.dumps(data))
