#!/user/bin/env python3
###################################################################################
#                                                                                 #
# AUTHOR: Michael Brockus.                                                        #
#                                                                                 #
# CONTACT: <mailto:michaelbrockus@gmail.com>                                      #
#                                                                                 #
# LICENSE: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0                 #
#                                                                                 #
###################################################################################

mesonui_green = '''
QTextEdit {
    background-attachment: scroll;
    background-color: rgb(63, 63, 63);
    border-color: rgb(245, 251, 251);
    border-style: outset;
    border-width: 1px;
    border-radius: 10px;
    border-color: beige;
    padding: 6px;
    color: rgb(63, 255, 6);
    font: 13pt "Monaco";
}
'''

mesonui_error = '''
QTextEdit {
    background-attachment: scroll;
    background-color: rgb(63, 63, 63);
    border-color: rgb(245, 251, 251);
    border-style: outset;
    border-width: 1px;
    border-radius: 10px;
    border-color: beige;
    padding: 6px;
    color: rgb(252, 29, 7);
    font: 13pt "Monaco";
}
'''


class MesonUiConsole:
    def __init__(self, context=None):
        self._context = context
        self._context.meson.process().setProcessChannelMode(self._context.meson.process().SeparateChannels)
        self._context.meson.process().readyReadStandardOutput.connect(lambda: self._child_process_stdout())
        self._context.meson.process().readyReadStandardError.connect(lambda: self._child_process_stderr())
        self._context.meson.process().started.connect(lambda: self._child_process_started())

    def append_line(self, text: str) -> None:
        if text == '':
            return
        cursor = self._context.mesonui_output_console.textCursor()
        self._context.mesonui_output_console.setTextCursor(cursor)
        cursor.setPosition(cursor.Start)
        cursor.movePosition(cursor.Left, cursor.KeepAnchor, 3)
        self._context.mesonui_output_console.ensureCursorVisible()

    def _child_process_started(self):
        msg: str = str('[***    Process Started    ***]')
        self._context.mesonui_output_console.setStyleSheet(mesonui_green)
        self._context.mesonui_output_console.setText(msg)
        self.append_line(msg)

    def _child_process_stdout(self):
        out: str = str(self._context.meson.process().readAllStandardOutput(), 'utf8')
        self._context.mesonui_output_console.setStyleSheet(mesonui_green)
        self._context.mesonui_output_console.setText(out)
        self.append_line(out)

    def _child_process_stderr(self):
        err: str = str(self._context.meson.process().readAllStandardError(), 'utf8')
        self._context.mesonui_output_console.setStyleSheet(mesonui_error)
        self._context.mesonui_output_console.setText(err)
        self.append_line(err)
