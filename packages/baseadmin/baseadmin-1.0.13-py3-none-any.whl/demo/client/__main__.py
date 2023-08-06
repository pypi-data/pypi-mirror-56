import logging
logger = logging.getLogger(__name__)

import sys

from baseadmin.storage  import db
from baseadmin.endpoint import register, run, command, me, socketio

# import custom components
from baseadmin.components.system.actions   import client
from baseadmin.components.system.screen    import client
from baseadmin.components.system.wifi      import client
from baseadmin.components.content.download import client

# example "bulky" state update command
@command("update")
def on_update(state):
  logger.info("updating state")
  me.state = state

# example background reporting thread
def report():
  while True:
    if me.connected:
      socketio.emit("report", "hello from {0}".format(me.name))
    socketio.sleep(300)

socketio.start_background_task(report)

try:
  run()
  logger.fatal("run ended...")
except KeyboardInterrupt:
  pass
