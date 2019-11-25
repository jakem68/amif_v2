import select

__author__ = 'Jan Kempeneers'

import os, shutil, sys, time, threading, mqtt_mitutoyo, json

def main():
    run()


def run():
    ask_file = "C:/MCOSMOS/Remote/remote.ask"
    msg_file = "C:/MCOSMOS/Remote/remote.msg"
    ans_file = "C:/MCOSMOS/Remote/remote.ans"
    commfiles = {"ask_file": ask_file, "ans_file":ans_file, "msg_file":msg_file}
    ans_file_found = False
    # thread1 = threading.Thread(target=params_dashboard.run, args=[])
    # thread1.start()
    clear_cmmComm(commfiles)
    previous_status_crysta = ""
    part_UID = ""
    while True:
        status_crysta = monitor_crysta(commfiles, ans_file_found, part_UID)
        status_crysta_json = {"status_crysta":status_crysta}
        if status_crysta == "error":
            mqtt_mitutoyo.publish(json.dumps(status_crysta_json))
            sys.exit("error on the Crysta-Apex")
        if status_crysta != previous_status_crysta:
            mqtt_mitutoyo.publish(json.dumps(status_crysta_json))
            previous_status_crysta = status_crysta    
        mqtt_msg = mqtt_mitutoyo.get_most_recent_message()
        if mqtt_msg:
            print("mqtt message is {}".format(mqtt_msg))
            mqtt_dict = json.loads(mqtt_msg)
            # analyzing {"command":"run", "part_UID":"1234"}
            if status_crysta == "ready" and \
               "command" in mqtt_dict.keys() and mqtt_dict["command"] == "run" and \
               "part_UID" in mqtt_dict.keys() and mqtt_dict["part_UID"] != "":
                part_UID = mqtt_dict["part_UID"]
                start_crysta()
        time.sleep(2)

        

# added this dummy function to replace real one below for safety reasons
'''
def start_crysta():
    print("starting the Crysta-Apex CMM")
    time.sleep(3)
    pass
'''
def start_crysta():
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

def clear_cmmComm(commfiles):
    for file in commfiles:
        file_exists = os.path.isfile(commfiles[file])
        if file_exists:
            os.remove(commfiles[file])


def monitor_crysta(commfiles, ans_file_found, part_UID):
    crysta_status = "busy"
    file_found = False
    files_found = []
    for file in commfiles:
        file_exists = os.path.isfile(commfiles[file])
        if file_exists:
            files_found.append(file)
    if files_found:
        if "ask_file" in files_found:
            crysta_status = "busy"
        elif "msg_file" in files_found:
            try:
                print(commfiles["msg_file"])
                with open(commfiles["msg_file"]) as f:
                    msg_firstline = f.readline()
                    if msg_firstline == 'PPERR\n':
                        crysta_status = "error"
                    elif msg_firstline == 'PPEND\n':
                        crysta_status = "ready"
                        copy_report(part_UID)
                print(msg_firstline)
                clear_cmmComm(commfiles)
            except:
                print('could not read remote.msg file')
                crysta_status = "busy"
                pass            
        elif "ans_file" in files_found:
            crysta_status = "busy"
    else:
        crysta_status = "ready"
    return crysta_status

def copy_report(part_UID):
    report = "C:\\Projecten\\ascii bestanden\\trial_connect.csv"
    report_copy = "\\\pc00392\demonstrator-share\\4.0_made_real_cmm_reports\\trial_connect_{}.csv".format(part_UID)
    shutil.copy(report, report_copy)
    os.remove(report)
    

if __name__ == "__main__":
    main()

