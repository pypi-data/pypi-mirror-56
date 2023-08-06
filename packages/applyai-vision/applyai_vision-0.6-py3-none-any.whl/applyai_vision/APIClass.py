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
import requests
import json
import os
import cv2
import time
from datetime import timedelta
import applyai_vision.job as job
import applyai_vision.memStore as ms
import pandas as pd
from pandas.io.json import json_normalize

class stdAPI:

  def __init__(self, name):
    self.logname = name[:6].upper().ljust(6)
    self.name = name
    self.store = ms.memStore(name)
    self.project = os.environ['PROJECT']
    self.cfgFilename = './projects/' + self.project + '/config/' + self.name + '.conf'
    self.cfg = {}
    applyai.log('init API',self.logname)

  #Converts the input JSON to a DataFrame
  def convertToDF(self,dfJSON):
      return(json_normalize(dfJSON))

  #Converts the input DataFrame to JSON 
  def convertToJSON(self, df):
      resultJSON = df.to_json(orient='records')
      return(resultJSON)

  @applyai.expose
  @applyai.tools.json_in()
  @applyai.tools.json_out()
  def start(self): #, sequence='detect', frameIn='', channel=0, targets="[]"):

    applyai.log('$Start', self.name)

    params = applyai.request.json
    params['name'] = self.name             # always overwrite this

    if 'sequence' not in params:          # default sequence detect
      params['sequence'] = 'detect'

    if 'frameIn' not in params:
      params['frameIn'] = self.name

    if 'frameOut' not in params:
      params['frameOut'] = self.name

    if 'channel' not in params:
      params['channel'] = 0

    # in image of this plugin = out image of that plugin
    self.store.updateFrameIn(self.name, 0, self.store.fetchFrameOut(params['frameIn'],0))

    targets = pd.DataFrame(columns=['plugin'])
    if 'targets' in params:
      targets = self.convertToDF(params['targets'])

    params['targets'] = targets
    #applyai.log(str(params), self.logname)

    targets = self.main(params)

    params['targets'] = targets.to_dict('records')
    params['frameIn'] = self.name       # use this to save the last plugin in frameIn for the nect plugin
    #applyai.log(str(params), self.logname)
    applyai.log('$Finished', self.name)
    return params

  @applyai.expose
  def getFrame(self, frame, camera=0, rand=0):
    # applyai.log('getFrame ' + str(frame) + '|' + str(camera), self.logname)
    camera = int(camera)
    if frame == 'in':
      return(self.getFrameIn(camera, rand))
    else:
      return(self.getFrameOut(camera, rand))

  @applyai.expose
  def getFrameIn(self, camera=0, rand=0):
    applyai.response.headers['Content-Type'] = "image/jpg"
    return cv2.imencode('.jpg', self.store.fetchFrameIn(self.name, camera))[1].tobytes()

  @applyai.expose
  def getFrameOut(self, camera=0, rand=0):
    applyai.response.headers['Content-Type'] = "image/jpg"
    return cv2.imencode('.jpg', self.store.fetchFrameOut(self.name, camera))[1].tobytes()

  @applyai.expose
  @applyai.tools.json_out()
  def getTargets(self):
    applyai.response.headers['Content-Type'] = "application/json"
    #jstr = '{"targets":' + self.store.fetchTargets(self.name).to_json(orient='records') + '}'
    return self.store.fetchTargets(self.name).to_json(orient='records')

  @applyai.expose
  @applyai.tools.json_out()
  def getConfig(self):
    with open(self.cfgFilename) as json_file:
      self.cfg = json.load(json_file)

    return(self.cfg)

  def exportConfigVariable(self, typ, valueType, var, defaultValue, units, guiText, guiLongText, select=""):
    self.cfg[var] = {}
    self.cfg[var]['type'] = typ
    self.cfg[var]['valueType'] = valueType
    self.cfg[var]['value'] = defaultValue
    self.cfg[var]['units'] = units
    self.cfg[var]['guiText'] = guiText
    self.cfg[var]['guiLongText'] = guiLongText
    self.cfg[var]['select'] = select

  def updateConfig(self):
    # load old config from file in stored
    stored = self.loadConfig()
    for c in self.cfg:
      if not c in stored:
        stored[c] = self.cfg[c]
      for a in self.cfg[c]:
        if self.cfg[c][a] != stored[c][a]:
          self.cfg[c][a] = stored[c][a]

    return self.cfg

  def monitorConfig(self):
    stamp = os.stat(self.cfgFilename).st_mtime
    if stamp != self.cached_stamp:
        self.cached_stamp = stamp
        applyai.log('cfg file modified', self.logname)
        self.cfg = self.updateConfig()
        applyai.engine.publish(self.name + '/monitorConfig', self.cfg)

  def loadConfig(self):
    if os.path.isfile(self.cfgFilename):
      with open(self.cfgFilename) as json_file:
        cfg = json.load(json_file)
      return(cfg)
    return({})

  def saveConfigToFile(self):
    with open(self.cfgFilename, 'w') as outfile:
      outfile.write(json.dumps(self.cfg, indent=2))

  @applyai.expose
  @applyai.tools.json_in()
  @applyai.tools.json_out()
  def saveConfig(self):
    with open(self.cfgFilename, 'w') as outfile:
      outfile.write(json.dumps(applyai.request.json, indent=2))
      return({'info':'updated cfg ' + self.cfgFilename})
    return({'info':'Project file cannot be updated'})
    
  #@applyai.expose
  #def getFrame(self, frame='in', rand=''):

  #  application = applyai.tree.apps['/Project']
  #  plugins = application.config['config']['plugins']

  #  for p in plugins:
  #    if p['name'] == self.name:
  #      path = str('../common/images/frame_%03d_%02d.jpg' % (p['frameIn'], p['camera']))
  #      if frame == 'out':
  #        path = str('../common/images/frame_%03d_%02d.jpg' % (p['frameOut'], p['camera']))
  #      
  #      with open(path, 'rb') as f:
  #        img = f.read()
  #
  #      applyai.response.headers['Content-Type'] = "image/jpg"
  #      return img
  #  
  #  return("no image")
  @applyai.expose
  def index(self):
    html = self.html_header()
    html += '<body onload="init()">'
    html += '<section class="section">'
    html += '<div class="container">'
    html += self.html_name()
    html += '<hr>'
    html += self.html_config()
    html += '<hr>'
    html += self.html_frames()
    html += '<hr>'
    html += self.html_buttons()
    html += '</section></div></body></html>'
    return(html)

  def html_header(self):
    html = '<!DOCTYPE html><html>\n'
    html += '<head>\n'
    html += '<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">\n'
    html += '<title>applyai Plugin Tester</title>\n'
    html += '<style>body {font-family:arial;}</style>\n'
    html += '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.8.0/css/bulma.min.css"/>\n'
    html += self.getJS()
    html += '</head>\n'
    return(html)

  def getJS(self):
    js = '<script type="text/javascript">\n'
    js += 'function init() {\n'
    js += '}\n'
    js += 'function startTest() {\n'
    js += ' get("/' + self.name + '/start", function() {\n'
    js += '   document.getElementById("frameOut").src = "/' + self.name + '/getFrameOut?camera=0&rand=" + Math.random()\n'
    js += ' })\n'
    js += '}\n'
    js += 'function get(what, next) {\n'
    js += 'xhr = new XMLHttpRequest()\n'
    js += 'xhr.open("GET", what)\n'
    js += 'xhr.onload = function() {\n'
    js += ' if (xhr.status === 200) {\n'
    js += '   console.log(xhr.responseText)\n'
    js += '   next()\n'
    js += ' } else {\n'
    js += '   alert("Request failed.  Returned status of " + xhr.status)\n'
    js += ' }\n'
    js += '}\n'
    js += 'xhr.send()\n'
    js += '}\n'
    js += '</script>\n'
    return(js)

  def html_name(self):
    html =  '<div><h2 class="title">applyai Plugin Tester</h2></div>\n'
    html += '<div><h2 class="title">Plugin: ' + self.name + '</h2></div>\n'
    return(html)

  def html_config(self):
    cfg = self.getConfig()
    html = '<div>\n'
    html += 'Description of Plugin: ' + cfg['description']['guiLongText']
    html += '</div>\n'
    return(html)

  def html_frames(self):
    html = '<div><figure class="image is-4by3">\n'
    html += '<img id="frameIn" src="/' + self.name + '/getFrameIn">\n'
    html += '</figure></div>\n'
    html += '<hr>\n'
    html += '<div><figure class="image is-4by3">\n'
    html += '<img id="frameOut" src="/' + self.name + '/getFrameOut">\n'
    html += '</figure></div>\n'
    return(html)

  def html_buttons(self):
    html = '<div>\n'
    html += '<button class="button is-primary" onclick="startTest()">Test</button>\n'
    html += '</div>\n'
    return(html)


