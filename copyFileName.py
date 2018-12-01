import sublime
import sublime_plugin
import os

class CopyFileNameCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if len(self.view.file_name()) > 0:
            sublime.set_clipboard(os.path.basename(self.view.file_name()))
            sublime.status_message("Copied file name")

    def is_enabled(self):
        return self.view.file_name() is not None and len(self.view.file_name()) > 0
