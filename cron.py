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
        parser.add_argument('-v', '--version',
            action='version',
            version='%(prog)s ' + str(VERSION))
        parser.add_argument('-V', '--verbose',
            action='store_true',
            help='use verbose mode, i.e. will output log messages')

        # create the parser for the "add" command
        parser_add = subparsers.add_parser('add',
            help='add a new task',
            description='Adds [command] to execution queue with the given designated time. '\
                        'The [command] is any valid console command in your environment.')
        parser_add.add_argument('minute',
            metavar='MINUTE',
            help='minute (0-59)',
            type=CronType.minute)
        parser_add.add_argument('hour',
            metavar='HOUR',
            help='hour (0-23, 0 = midnight)',
            type=CronType.hour)
        parser_add.add_argument('day',
            metavar='DAY',
            help='day of month (1-31)',
            type=CronType.day)
        parser_add.add_argument('month',
            metavar='MONTH',
            help='month (1-12, Jan, Feb, ...)',
            type=CronType.month)
        parser_add.add_argument('weekday',
            metavar='WEEKDAY',
            help='day of week (0-6) 0=Sunday, 1=Monday ... \n or Sun, Mon, Tue, Wed, Thur, Fri',
            type=CronType.weekday)
        parser_add.add_argument('command',
            nargs='+',
            help='the task which will be run at the specified times')

        # create the parser for the "list" command
        parser_list = subparsers.add_parser('list',
            help='list tasks running tasks',
            description='Lists all the running tasks')
        parser_list.add_argument('--baz', choices='XYZ', help='baz help') #TODO this stub should be removed

        # create the parser for the "remove" command
        parser_remove = subparsers.add_parser('remove',
            help='remove task',
            description='Removes any specified task from the queue')
        parser_remove.add_argument('--baz', choices='XYZ', help='baz help') #TODO this stub should be removed

        self.parser = parser

    def execute_command(self, args=None):
        return self.parser.parse_args(args)

    def _handle_add_task(self, args):
        now = CronDateTime.now()
        cron_time = self._create_des_time(args.minute, args.hour, args.day, args.month, args.weekday)
        command = args.command

        #TODO rework! should always run from queue
        if now == cron_time:
            self._execute_immediately(command)
        else:
            self._add_to_task_queue(command, cron_time)

    def _execute_immediately(self, command):
        from subprocess import call

        call(command)

    def _create_des_time(self, m, h, d, M, w): #TODO implement weekdays support
        return CronDateTime(1, M, d, h, m)

    def _add_to_task_queue(self, command, date): #TODO implement with greenlets
        pass


class CronDateTime(
    datetime.datetime): #TODO further rework (also handle that for weekdays 0 is Sunday!! e.g. rework __init__) and also handle 999 as infinite
    """ Custom datetime.datetime representation with app-specific equality rules """

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return\
            self.month == other.month and\
            self.day == other.day and\
            self.hour == other.hour and\
            self.minute == other.minute
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class CronType():
    """ Container for parser argument types """
    INFINITE_MARKER = 999

    @staticmethod
    def minute(string):
        if string.isdigit():
            if int(string) in xrange(60):
                return int(string)
            else:
                msg = "%s is not in range of [0-59]" % string
                raise argparse.ArgumentTypeError(msg)
        elif string.strip() == '*':
            return CronType.INFINITE_MARKER
        else:
            msg = "%s is unsupported value for argument" % string
            raise argparse.ArgumentTypeError(msg)

    @staticmethod
    def hour(string):
        if string.isdigit():
            if int(string) in xrange(24):
                return int(string)
            else:
                msg = "%s is not in range of [0-23]" % string
                raise argparse.ArgumentTypeError(msg)
        elif string.strip() == '*':
            return CronType.INFINITE_MARKER
        else:
            msg = "%s is unsupported value for argument" % string
            raise argparse.ArgumentTypeError(msg)

    @staticmethod
    def day(string):
        if string.isdigit():
            if int(string) in xrange(1, 32):
                return int(string)
            else:
                msg = "%s is not in range of [1-31]" % string
                raise argparse.ArgumentTypeError(msg)
        elif string.strip() == '*':
            return CronType.INFINITE_MARKER
        else:
            msg = "%s is unsupported value for argument" % string
            raise argparse.ArgumentTypeError(msg)

    @staticmethod
    def month(string):
        months = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10,
                  'nov': 11, 'dec': 12}
        if string.isdigit():
            if int(string) in xrange(1, 13):
                return int(string)
            else:
                msg = "%s is not in range of [1-12]" % string
                raise argparse.ArgumentTypeError(msg)
        elif string.strip() == '*':
            return CronType.INFINITE_MARKER
        elif string.strip().lower() in months:
            return months[string.strip().lower()]
        else:
            msg = "%s is unsupported value for argument" % string
            raise argparse.ArgumentTypeError(msg)

    @staticmethod
    def weekday(string):
        weekdays = {'sun': 0, 'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6}
        if string.isdigit():
            if int(string) in xrange(7):
                return int(string)
            else:
                msg = "%s is not in range of [0-6], where 0 is Sunday" % string
                raise argparse.ArgumentTypeError(msg)
        elif string.strip() == '*':
            return CronType.INFINITE_MARKER
        elif string.strip().lower() in weekdays:
            return weekdays[string.strip().lower()]
        else:
            msg = "%s is unsupported value for argument" % string
            raise argparse.ArgumentTypeError(msg)


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
        logging.debug(command)
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
    sys.exit(main('add * 1 30 JAn wED ls'.split()))
#    sys.exit(main('add -h'.split()))
