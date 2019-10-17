import select

__author__ = 'Jan Kempeneers'

import os, sys, time, threading, mqtt_mitutoyo

if __name__ == "__main__":
    main()

def main():
    run()


def run():
    ask_file = "C:/MCOSMOS/Remote/remote.ask"
    msg_file = "C:/MCOSMOS/Remote/remote.msg"
    ans_file = "C:/MCOSMOS/Remote/remote.ans"
    commfiles = {"ask_file": ask_file, "ans_file":ans_file, "msg_file":msg_file}
    ans_file_found = False
    topic = "sirris/diep2/klima1/Mitutoyo"
    # thread1 = threading.Thread(target=params_dashboard.run, args=[])
    # thread1.start()
    clear_cmmComm()
    while True:
        status_kogame = monitor_kogame(commfiles, ans_file_found)
        mqtt_msg = mqtt_mitutoyo.get_most_recent_message()
        if mqtt_msg != "" and mqtt_msg =="run" and status_kogame == "ready":
            start_kogame()
            status_kogame="busy"
            mqtt_mitutoyo.publish(status_kogame)
        time.sleep(0.25)

        

# added this dummy function to replace real one below for safety reasons
def start_kogame():
    print("starting the Crysta-Apex CMM")
    time.sleep(3)
    pass

'''
def start_kogame():
    tempfile = "C:/MCOSMOS/Remote/tempfile.txt"
    askfile = "C:/MCOSMOS/Remote/remote.ask"
    text = 'EXECUTE_PATH_PART_PROGRAM\n' \
           'C:\Projecten\ALMA\DATA\n' \
           'Trial connect\n' \
           'Trial connect\n' \
           '0\n' \
           '0\n' \
           '0\n' \
           '1\n' \
           '1\n' \
           'CRTAS776\n' \
           'STAT'

    try:
        with open(tempfile, 'w') as f:
            f.write(text)
    except:
        print('could not create tempfile')
        pass

    try:
        os.rename(tempfile, askfile)
    except:
        print('could not rename tempfile to askfile')
        pass
'''

def clear_cmmComm(commfiles):
    for file in commfiles:
        file_exists = os.path.isfile(commfiles[file])
        if file_exists:
            os.remove(commfiles[file])


def monitor_kogame(commfiles, ans_file_found):
    kogame_status = "busy"
    file_found = False
    for file in commfiles:
        file_exists = os.path.isfile(commfiles[file])
        if file_exists:
            if file == commfiles["ask_file"]:
                file_found = True
                kogame_status = "busy"
                break
            elif file == commfiles["ans_file"]:
                file_found = True
                ans_file_found = True
                os.remove(commfiles["ans_file"])
                kogame_status = "busy"
            elif file == commfiles["msg_file"]:
                file_found = True
                try:
                    with open(file) as f:
                        msg_firstline = f.readline()
                        if msg_firstline == 'PPERR\n':
                            kogame_status = "busy"
                        elif msg_firstline == 'PPEND\n':
                            kogame_status = "ready"
                    os.remove(file)
                    ans_file_found = False
                    print(msg_firstline)
                except:
                    print('could not read remote.msg file')
                    kogame_status = "busy"
                    pass
    if not file_found and not ans_file_found:
        kogame_status = "ready"
    return kogame_status

