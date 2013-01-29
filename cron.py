#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'miracledelivery'

import sys
import argparse
import logging
import datetime

VERSION = 0.1

class Cron():
    def __init__(self):
        self._create_parser()

    def _create_parser(self):
        # create the top-level parser
        parser = argparse.ArgumentParser(
                prog='pyCron',
                description='Python alternative to Posix cron utility',
                epilog='Development build. Feel free to disturb me if any error occurs.')
        subparsers = parser.add_subparsers(
            title='commands',
            description='type command name with "-h" argument to get more info about '\
                        'supported commands and their arguments, for example, "pyCron add -h"',
            dest='command_name')
        parser.add_argument('-v', '--version', action='version', version='%(prog)s '+ str(VERSION))
        parser.add_argument('-V', '--verbose', action='store_true', help='use verbose mode, i.e. will output log messages')

        # create the parser for the "add" command
        parser_add = subparsers.add_parser(
            'add',
            help='add a new task',
            description='Adds [command] to execution queue with the given designated time. '\
                        'The [command] is any valid console command in your environment.')
        parser_add.add_argument('minute', metavar='0-59', help='minutes (0-59)', type=int, choices=xrange(60))
        parser_add.add_argument('hour', metavar='0-23', help='hour (0-23, 0 = midnight)', type=int, choices=xrange(24))
        parser_add.add_argument('day', metavar='1-31', help='minutes (1-31)', type=int, choices=xrange(1, 32))
        parser_add.add_argument('month', metavar='1-12', help='month (1-12)', type=int, choices=xrange(1, 13))
        parser_add.add_argument('weekday', metavar='0-6', help='weekday (0-6, 0 = Monday)', type=int, choices=xrange(7))
        parser_add.add_argument('command', nargs='+', help='the task which will be run at the specified times')

        # create the parser for the "list" command
        parser_list = subparsers.add_parser(
            'list',
            help='list tasks running tasks',
            description='Lists all the running tasks')
        parser_list.add_argument('--baz', choices='XYZ', help='baz help') #TODO this stub should be removed

        # create the parser for the "remove" command
        parser_remove = subparsers.add_parser(
            'remove',
            help='remove task',
            description='Removes any specified task from the queue')
        parser_remove.add_argument('--baz', choices='XYZ', help='baz help') #TODO this stub should be removed

        self.parser = parser

    def execute_command(self, args=None):
        return self.parser.parse_args(args)

    def _handle_add_task(self, args):
        now = datetime.datetime.now()
        command = args.command
        if now.month == args.month and now.day == args.day and now.hour == args.hour: #TODO stub, remove after debug is complete
            self._execute_immediately(command)
        #if now.month == args.month and now.day == args.day and now.hour == args.hour and now.minute == args.minute and now.weekday():
        #    self._execute_immediately(command)
        else:
            date = self._create_des_time(args.minute, args.hour, args.day, args.month, args.weekday)
            self._add_to_task_queue(command, date)

    def _execute_immediately(self, command):
        from subprocess import call
        call(command)

    def _create_des_time(self, m, h, d, M, w): #TODO implement!
        pass

    def _add_to_task_queue(self, command, date): #TODO implement with greenlets
        pass

def main(args=None):
    # logger initialize
    logging.basicConfig(level=logging.DEBUG)

    if args is None:
        args = sys.argv[1:]
    # pyCron initialize
    cron = Cron()
    command = cron.execute_command(args)

    if command.command_name == 'add':
        logging.debug('ADD was called')
        cron._handle_add_task(command)
    elif command.command_name == 'list':
        logging.debug('LIST was called')
        #TODO
        pass
    elif command.command_name == 'remove':
        logging.debug('REMOVE was called')
        #TODO
        pass

if __name__ == '__main__':

    sys.exit(main('add 0 0 30 1 0 man ls'.split()))

