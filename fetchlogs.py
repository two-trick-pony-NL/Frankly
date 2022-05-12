import os
import time
epoch_time = int(time.time())


print("\n########################\n")
print("\n---Fetching logs from Lightsail---\n")
print("\n########################\n")
print("\n########################\n")
time.sleep(1)
print("\n########################\n")
minutesoldlogs = input("How many minutes of old logs should I fetch?    ")
minutesoldlogs = int(minutesoldlogs*60*1000)

#Getting the logs of the container with the preferences set so as in the file. The epoch at 3600 specifies all logs of the last 24H
timestamp = epoch_time - minutesoldlogs
print(timestamp)
getnewlog = True

print("getting new logs:")
while getnewlog:
    os.system("aws --color on lightsail  get-container-log --cli-input-json file://AWS/scriptpreferences.json --start-time "+str(timestamp)+"&")
    time.sleep(5)
    refresh = input("Hit r to refresh the logs, press q to exit ")
    if refresh == "r":
        pass
    elif refresh == "q":
        getnewlog = false
    else:
        pass
print("Closing logs, goodbye!")
    