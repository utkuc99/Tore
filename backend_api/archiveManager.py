import os.path

def checkArchive(videoCode):

    script_dir = os.path.dirname(os.path.realpath(__file__))

    with open(f"{script_dir}/worker.lock", "r+") as fp:

            if videoCode in fp.read():
                print("found it")
                return True
            else:
                return False

def writeArchieve(videoCode):

    script_dir = os.path.dirname(os.path.realpath(__file__))

    with open(f"{script_dir}/worker.lock", "r+") as fp:

        print("writing it")
        fp.write(videoCode)
