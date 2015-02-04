from vai.sdk import CommandPlugin

class FoobarPlugin(CommandPlugin):

    def __init__(self):
        super().__init__("foobar", 1, 0)

    @property
    def keyword(self):
        return "foobar"

    def invoke(self, command_line, editor_app):
        editor_app.editor.status_bar.setMessage("Foo!",2000)




def plugins():
    return [ FoobarPlugin() ]
