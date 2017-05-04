#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, re, json
import logging
import random
import copy
import argparse
from datetime import datetime

#
# Customized global variables
#
TIME_FORMAT = '%Y%m%d-%H:%M:%S'
CHECKLIST_NAME = 'checklist-' + str(datetime.now().strftime(TIME_FORMAT))
DEFAULT_SCENARIO_NUM = 30
INITIAL_ID = 1

def configLog(debug):
    "Configure logging"
    logfile = os.path.basename(__file__).replace('.py', '.log') if debug == True else None
    loglevel = logging.DEBUG if logfile is not None else None
    logging.basicConfig(format='%(asctime)s [%(threadName)16s][%(module)14s][%(levelname)8s] %(message)s', filename=logfile, level=loglevel)

def convertPrioToOccur(num):
    "Convert priority to occurance times"
    # occurance = 6 / priority
    #  e.g: priority is 3, occurance is 2
    return int(6 / int(num))

def randomPickScenario(component):
    "Pick a sencario randomly"
    defaultOccur = convertPrioToOccur(component['prio'])
    scenarios = []
    for key, val in component['scenario'].items():
        occur = defaultOccur
        if (len(val) != 0):
            if 'prio' in val:
                occur = convertPrioToOccur(val['prio'])

        scenarios += [key] * occur

    return random.choice(scenarios)

def showSenario(data, currentId):
    "Show a scenario"
    logging.debug('>> showSenario')
    logging.debug('currentId: ' + str(currentId))

    for name, component in data.items():
        if (int(component['id']) == int(currentId)):
            logging.debug('id:' + str(component['id']))
            sentence = randomPickScenario(component)
            scenario = component['scenario'][sentence]

            # Not show current senario again
            del data[name]['scenario'][sentence]

            logging.debug('scenario: ' + str(scenario))

            if 'to' in scenario:
                if isinstance(scenario['to'], list):
                    nextId = random.choice(scenario['to'])
                else:
                    nextId = scenario['to']
            else:
                nextId = currentId

            if 'user' in scenario:
                if isinstance(scenario['user'], list):
                    sentence += ' (User: ' + '/'.join(scenario['user']) + ')'
                else:
                    sentence += ' (User: ' + scenario['user'] + ')'

            if 'platform' in scenario:
                if isinstance(scenario['platform'], list):
                    sentence = '[' + '/'.join(scenario['platform']) + '] ' + sentence
                else:
                    sentence = '[' + scenario['platform'] + '] ' + sentence

            appendChecklist(CHECKLIST_NAME, name, sentence)
            print('[' + name + '] ' + sentence)

            logging.debug('sentence: ' + str(sentence))
            logging.debug('nextId: ' + str(nextId))

            return data, nextId

def checkSenarioData(data, rawdata, currentId):
    "Check scenario list"
    for name, component in data.items():
        if (int(component['id']) == int(currentId)):
            # Restore secanrio list when it's empty
            if (len(component['scenario']) == 0):
                logging.debug('reset data for: ' + name)
                data[name]['scenario'] = copy.deepcopy(rawdata[name]['scenario'])
    return data

def randomInterrupt(data):
    "Show a random interruption"
    # less than 10% chance to have interruption
    if (random.randint(0, 100) < 10):
        sentence = randomPickScenario(data['interruption'])
        appendChecklist(CHECKLIST_NAME, 'Interruption', sentence)
        print('[' + 'Interruption' + '] ' + sentence)
        return True
    return False

def appendChecklist(fname, name, line):
    "Append line at the end of file"
    try:
        f = open(fname, 'r+')
    except IOError:
        f = open(fname, 'w+')

    content = f.read()
    f.write('[' + name + '] ' + line + '\n')

def main():
    # Setup parameter
    #   run script with -d, active debug mode (log file will be created)
    parser = argparse.ArgumentParser()
    parser.add_argument('file',  nargs=1, help='input json file')
    parser.add_argument('-n',  '--number', nargs=1, type=int, default=[DEFAULT_SCENARIO_NUM], help='number of scenario to display')
    parser.add_argument('-m',  '--mute', action='store_true', dest="mute", help='generate checklist without interation')
    parser.add_argument('-d',  '--debug', action='store_true', dest="debug", help='active debug log')

    args = parser.parse_args()

    # Config logging
    configLog(args.debug)
    logging.debug('args:\n' + str(args))

    try:
        with open(args.file[0]) as data_file:
            rawdata = json.load(data_file)
    except:
        print('Cannot read input file')
        sys.exit(1)
    data = copy.deepcopy(rawdata)

    currentId = INITIAL_ID

    for i in range(args.number[0]):
        print('>> Scenario ' + str(i + 1))
        if not randomInterrupt(data):
            data = checkSenarioData(data, rawdata, currentId)
            data, currentId = showSenario(data, currentId)


        if not args.mute:
            input('Press enter: ')
        print('\n')

if __name__ == '__main__':
    main()
