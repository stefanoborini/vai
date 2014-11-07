from .. import FocusPolicy
from .. import core
from . import events
from .VPalette import VPalette
from .VScreen import VScreen
from .events import VFocusEvent
import threading
import queue
import logging
import time

class _VExceptionEvent:
    def __init__(self, exception):
        self.exception = exception

class _KeyEventThread(threading.Thread):
    def __init__(self, screen, key_event_queue, event_available_flag):
        super().__init__()
        self.daemon = True
        self.stop_event = threading.Event()
        self.throttle = threading.Event()
        self.exception = None

        self._screen = screen
        self._key_event_queue = key_event_queue
        self._event_available_flag = event_available_flag


    def run(self):
        while not self.stop_event.is_set():
            last_event = (None, time.time())
            try:
                c = self._screen.getKeyCode()

#                if last_event[0] == c and time.time()-last_event[1] < 0.04:
#                    continue
                last_event = (c, time.time())

                event = events.VKeyEvent.fromNativeKeyCode(c)
                if event is not None:
                    self._key_event_queue.put(event)
                    self._event_available_flag.set()
                else:
                    if hasattr(self, "debug"):
                        logging.info("Unknown key code "+str(c))

                self.throttle.wait()
                self.throttle.clear()
            except Exception as e:
                event = _VExceptionEvent(e)
                self._key_event_queue.put(event)
                self._event_available_flag.set()

    def registerTimer(self, timer):
        pass

