from vaitk import gui
from .Editor import Editor
from . import models
import random
import os


class EditorApp(gui.VApplication):
    @staticmethod
    def editorConfigPath():
        _home = os.path.expanduser('~')
        xdg_config_home = os.environ.get('XDG_CONFIG_HOME') or \
                          os.path.join(_home, '.config')
        config_dir = os.path.join(xdg_config_home, 'vai')
        if not os.path.isdir(config_dir):
            os.makedirs(config_dir)
        return os.path.join(config_dir, 'vairc')

    def __init__(self, filename=None, argv=None):
        super().__init__(argv)

        config_file = self.editorConfigPath()
        if os.path.exists(config_file):
            try:
                models.Configuration.initFromFile(config_file)
            except:
                pass
        # We keep them at the App level because the app will be responsible
        # for coordinating the async system in the future.
        self._global_model = models.GlobalState()

        if filename is not None:
            first_buffer = models.Buffer.newBufferForFilename(filename)
        else:
            first_buffer = models.Buffer()

        self._buffer_list = models.BufferList(first_buffer)

        self._editor = Editor(self._global_model, self._buffer_list)
        self._editor.show()

    def dumpBuffers(self, destination_dir=None):
        """
        Dump the buffers to your home directory in case of a crash.
        Returns the list of files dumped down.
        """

        if destination_dir is None:
            destination_dir = os.path.expanduser("~")

        file_list = []

        for buffer in self._buffer_list.buffers:
            document_text = buffer.document.documentText()
            document_name = buffer.document.filename() or "noname"
            random_number = random.randint(1, 100000)
            path = os.path.join(destination_dir, "vaidump-%s-%d.txt" % (os.path.basename(document_name), random_number))

            with open(path, "w") as f:
                f.write(document_text)

            file_list.append(path)

        return file_list
