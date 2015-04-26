import os
import shlex
import hashlib

from vaitk import gui
from .. import Search
from .. import linting
from .. import paths
from ..lexer import Lexer
from .. import models
from ..models import commands

from yapsy.PluginManager import PluginManager

class EditorController:
    def __init__(self, editor, global_state, buffer_list):
        self._editor = editor
        self._global_state = global_state
        self._buffer_list = buffer_list
        self._lexer = Lexer()
        self._plugin_manager = PluginManager()
        self._plugin_manager.getPluginLocator().setPluginInfoExtension("ini")
        self._plugin_manager.setPluginPlaces([paths.pluginsDir("user", "commands"), paths.pluginsDir("system", "commands")])
        self._plugin_manager.collectPlugins()

        for plugin_info in self._plugin_manager.getAllPlugins():
            self._plugin_manager.activatePluginByName(plugin_info.name)

        # To speed up resolution, we cache the keyword->plugin association. It is filled lazy
        self._keyword_to_plugin_cache = {}

        self._buffer_list.currentBufferChanged.connect(self.registerCurrentBuffer)

    def registerCurrentBuffer(self, *args):
        self._editor.edit_area.buffer = self._buffer_list.current
        self._editor.status_bar_controller.buffer = self._buffer_list.current
        self._editor.side_ruler_controller.buffer = self._buffer_list.current
        self._editor.info_hover_box.buffer = self._buffer_list.current
        self._lexer.setModel(self._buffer_list.current.document)

    def forceQuit(self):
        for b in self._buffer_list.buffers:
            if b.document.documentMetaInfo("Filename").data() is None:
                continue

            models.EditorState.instance().setCursorPosForPath(
                    os.path.abspath(b.document.documentMetaInfo("Filename").data()),
                    b.cursor.pos)

        models.EditorState.instance().save()
        models.Configuration.save()
        gui.VApplication.vApp.exit()

    def doSave(self):
        self._doSave()
        self._doLint()

    def doSaveAs(self, filename):
        self._doSave(filename)
        self._doLint()

    def doInsertFile(self, filename):
        buffer = self._buffer_list.current

        command = commands.InsertFileCommand(buffer, filename)

        result = command.execute()
        if result.success:
            buffer.command_history.add(command)

    def tryQuit(self):
        if any([b.isModified() for b in self._buffer_list.buffers]):
            self._editor.status_bar.setMessage("Document has been modified. " +
                                               "Use :q! to quit without saving " +
                                               "or :qw to save and quit.", 3000)
        else:
            self.forceQuit()

    def searchForward(self, search_text):
        if search_text == '':
            if self._global_state.current_search is not None:
                search_text = self._global_state.current_search[0]

        if search_text != '':
            self._global_state.current_search = (search_text, Search.SearchDirection.FORWARD)
            Search.find(self._buffer_list.current, search_text, Search.SearchDirection.FORWARD)

    def searchBackward(self, search_text):
        if search_text == '':
            if self._global_state.current_search is not None:
                search_text = self._global_state.current_search[0]

        if search_text != '':
            self._global_state.current_search = (search_text, Search.SearchDirection.BACKWARD)
            Search.find(self._buffer_list.current, search_text, Search.SearchDirection.BACKWARD)

    def selectPrevBuffer(self):
        self._buffer_list.selectPrev()

    def selectNextBuffer(self):
        self._buffer_list.selectNext()

    def doSaveAndExit(self):
        self._doSave()
        self.forceQuit()

    def openFile(self, filename):
        buffer = self._buffer_list.bufferForFilename(filename)
        if buffer is not None:
            self._buffer_list.select(buffer)
            return

        current_buffer = self._buffer_list.current
        new_buffer = models.Buffer()
        status_bar = self._editor.status_bar

        try:
            with open(filename,'r') as f:
                new_buffer.document.read(f)
        except FileNotFoundError:
            status_bar.setMessage("%s [New file]" % filename, 3000)
        except Exception as e:
            status_bar.setMessage("%s [Error: %s]" % (filename, str(e)), 3000)

        new_buffer.document.documentMetaInfo("Filename").setData(filename)
        new_buffer.document.documentMetaInfo("Modified").setData(False)

        initial_md5 = None
        if not new_buffer.document.isEmpty():
            initial_md5 = hashlib.md5(new_buffer.document.documentText().encode("utf-8"))
        new_buffer.document.documentMetaInfo("InitialMD5").setData(initial_md5)

        if current_buffer.isEmpty() and not current_buffer.document.documentMetaInfo("Modified").data():
            self._buffer_list.replaceAndSelect(current_buffer, new_buffer)
        else:
            self._buffer_list.addAndSelect(new_buffer)

        recovered_cursor_pos = models.EditorState.instance().cursorPosForPath(os.path.abspath(filename))
        if recovered_cursor_pos is not None:
            new_buffer.cursor.toPos(recovered_cursor_pos)

        self._doLint()

    def createEmptyBuffer(self):
        self._buffer_list.addAndSelect(models.Buffer())

    def setMode(self, mode):
        self._global_state.edit_mode = mode

    def interpretCommandLine(self, command_line):
        """
        Interprets and dispatch the command line to the plugin system
        (for now. In the future this controller will just handle all commandline execution)
        command_line contains the full command line as specified by the user, as a string.
        """

        command_tokens = shlex.split(command_line)
        keyword = command_tokens[0]

        if keyword not in self._keyword_to_plugin_cache:
            for plugin_info in self._plugin_manager.getAllPlugins():
                plugin_object = plugin_info.plugin_object
                if plugin_object.keyword() == keyword:
                    self._keyword_to_plugin_cache[keyword] = plugin_object

        if keyword in self._keyword_to_plugin_cache:
            plugin_object = self._keyword_to_plugin_cache[keyword]
            plugin_object.execute(command_line)

        # Always return True, regardless. Even if the plugin execution
        # fails, the command was parsed and interpreted correctly
        return True

    # Private

    def _doLint(self):
        document = self._buffer_list.current.document

        linter1 = linting.PyFlakesLinter(document)
        all_info = linter1.runOnce()

        meta_info = {}

        for info in all_info:
            meta_info[info.line] = info

        line_info = document.lineMetaInfo("LinterResult")
        line_info.clear()
        line_info.setDataForLines(meta_info)

    def _doSave(self, filename=None):
        status_bar = self._editor.status_bar
        document = self._buffer_list.current.document

        if filename is not None and len(filename) == 0:
            status_bar.setMessage("Error! Unspecified file name.", 3000)
            return

        status_bar.setMessage("Saving...")
        gui.VApplication.vApp.processEvents()

        if filename is None:
            filename = document.documentMetaInfo("Filename").data()

        if filename is None:
            status_bar.setMessage("Error! Cannot save unnamed file. Please specify a filename with :w filename", 3000)
            return

        try:
            with open(filename,'w') as f:
                document.write(f)
        except Exception as e:
            status_bar.setMessage("Error! Cannot save file. %s" % str(e), 3000)
            return
        else:
            status_bar.setMessage("Saved %s" % filename, 3000)

        document.documentMetaInfo("Filename").setData(filename)
        document.documentMetaInfo("Modified").setData(False)
        document.lineMetaInfo("Change").clear()

