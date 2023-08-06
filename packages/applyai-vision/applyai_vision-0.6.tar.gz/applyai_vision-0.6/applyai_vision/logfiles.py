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
from cherrypy.process.plugins import SimplePlugin
import os
import datetime
import re
import paho.mqtt.client as mqtt
import logging
import logging.config

applyai._cplogging.LogManager.time = lambda self : '[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:23] + ']'
applyai._cplogging.LogManager.access_log_format = ( '{t} WEBGUI {h} "{r}" {s} {b}' ) #"{f}" "{a}"'  )
#applyai._cplogging.LogManager(logger_root = "applyai")

class Logs(object):
  def __init__(self):
    self.perPage = 20

  exposed = True
  def GET(self, page=1):
    page = int(page)
    if page < 1:
      page = 1
    start  = (page-1) * self.perPage
    finish = start + self.perPage

    filename  = '../common/logs/error.log'
    # html = '<table id="logtable" class="table">'
    html = '<tr><th>timestamp</th><th>source</th><th>message</th></tr>\n'
    with open(filename) as fp:
      idx = 0
      for line in self.reversed_fp_iter(fp, 256):
        if idx >= start:
          line = line.replace('\n','')
          s = line.split(' ')
          if len(s) > 2:
            html += '<tr>'
            html += '<td style="padding: 0px;white-space: nowrap;">' + s[0].replace('[','') + ' ' + s[1].replace(']','') + '</td>' 
            html += '<td style="padding: 0px">' + s[2] + '</td>'
            tmp = ''
            for i in range(3,len(s)):
              tmp += s[i] + ' '
            html += '<td style="padding: 0px">' + tmp + '</td>' 
            html += '</tr>'

        idx += 1
        if idx > finish:
          break
    #html += '</table>'
    applyai.response.headers['Content-Type'] = "text/html"
    return html

  def reversed_fp_iter(self, fp, buf_size=1024):
      """a generator that returns the lines of a file in reverse order
      ref: https://stackoverflow.com/a/23646049/8776239
      """
      segment = None  # holds possible incomplete segment at the beginning of the buffer
      offset = 0
      fp.seek(0, os.SEEK_END)
      file_size = remaining_size = fp.tell()
      while remaining_size > 0:
          offset = min(file_size, offset + buf_size)
          fp.seek(file_size - offset)
          buffer = fp.read(min(remaining_size, buf_size))
          remaining_size -= buf_size
          lines = buffer.splitlines(True)
          # the first line of the buffer is probably not a complete line so
          # we'll save it and append it to the last line of the next buffer
          # we read
          if segment is not None:
              # if the previous chunk starts right from the beginning of line
              # do not concat the segment to the last line of new chunk
              # instead, yield the segment first
              if buffer[-1] == '\n':
                  #print 'buffer ends with newline'
                  yield segment
              else:
                  lines[-1] += segment
                  #print 'enlarged last line to >{}<, len {}'.format(lines[-1], len(lines))
          segment = lines[0]
          for index in range(len(lines) - 1, 0, -1):
              if len(lines[index]):
                  yield lines[index]
      # Don't yield None if the file was empty  hhh
      if segment is not None:
          yield segment

class LogfilePlugin(SimplePlugin):
  
  def __init__(self, bus):
    SimplePlugin.__init__(self, bus)
    self.name = "logs"
    self.logname = self.name.upper().ljust(6)
    self.client = None
    applyai.log('in init', self.logname)

    # grab the current LogRecordFactory
    self.old_factory = logging.getLogRecordFactory()

  def start(self):
    '''Called when the engine starts'''
    # create a mqtt client
    self.client = mqtt.Client()
    self.client.on_connect = self.on_connect
    self.client.connect("localhost", 1883, 60)
    logging.setLogRecordFactory(self.record_factory)
    applyai.log('Starting up MQTT client' + self.logname, self.logname)
    #self.client.loop_forever(timeout=1.0, max_packets=1, retry_first_connection=False)
    self.client.loop_start()

  def stop(self):
    '''Called when the engine stops'''
    if self.client != None:
      self.client.loop_stop(force=False)
      self.client.disconnect()
    applyai.log('Stopping ' + self.logname, self.logname)

  def on_connect(self, client, userdata, flags, rc):
    applyai.log("Connected with result code "+str(rc), self.logname)

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

  # add mqtt publish to the current LogRecordFactory
  # this will catch all logs and send them on to the mqtt broker
  def record_factory(self, *args, **kwargs):
    record = self.old_factory(*args, **kwargs)
    logstr = self.replacenth(record.getMessage(), ' ', '@', 2)
    logstr = self.replacenth(logstr, ' ', '@', 2).replace('@  ','@').replace('@ ','@')
    self.client.publish('logger/message', logstr)
    return record

  def replacenth(self, string, sub, wanted, n):
    where = [m.start() for m in re.finditer(sub, string)][n-1]
    before = string[:where]
    after = string[where:]
    after = after.replace(sub, wanted, 1)
    newString = before + after
    return newString
