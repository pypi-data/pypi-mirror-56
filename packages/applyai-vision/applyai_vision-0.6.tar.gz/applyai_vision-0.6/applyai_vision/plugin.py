# =============================================================================
# Copyright (c) 2018-2019 gardner ag. All Rights Reserved.
#
# This software is the confidential and proprietary information of gardner ag
# ("Confidential Information"). You shall not disclose such 
# Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with gardner ag.
#
# GARDNER AG MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY OF THE
# SOFTWARE, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE, OR NON-INFRINGEMENT. GARDNER AG SHALL NOT BE LIABLE FOR ANY DAMAGES
# SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING OR DISTRIBUTING
# THIS SOFTWARE OR ITS DERIVATIVES.
# =============================================================================
import cherrypy
from cherrypy.process import wspbus, plugins

class Plugin(plugins.SimplePlugin):
    def __init__(self, bus, klass):
        plugins.SimplePlugin.__init__(self, bus)
        self.p = klass()

    def start(self):
        self.bus.log('Starting up ' + self.p.logname)
        self.bus.subscribe(self.p.name + "/start", self.startProjectCode)

    def stop(self):
        self.bus.log('Stopping ' +  self.p.logname)
        self.bus.unsubscribe(self.p.name + "/start", self.startProjectCode)
        self.stopProjectCode()

    def startProjectCode(self, options):
        self.p.start(options)

    def stopProjectCode(self):
      invert_op = getattr(self.p, "stop", None)
      if callable(invert_op):
          self.p.stop()

