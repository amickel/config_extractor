# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 14:11:47 2021

@author: amickel
"""

import json
import ast
import zlib
import os
import re


def file_handler(fname, fType):
    file_extension = os.path.splitext(fType)
    if(file_extension[1] == '.bin'):  # if this is a .bin file
        config = json.loads(zlib.decompress(fname).decode())[0]
        config = config.get('config')
        #configJ = json.loads(config)
        config = '{"configuration": [' + json.dumps(conf_wrapper(config)) + ',[]]}'
        return make_file(config)
        #return make_file(conf_wrapper(config))
    # file is diagnostic, config or support log.
    data = fname.decode('utf-8')
    # print("fname is ", fname)
    if data.find('*** CFGDIFF ***') > -1:  # is this a support log
        # extract config portion of file from support log
        obj = data[data.find('*** CFGDIFF ***')+16:
                   data.rfind('*** REMOVALS ***')-2]
        lit = ast.literal_eval(obj)  # convert to dict
        # grab the config section (ignore state)
        config = lit.get('config')
        config = '{"configuration": [' + json.dumps(conf_wrapper(config)) + ',[]]}'
        return make_file(config)
    elif data.find('Config\n======\n{') > -1 or data.find(
            'Config\r\n======\r\n{') > -1:  # is this a diagnostic log
        data = conf_clean(data)
        obj = data[data.find('Config\n======\n')+14: len(data)]  # EOF
        config = json.loads(obj)  # convert to dict
        # grab the config section (ignore state)
        conf_fin = '{"configuration": [' + json.dumps(conf_wrapper(config)) + ',[]]}'
        return make_file(conf_fin)
    # fist line of a config summary should always be '['
    elif data.split('\n', 1)[0] == "[\r" or data.split('\n', 1)[0] == "[":
        #  Remove conflicting group config if this is from the Target tab.
        data = conf_clean(data)
        # remove all group level configs with a comma (not last in list)
        data = re.sub("\" / \".+?(?=,)", "\"", data)  # remove group code
        data = re.sub(" / .+?(?=,)", "", data)  # remove group code
        # remove all group level configs that are last in list
        data = re.sub("(\" / \".*)", "\"", data)
        conf_fin = json.loads(data)
        conf_fin[0] = conf_wrapper(conf_fin[0])
        return make_file('{"configuration": ' + json.dumps(conf_fin) + '}')
    else:  # this is not a supported file.
        return 'Sorry, I cannot read this file. Check that it is a supported \
file type.'


def conf_clean(dirty_config):  # Consolidate regex code cleaning where possible
    data = re.sub("\r", "", dirty_config)
    # Single * not an accepted password, insert new password where applicable
    data = re.sub(": \"\*\"", ": \"Welcome!\"", data)
    return data


def conf_wrapper(config):
    # Strip contaienrs projects from file as NCM API will reject this for
    #    security reasons.
    config.pop('ecm', None)
    '''containers = config.get('container', {}).get('projects', {})
    if containers != {}:
        for project in containers:
            if type(project) == str:
                project = json.loads(project)
                print(project)
                print(type(project))
            project.pop('config', None)'''
    if config.get('system', {}) != {}:
        config['system'].pop('users', None)  # remove users section
    return config


def make_file(conf_fin):
    try:
        f = open("/temp/config.txt", "w")
        f.write(conf_fin)
        f.close()
        return "/temp/config.txt"
    except IOError:
        print(IOError)
        return 'Sorry, there was an issue with sending the file. Please \
report to Adrianna Mickel.'

    