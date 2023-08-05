# Author : BetaCodings
# Author : info@betacodings.com
# Maintainer By: Emmanuel Martins
# Maintainer Email: emmamartinscm@gmail.com
# Created by BetaCodings on 17/11/2019.
import os, re

class browser:

    def __getattr__(self, item):
        return item

    def __init__(self):
        if "" is not os.environ.get('HTTP_USER_AGENT'):
            self.agent = os.environ.get('HTTP_USER_AGENT')
        else:
            self.agent = None

        self.info = []
        self.name()
        self.name = self.info['Browser']
        self.version = self.info['Version']

    def name(self):
         NAME = {
                "Navigator": "Navigator",
                "Firefox": "Firefox",
                "Internet Explorer": "MSIE",
                "Chrome": "chrome",
                "Maxthon": "Maxthon",
                "Opera": "Opera",
                "OPR": "Opera",
                "Safari": "Safari",
                "Camino": "Camino",
                "SeaMonkey": "SeaMonkey",
                "K-Meleon": "K-Meleon",
                "Flock": "Flock",
                "Lunascape": "Lunascape",
                "Torch": "Torch",
                "Xtravo": "Xtravo",
                "Stainless": "Stainless",
                "Deepnet Explorer": "Deepnet",
                "QtWeb": "QtWeb",
                "CometBird": "CometBird",
                "xombrero": "xombrero",
                "Ultrabrowser": "Ultrabrowser",
                "Chromium": "Chromium",
                "Dooble": "Dooble"

            }
         agent = str(self.agent)
         slipt = agent.split(" ")
         for key in reversed(slipt):
             splits = key.split("/")

             if len(splits[0]) > 0 or len(splits[1]) > 0 :
                 if NAME.get(splits[0], None) is not None:
                     self.info = {'Browser': splits[0]}
                     info = {'Version': splits[1]}
                     break
                 else:
                     self.info = {'Browser': "UNKNOWN"}
                     info = {'Version': "UNKNOWN"}

             else:
                self.info = {'Browser': "UNKNOWN"}
                info = {'Version': "UNKNOWN"}


         self.info.update(info)