class VApplication(core.VCoreApplication):

    def __init__(self, argv, screen=None):
        from . import VWidget
        super().__init__(argv)
        if screen is not None:
            self._screen = screen
        else:
            self._screen = VScreen()

        self._root_widget = VWidget()
        self._focus_widget = None
        self._palette = self.defaultPalette()
        self._event_available_flag = threading.Event()
        self._event_queue = queue.Queue()
        self._key_event_queue = queue.Queue()
        self._key_event_thread = _KeyEventThread(self._screen, self._key_event_queue, self._event_available_flag)
        self._delete_later_queue = []
        self._exit_flag = False

        # Signals.
        self.lastWindowClosed = core.VSignal(self)
        self.focusChanged = core.VSignal(self)

    def exec_(self):
        self._root_widget.show()
        self.processEvents(True)
        self._key_event_thread.start()
        while self._exit_flag != True:
            self.logger.info("Waiting for events")
            self._event_available_flag.wait()
            self._event_available_flag.clear()
            self.logger.info("Event available")
            self.processEvents(True)
            self._key_event_thread.throttle.set()

        self._exitCleanup()

    def processEvents(self, native=False):
        self.logger.info("++++---- %s processing events ---+++++" % ("Native" if native else "Forced"))
        self._processKeyEvents()
        self._processRemainingEvents()
        self._deleteScheduled()
        self.logger.info("===================================")
        self._screen.refresh()

    def postEvent(self, receiver, event):
        self.logger.info(" <posted " + str(receiver) + " " + str(event))
        self._event_queue.put((receiver, event))
        self._event_available_flag.set()

    def exit(self):
        self._exit_flag = True

    def addTopLevelWidget(self, widget):
        self._root_widget.addChild(widget)

    def deleteLater(self, widget):
        self.logger.info("Added widget %s to deleteLater queue" % str(widget))
        self._delete_later_queue.append(widget)

    def screen(self):
        return self._screen

    def focusWidget(self):
        return self._focus_widget

    def setFocusWidget(self, widget):
        if self._focus_widget is widget:
            return

        self.logger.info("Setting focus on widget %s." % widget)

        if self._focus_widget is not None:
            self.logger.info("Focus out on widget %s." % self._focus_widget)
            VApplication.vApp.postEvent(self._focus_widget, VFocusEvent(core.VEvent.EventType.FocusOut))

        self._focus_widget = None
        if widget is not None:
            if widget.focusPolicy() == FocusPolicy.NoFocus:
                self.logger.info("Focus not accepted on widget %s due to its focus policy." % self._focus_widget)
                return

            self._focus_widget = widget
            VApplication.vApp.postEvent(self._focus_widget, VFocusEvent(core.VEvent.EventType.FocusIn))

    def defaultPalette(self):
        palette = VPalette()
        palette.setDefaults()
        return palette

    def palette(self):
        return self._palette

    def rootWidget(self):
        try:
            return self._root_widget
        except AttributeError:
            self._root_widget = None
            return self._root_widget

    def resetScreen(self):
        self._screen.reset()

    def topLevelWidgets(self):
        raise NotImplementedError()

    def allWidgets(self):
        raise NotImplementedError()

    def activeWindow(self):
        raise NotImplementedError()

    def setActiveWindow(self, window):
        raise NotImplementedError()

    def closeAllWindows(self):
        raise NotImplementedError()

    def event(self, event):
        raise NotImplementedError()

    def clipboard(self):
        raise NotImplementedError()

    def keyboardModifiers(self):
        raise NotImplementedError()

    def notify(self):
        raise NotImplementedError()

    # Private

    def _hideScheduled(self):
        self.logger.info("Widget scheduled for deletion: %s" % str(self._delete_later_queue))
        for w in self._delete_later_queue:
            self.logger.info("Posting hide events for deleted widget %s" % str(w))
            w.hide()

    def _deleteScheduled(self):
        for w in self._delete_later_queue:
            w.parent().removeChild(w)

        self._delete_later_queue.clear()

    def _processKeyEvents(self):
        while True:
            self.logger.info("key queue %d" % self._key_event_queue.qsize())
            try:
                event = self._key_event_queue.get_nowait()
            except queue.Empty:
                event = None

            if event is None:
                return

            if isinstance(event, events.VKeyEvent):
                self._processSingleKeyEvent(event)
            elif isinstance(event, _VExceptionEvent):
                raise event.exception

    def _processSingleKeyEvent(self, key_event):
        self.logger.info("Key event %d %x" % (key_event.key(), key_event.modifiers()))

        if not self.focusWidget():
            self.logger.info("Key event ignored. No widget has focus.")
            return

        key_event.setAccepted(False)
        for widget in self.focusWidget().traverseToRoot():
            self.logger.info("KeyEvent attempting delivery to "+str(widget))
            stop_event = False
            for event_filter in reversed(widget.installedEventFilters()):
                stop_event = stop_event | event_filter.eventFilter(key_event)
                if key_event.isAccepted():
                    self.logger.info("KeyEvent accepted by filter "+str(event_filter))
                    return

            if not stop_event:
                self.logger.info("KeyEvent not stopped. Sending to widget "+str(widget))
                widget.keyEvent(key_event)

                if key_event.isAccepted():
                    self.logger.info("KeyEvent accepted by "+str(widget))
                    return

    def _processRemainingEvents(self):
        previous_data = None
        while True:
            try:
                receiver, event = self._event_queue.get_nowait()
            except queue.Empty:
                receiver, event = None, None

            if event is None:
                break

            if previous_data is not None:
                prev_receiver, prev_event = previous_data
                if event.eventType() == prev_event.eventType() and receiver == prev_receiver:
                   continue

            self.logger.info("Data queue %d. Processing %s -> %s." % (self._event_queue.qsize(), str(event), str(receiver)))
            receiver.event(event)
            previous_data = (receiver, event)

            #self._stop_flag.append(1)
        # Check if screen was re-sized (True or False)
        #x,y = self._screen.size()
        #resize = curses.is_term_resized(y, x)

        # Action in loop if resize is True:
        #if resize is True:
            #x, y = self._screen.size()
            #curses.resizeterm(y, x)
            #self.renderWidgets()

    def _exitCleanup(self):
        self._key_event_thread.stop_event.set()
        self._screen.reset()
        super().exit()

