# Author : BetaCodings
# Author : info@betacodings.com
# Maintainer By: Emmanuel Martins
# Maintainer Email: emmamartinscm@gmail.com
# Created by BetaCodings on 17/11/2019.
import os as opy, re

class os:

    def __getattr__(self, item):
        return item

    def __init__(self):
        if "" is not opy.environ.get('HTTP_USER_AGENT'):
            self.agent = opy.environ.get('HTTP_USER_AGENT')
        else:
            self.agent = None

        self.info = []
        self.name()
        self.name = self.info['OS']
        self.device = self.info['Device']

    def name(self):
         NAME = {
                "Windows": "PC",
				"Linux" : "PC",
				"Unix" : "PC",
				"Mac": "PC",
				"Android" : "Mobile",
				"Ubuntu" : "PC",
				"Chromium" : "PC",
				"iOS" : "PC",
				"DOS" : "PC",
				"JavaOS" : "PC",
				"Zorin" : "PC",
				"Elementary" : "PC",
				"NetWare" : "PC",
				"Papyros" : "PC",
				"Solaris" : "PC",
				"Symbian" : "Mobile",
				"Bharat" : "PC",
				"CentOS" : "PC",
				"ReactOS" : "PC",
                "iPhone" : "Mobile",
                "iPod" : "Mobile",
                "iPad" : "Mobile",
                "BlackBerry" : "Mobile",
                "Funtouch" : "Mobile",
                "LineageOS" : "Mobile",
                "BADA" : "Mobile",
                "Palm" : "Mobile",
                "Open" : "Mobile",
                "Maemo" : "Mobile",
                "Verdict" : "Mobile",

            }
         agent = str(self.agent)
         slipt1 = agent.split(")")
         slipt1 = str(slipt1).split("(")
         slipt1 = str(slipt1).split(";")
         slipt1 = str(slipt1).replace('"', " ").split('"')
         splits = str(slipt1).replace("'", " ").split(' ')

         for key in splits:
            if len(key) > 0:
                if NAME.get(key, None) is not None:
                    self.info = {'OS': key}
                    info = {'Device': NAME.get(key, "UNKNOWN")}
                    break
                else:
                    self.info = {'OS': "UNKNOWN"}
                    info = {'Device': "UNKNOWN"}


            else:
                self.info = {'OS': "UNKNOWN"}
                info = {'Device': "UNKNOWN"}

         self.info.update(info)