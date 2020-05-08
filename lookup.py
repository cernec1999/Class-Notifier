#!/usr/bin/python3
import requests, time

# Query in the return text to search for
search = "NO SECTIONS FOUND FOR THIS INQUIRY."

# URL to the Hokie Spa Timetable
url = "https://banweb.banner.vt.edu/ssb/prod/HZSKVTSC.P_ProcRequest"

# URL to IFTTT maker WebHooks
# CHANGE ME
ifttt = "https://maker.ifttt.com/trigger/{{event_name}}/with/key/{{key_name}}"

# POST request headers to create a search
# CHANGE ME
headers =   {
                'CAMPUS':           '0',
                'TERMYEAR':         '202001',
                'CORE_CODE':        'AR%',
                'subj_code':        'CS',
                'SCHDTYPE':         '%',
                'CRSE_NUMBER':      '3214',
                'crn':              '13010',
                'open_only':        'on',
                'disp_comments_in': 'Y',
                'BTN_PRESSED': 'FIND class sections',
                'inst_name': ''
            }

# Method to evaluate if a certain class is open
def class_is_open():
    x = requests.post(url, data = headers)
    ret_text = x.text
    #print(ret_text)
    if x.status_code is not 200:
        return False
    if search not in ret_text:
        return True
    return False

# We wish to loop forever, even if the class
# is open to continue alerting the user to
# choose the class (in case of sleep)
while True:
    try:
        if not class_is_open():
            print("[DBG]: The specified class is not open. Doing nothing...")
        else:
            print("[DBG]: The specified class is now open! Deploying alert via IFTTT...")
            requests.get(ifttt)
    except:
        print("[DBG]: Something went wrong. But let's loop again!")
    time.sleep(15)
