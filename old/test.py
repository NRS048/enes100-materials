def timetest():
    import time

    waittime = 5

    oldtime = time.time()

    while time.time() - oldtime < waittime:
        #print("looping")
        continue

    print(time.time() - oldtime)
    print(waittime)