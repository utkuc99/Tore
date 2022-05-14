# Try motion analysis

import subprocess
from datetime import datetime, timedelta


def motion_analysis(videoCode):
    print("trying motion analysis")
    process = subprocess.run("dvr-scan -i " + videoCode + ".mp4 -t 5 -so", stdout=subprocess.PIPE, shell=True)
    output = str(process.stdout)
    # For windows: \\r\\n For MacOS: \\n and \\n\'
    x = output.partition("values:\\r\\n")[2].split("\\r\\n")[0]
    print(x)
    size = len(x)
    y = x.split(",")

    # Calculate segments without motion
    array = []
    for i in range(0, len(y)):
        time2 = datetime.strptime(y[i], '%H:%M:%S.%f')
        a_timedelta = time2 - datetime(1900, 1, 1)
        seconds = a_timedelta.total_seconds()
        array.append(seconds)

    segmentsWithMotion = []
    x = 0
    while x < len(array) - 1:
        segmentsWithMotion.append([array[x], array[x + 1]])
        x = x + 2
    print("done motion analysis")
    print("Segments with motion: " + str(segmentsWithMotion))
    return segmentsWithMotion
