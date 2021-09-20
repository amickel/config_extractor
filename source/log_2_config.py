# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 11:43:01 2021

@author: amickel
"""

import PySimpleGUI as sg
import requests
import file_handler
import os


layout = [
          [sg.Text('X-CP-API-ID:'), sg.InputText(key='Your-X-CP-API-ID',
                                                  default_text=os.environ.get(
                                                     "X-CP-API-ID", ""))],
          [sg.Text('X-CP-API-KEY:'), sg.InputText(key='Your-X-CP-API-KEY',
                                                  default_text=os.environ.get(
                                                    "X-CP-API-KEY", ""))],
          [sg.Text('X-ECM-API-ID:'), sg.InputText(key='Your-X-ECM-API-ID',
                                                  default_text=os.environ.get(
                                                      "X-ECM-API-ID", ""))],
          [sg.Text('X-ECM-API-KEY:'), sg.InputText(key='Your-X-ECM-API-KEY',
                                                   default_text=os.environ.get(
                                                       "X-ECM-API-KEY", ""))],
          [sg.Text('Input target group ID:'), sg.InputText(key='groupID')],
          [sg.Text('Browse to the log file'), sg.Input(),
           sg.FileBrowse(key="fLog")],
          [sg.Button('Do The Thing!'), sg.Button('Cancel')],
          [sg.Multiline(key='result', visible=False)]
         ]


def sendConfig():
    server = 'https://www.cradlepointecm.com/api/v2'
    headers = {
                "X-CP-API-ID": values['Your-X-CP-API-ID'],
                "X-CP-API-KEY": values['Your-X-CP-API-KEY'],
                "X-ECM-API-ID": values['Your-X-ECM-API-ID'],
                "X-ECM-API-KEY": values['Your-X-ECM-API-KEY'],
                'Content-Type': 'application/json'
    }
    group_id = values["groupID"]
    newFile = extractConfig()[1]

    url = f'{server}/groups/{group_id}/'
    req = requests.put(url, headers=headers, data=newFile)
    if req.status_code == 401:
        return("Check your API IDs...")
    elif req.status_code == 400:
        return("Check your API Keys...")
    elif req.status_code < 300:
        return(str(req.status_code) + ": Success!")
    else:
        return(str(req.status_code) + ": Error:\n" + req.text)


def extractConfig():
    fname = values["fLog"]
    try:
        newFile = file_handler.file_handler(fname)
        f = open("config.txt", "w")
        f.write(newFile)
        f.close()
        return "Wrote config to config.txt", newFile
    except Exception as err:
        return(err)


'''GUI'''
sg.theme('DarkAmber')   # Add a touch of color

# Create the Window
window = sg.Window('Support Log to Group Config', layout)
# Event Loop to process "events" and get the "values" of the inputs

while True:
    event, values = window.read()

    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    elif event == "Do The Thing!" and values['Your-X-CP-API-ID'] and values['Your-X-ECM-API-ID'] and values['Your-X-ECM-API-KEY'] and values['Your-X-CP-API-KEY'] and values['groupID'] and values['fLog']:
        method_returned = sendConfig()
        print(method_returned)
        window['result'].update(visible=True)
        window['result'].update(method_returned)
    elif event == "Do The Thing!" and values['fLog']:
        method_returned = extractConfig()
        print(method_returned[0])
        window['result'].update(visible=True)
        window['result'].update(method_returned)

window.close()