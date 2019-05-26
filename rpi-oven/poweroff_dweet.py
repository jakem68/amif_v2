#!/usr/bin/env python

__author__ = 'Jan Kempeneers'

import dweepy, time, threading, queue, os
from subprocess import call


def dweet_listener(thing_name, q):
    while True:
        try:
            for dweet in dweepy.listen_for_dweets_from(thing_name):
                q.put(dweet)
                # print(dweet)
        except:
            print("no incoming messages for {}, reconnecting the listener".format(thing_name))
            pass
        # print(dweet)
        # for dweet in dweepy.listen_for_dweets_from('cirris_dweet135c1'):
        #     print(dweet)

def dweet_actions(q):
    while True:
        print("waiting for incoming message from test_device")
        message = q.get()
        content = message["content"]
        print(content["msg"])
        if content["msg"] == 1:
            os.system('sudo reboot')
        if content["msg"] == 2:
            os.system('sudo shutdown -h now')

        time.sleep(0.1)


def dweet_run(dweet_thing_name):
    q = queue.Queue()
    thread1 = threading.Thread(target=dweet_listener, args=(dweet_thing_name, q))
    thread1.start()
    thread2 = threading.Thread(target=dweet_actions, args=(q,))
    thread2.start()


def main():
    dweet_thing_name = "sirris.amifv2.oven"
    dweet_run(dweet_thing_name)


if __name__ == "__main__":
    main()
