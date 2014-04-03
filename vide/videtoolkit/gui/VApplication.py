from .. import core
from ..core import events as coreevents
from . import events
from .VPalette import VPalette
from .VScreen import VScreen
from .VPainter import VPainter
import threading
import Queue
import logging
import os

class KeyEventThread(threading.Thread):
    def __init__(self, screen, key_event_queue, event_available_flag):
        super(KeyEventThread, self).__init__()
        self.daemon = True
        self.exception_occurred_event = threading.Event()
        self.stop_event = threading.Event()
        self.exception = None

        self._screen = screen
        self._key_event_queue = key_event_queue
        self._event_available_flag = event_available_flag

    def run(self):
        try:
            while not self.stop_event.is_set():
                c = self._screen.getKeyCode()
                event = events.VKeyEvent.fromNativeKeyCode(c)
                if event is not None:
                    self._key_event_queue.put(event)
                    self._event_available_flag.set()
                else:
                    logging.info("Unknown key code "+str(c))
        except Exception as e:
            self.exception = e
            self.exception_occurred_event.set()

    def registerTimer(self, timer):
        pass

class VApplication(core.VCoreApplication):
    def __init__(self, argv, screen=None):
        super(VApplication, self).__init__(argv)
        if screen:
            self._screen = screen
        else:
            self._screen = VScreen()

        self._top_level_widgets = []
        self._focused_widget = None
        self._palette = self.defaultPalette()
        self._event_available_flag = threading.Event()
        self._event_queue = Queue.Queue()
        self._key_event_queue = Queue.Queue()
        self._key_event_thread = KeyEventThread(self._screen, self._key_event_queue, self._event_available_flag)

    def exec_(self):
        self._key_event_thread.start()
        for w in self._top_level_widgets:
            self.postEvent(w, events.VPaintEvent())
        while True:
            if self._key_event_thread.exception_occurred_event.is_set():
                raise self._key_event_thread.exception
            logging.info("Waiting for events")
            self._event_available_flag.wait()
            self._event_available_flag.clear()
            logging.info("Event available")
            self.processEvents()
            self._screen.refresh()

    def processEvents(self):
        logging.info("---- processing events -------")
        while True:
            try:
                key_event = self._key_event_queue.get_nowait()
            except Queue.Empty:
                key_event = None

            if key_event is None:
                break

            if isinstance(key_event, events.VKeyEvent):
                logging.info("Key event %d %x" % (key_event.key(), key_event.modifiers()))
                if not self.focusedWidget():
                    logging.info("Key event ignored. No widget has focus.")
                    continue

                key_event.setAccepted(False)
                for widget in self.focusedWidget().traverseToRoot():
                    logging.info("Attempting delivery to "+str(widget))
                    widget.keyEvent(key_event)
                    if key_event.accepted():
                        logging.info("Event accepted by "+str(widget))
                        break

        while True:
            try:
                receiver, event = self._event_queue.get_nowait()
            except Queue.Empty:
                receiver, event = None, None

            if event is None:
                break

            if isinstance(event, events.VPaintEvent):
                logging.info("Paint event. Receiver "+str(receiver))
                repaint_queue = [receiver]
                while len(repaint_queue) > 0:
                    widget = repaint_queue.pop(0)
                    if not widget.isVisible():
                        logging.info("Widget %s not visible. skipping." % str(widget))
                        continue

                    logging.info("Widget %s visible. painting." % str(widget))
                    widget.paintEvent(event)
                    repaint_queue.extend(widget.children())

            elif isinstance(event, coreevents.VTimerEvent):
                receiver.timerEvent(event)

        logging.info("---- Done processing events -------")

            #self._stop_flag.append(1)
        # Check if screen was re-sized (True or False)
        #x,y = self._screen.size()
        #resize = curses.is_term_resized(y, x)

        # Action in loop if resize is True:
        #if resize is True:
            #x, y = self._screen.size()
            #curses.resizeterm(y, x)
            #self.renderWidgets()

    def postEvent(self, receiver, event):
        logging.info("Posting event: " + str(receiver) + " " + str(event))
        self._event_queue.put((receiver, event))
        self._event_available_flag.set()

    def exit(self):
        super(VApplication, self).exit()
        self._key_event_thread.stop_event.set()
        self._screen.deinit()

    def addTopLevelWidget(self, widget):
        self._top_level_widgets.append(widget)

    def screen(self):
        return self._screen

    def setFocusWidget(self, widget):
        self._focused_widget = widget

    def focusedWidget(self):
        return self._focused_widget

    def defaultPalette(self):
        palette = VPalette()
        palette.setDefaults()
        return palette

    def palette(self):
        return self._palette