class stdPCode:
  
  def __init__(self, name):

    self.logname = name[:6].upper().ljust(6)
    self.name = name
    self.project = os.environ['PROJECT']
    self.cfgFilename = './projects/' + self.project + '/config/' + self.name + '.conf'
    self.cfg = {}
    self.store = ms.memStore(name)

    if not os.path.isfile(self.cfgFilename):
      with open(self.cfgFilename, 'w') as outfile:
        outfile.write('{}')

    self.cached_stamp = os.stat(self.cfgFilename).st_mtime
    self.monitor = job.Job(interval=timedelta(seconds=1), execute=self.monitorConfig)
    self.monitor.start()
    
    applyai.log('init PCode',self.logname)

  def exportConfigVariable(self, typ, valueType, var, defaultValue, units, guiText, guiLongText, select=""):
    self.cfg[var] = {}
    self.cfg[var]['type'] = typ
    self.cfg[var]['valueType'] = valueType
    self.cfg[var]['value'] = defaultValue
    self.cfg[var]['units'] = units
    self.cfg[var]['guiText'] = guiText
    self.cfg[var]['guiLongText'] = guiLongText
    self.cfg[var]['select'] = select

  def updateConfig(self):
    # load old config from file in stored
    stored = self.loadConfig()
    for c in self.cfg:
      if not c in stored:
        stored[c] = self.cfg[c]
      for a in self.cfg[c]:
        if self.cfg[c][a] != stored[c][a]:
          self.cfg[c][a] = stored[c][a]
    return self.cfg

  def monitorConfig(self):
    stamp = os.stat(self.cfgFilename).st_mtime
    if stamp != self.cached_stamp:
        self.cached_stamp = stamp
        applyai.log('cfg file modified', self.logname)
        self.cfg = self.updateConfig()
        applyai.engine.publish(self.name + '/monitorConfig', self.cfg)

  def loadConfig(self):
    if self.name == 'Project':
      cfg = {}
      cfg['list'] = self.application.config['config']['list']
      for c in cfg['list']:
        cfg[c] = self.application.config['config'][c]
    else:
      with open(self.cfgFilename) as json_file:
        cfg = json.load(json_file)
    return(cfg)

  def saveConfig(self):
    with open(self.cfgFilename, 'w') as outfile:
      outfile.write(json.dumps(self.cfg, indent=2))

  def stop(self):
    self.monitor.stop()
    applyai.log('Stopping monitor', self.logname)

  def loadCfgList(self):
    if hasattr(self, 'application'):
      return(self.application.config['config']['list'])
    else:
      application = applyai.tree.apps['/' + self.name]
      return(application.config['config']['list'])
    return([])

  def loadValue(self, valueStr):
    if hasattr(self.cfg, 'application'):
      for value in self.application.config['config']['list']:
        if value == valueStr:
          return self.application.config['config'][value]['value']
      return self.application.config['config']['list']
    else:
      application = applyai.tree.apps['/' + self.name]
      for value in application.config['config']['list']:
        if value == valueStr:
          return application.config['config'][value]['value']
      return application.config['config']['list']
    return('')

