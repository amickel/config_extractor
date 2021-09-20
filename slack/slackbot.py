# -*- coding: utf-8 -*-
"""

Created on Wed Sep  1 11:57:24 2021

@author: amickel

"""

import os
import re
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import file_handler
from slack.errors import SlackApiError
import slack
import json
import urllib
#import support_log


# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ["SLACK_BOT_TOKEN_CP"])  # use SLACK_BOT_TOKEN for beta.
# constants
EXAMPLE_COMMAND = "help"


# Listens to incoming messages that contain "hello"
# To learn available listener arguments,
# visit https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html


@app.message("help")
def message_help(message, say):
    # say() sends a message to the channel where the event was triggered
    say(("Attach the file you want me to convert. If you want this posted to" 
        "a group, include its ID in the message."
        '''\nHere are the files I can read:
            -Support log
            -Config Summary
            -bin
            -Diagnostic log'''
        "\nBe sure to not modify the file in any way so that I can verify what"
        "type of file you are giving me."
        
        '''\nUsers are stripped from the config.
        
        All passwords are set to "Welcome!"'''
        
        "\nI don't store your API keys for security reasons so you will need to"
        "provide them everytime you want to configure a group."

        
        "\nTo see the python code for extracting the config try:"
        "source [summary|support|diag|bin]"
        "\nFor help simply type \"help\":"
        "\nHave a feature request? Type \"Request [Your message here]\"."
        "\nNeed more help? Reach out to Adrianna Mickel or the SRE team!"
        ))


@app.event(event={"type": "message", "subtype":
                  re.compile("(me_message)|(file_share)")})
    
    
def add_reaction(message, say):
    #say(app.client.files_info)
    fileURL = message.get('files')[0].get('url_private')
    fileName = message.get('files')[0].get('name')
    user = message.get('user')
    groupID = message.get('text')

    res = requests.get(fileURL, headers={'Authorization': 'Bearer %s' % os.environ["SLACK_BOT_TOKEN"]})
    res.raise_for_status()
    content = res.content#.decode('utf-8')
    print(fileURL, " ", fileName, " ", res, " ", content)
    newFile = file_handler.file_handler(content, fileName)
    if newFile[0] != "/":#check if file path was returned
        say(newFile)
    else:
        try:
            response = app.client.files_upload(    
                file=newFile,
                initial_comment='Here is the config...',
                channels=user
            )
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            print('HERE')
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")


@app.message("")  # default message
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say("Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND))
    #res = app.client.apps_permissions_info()


#  Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN_CP"]).start()#).start()# use SLACK_APP_TOKEN for beta

#Slack bot can use v1 to look up whether an account is disabled or not given the correct permissions: https://www.cradlepointecm.com/api/v1/accounts/?format=json
#slack bot can use mana api to migrate customers. 

#


    
