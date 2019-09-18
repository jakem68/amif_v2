#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Copyright 2014,2018 Mario Gomez <mario.gomez@teubi.co>
#
#    This file is part of MFRC522-Python
#    MFRC522-Python is a simple Python implementation for
#    the MFRC522 NFC Card Reader for the Raspberry Pi.
#
#    MFRC522-Python is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MFRC522-Python is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with MFRC522-Python.  If not, see <http://www.gnu.org/licenses/>.
#

import RPi.GPIO as GPIO
import MFRC522
import signal
import time, json
from my_mqtt_module import Mqtt

continue_reading = True
card_dict = {}
message = {"timestamp":"", "payload": ""}

my_mqtt = Mqtt("/media/usb/MFRC522-python/rfid_to_mosquitto.yml")
my_mqtt.start()
mqtt_start_time = time.time()

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

def remove_old_reads(card_dict):
    old_entries = []
    for k in card_dict:
        if time.time() - card_dict[k] > 1 :
            old_entries.append(k)
    for k in old_entries:
        del(card_dict[k])
    return card_dict

def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    return added, removed

def update_message(payload):
#    payload_str = json.dumps(payload)
    message["timestamp"] = time.strftime('%Y-%m-%d %H:%M:%S')
    message["payload"] = payload
    msg_out = json.dumps(message)
    return msg_out


# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    # If we have the UID, continue
    card_dict_previous = card_dict.copy()
    if status == MIFAREReader.MI_OK:
        now = time.time()
        # add new found id and timestamp to a dict of cards
#        card_dict = {card_id_str : now}
        card_dict = {tuple(uid) : now}
    # check for reads which haven't been update in the last second and remove them
    card_dict = remove_old_reads(card_dict)
    # check for added or removed cards
    added, removed = dict_compare(card_dict, card_dict_previous)
    if len(added) > 0:
        for a_tuple in added:
            a_list = list(a_tuple)
            a_list[4]="ON"
            a_str = ','.join(map(str, a_list))
            msg_out = update_message(a_str)
            my_mqtt.publish(msg_out = msg_out)

    if len(removed)>0:
        for r_tuple in removed:
            r_list = list(r_tuple)
            r_list[4]="OFF"
            r_str = ','.join(map(str, r_list))
            msg_out = update_message(r_str)
            my_mqtt.publish(msg_out = msg_out)

    if time.time() - mqtt_start_time > 30:
        my_mqtt.client.disconnect()
        mqtt_start_time = time.time()
        my_mqtt.start()

    time.sleep(my_mqtt.get_time_interval())
