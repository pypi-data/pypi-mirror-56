"""
A human friendly time calculator for functions and code blocks
"""
import logging
import time

__author__ = 'ozgur'
__creation_date__ = '15.11.2019' '21:58'

TALK_TO_LOG = False


class TimedFunction:
    """
    Decorator class for timing functions
    """
    def __init__(self, func=None, tag: str = None, talk: bool = True):
        """
        Decorator for calculating a function
        :param func: default function given by decorator subsystem
        :param tag: use tag instead of function name
        :param talk: echo directly if true else echo in summary
        """
        self.tag = tag
        self.talk = talk
        self.func = func

    def __call__(self, *args, **kwargs):
        if not self.func:
            self.func = args[0]

        if not self.tag:
            self.tag = self.func.__name__

        TimeThat.start(self.tag)
        retval = self.func(*args, **kwargs)
        TimeThat.stop(self.tag, self.talk)
        return retval


class TimeThat:
    """
    Collection of timethat functions
    """
    timedict = {}

    @staticmethod
    def _echo(outtext: str):
        estr = "TimeThat -> {}".format(outtext)
        if TALK_TO_LOG:
            logging.info(estr)
        else:
            print(estr)

    @classmethod
    def talkone(cls, tag: str, tdiff: float):
        """
        Simple echo a calculation in Time Me ecosystem

        :param tag: name of the echo
        :param tdiff: calculated time
        :return:
        """
        cls._echo("{:7.2f} sec. -> {}".format(tdiff, tag))

    @classmethod
    def start(cls, tag: str):
        """
        starts a timer

        :param tag: name of the timer
        :return:
        """
        if not isinstance(tag, str):
            raise TypeError("Tag must be str")
        if not tag:
            raise ValueError("Tag can't be empty")
        tdict = cls.timedict.get(tag, {"stime": 0.0, "cost": 0.0, "cnt": 0})
        tdict["stime"] = time.time()
        cls.timedict[tag] = tdict

    @classmethod
    def stop(cls, tag: str, talk: bool = True):
        """

        :param tag: name of the timer
        :param talk: echo directly if true else echo later
        :return:
        """
        if not isinstance(tag, str) or not isinstance(talk, bool):
            raise TypeError
        if not tag:
            raise ValueError("Tag can't be empty")

        tdict = cls.timedict.get(tag, None)
        if not tdict or tdict["stime"] == 0.0:
            if talk:
                raise ValueError("{} not started yet.".format(tag))
        else:
            tdict["cost"] = tdict["cost"] + time.time() - tdict["stime"]
            tdict["stime"] = 0.0
            tdict["cnt"] = tdict["cnt"] + 1
            cls.timedict[tag] = tdict
            if talk:
                cls.talkone(tag, tdict["cost"])

    @classmethod
    def summary(cls, tags: list = None, reset: bool = False):
        """
        echoes summary

        :param tags: echos all timers if None else only echo given timers
        :param reset: resets all timers
        :return:
        """
        if not tags:
            tags = []
        if not isinstance(tags, list) or not isinstance(reset, bool):
            raise TypeError
        for tag, tdict in cls.timedict.items():
            if not tags or tag in tags:
                cls._echo("Total: {:7.2f} sec, Average: {:7.2f} sec, Count: {:3}  -> {}".format(
                    tdict['cost'], tdict['cost'] / tdict['cnt'], tdict['cnt'], tag))
            else:
                pass
        if reset:
            cls.timedict.clear()
