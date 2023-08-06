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
import cherrypy as applyai
import json

class Config(object):
  def __init__(self):
    self.cfg = {}

  @applyai.expose
  def getSettingsForm(self):
    tab = "<table>"
    for c in self.cfg["settings"]:
      for v in self.cfg["settings"][c]["list"]:
        tab += "<tr>"
        tab += "<td>" + c
        tab += "</td>"
        tab += "<td>" + v
        tab += "</td>"
        if "text" in self.cfg["settings"][c][v]:
          tab += "<td>" + str(self.cfg["settings"][c][v]["text"])
          tab += "</td>"
          tab += "<td><input size='4' value='" + str(self.cfg["settings"][c][v]["value"]) + "'/>"
          tab += "</td>"
        else: # must be an array
          for a in self.cfg["settings"][c][v]:
            tab += "<tr><td></td><td></td><td></td>"
            for attr, value in a.items():
              tab += "<td>" + str(attr)
              tab += "</td>"
              tab += "<td><input size='4' value='" + str(value) + "'/>"
              tab += "</td>"
            tab += "</tr>"
        tab += "</tr>"
    tab += "</table>"
    
    applyai.response.headers['Content-Type'] = "text/html"
    return tab

  @applyai.expose
  def updateSettingVar(self, plugin, var, value):
    self.cfg["settings"][plugin][var]["value"] = value
    return self.cfg["settings"][plugin]

  @applyai.expose
  @applyai.tools.json_out()
  def getConfig(self, page=""):
    if page == "":
      return self.cfg["settings"]
    else:
      try:
        return self.cfg["settings"][page]
      except:
        return "that did not work ['settings']['" + page + "']"
    return self.cfg
