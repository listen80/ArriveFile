import sublime, sublime_plugin
import re,os
path = os.path

def toFile(view, point, dist):

    file = path.basename(dist)
    body = """
        <body>
            <style>
                body {
                    font-family: Arial;
                    color: red;
                }
                a {
                    color: #9517ff;
                }
            </style>
            <a href="%s">%s</a>
        </body>
    """ % (dist, file)

    def on_navigate(href):
        view.window().open_file(href + ":" + "0" + ":" + "0",sublime.ENCODED_POSITION | sublime.FORCE_GROUP)

    view.show_popup(
        body,
        flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY,
        location=point,
        on_navigate=on_navigate,
        max_width=1024)

class arriveFile(sublime_plugin.EventListener):
    def on_hover(self, view, point, hover_zone):
        if hover_zone != sublime.HOVER_TEXT:
            return

        line = view.line(point);
        str = view.substr(line);
        pattern = r"from\s+(['\"])([^/].*)\1"
        result = re.search(pattern, str)
        if not result:
            pattern = r"require\((['\"])([^/].*)\1\)"
            result = re.search(pattern, str)
        if not result:
            pattern = r"(?:src|href)=(['\"])([^/].*?)\1"
            result = re.search(pattern, str)
        if not result:
            return
        dist = result.group(2)

        filename = view.file_name()
        dir = path.dirname(filename)
        ext = path.splitext(filename)[1]

        dist = path.normpath(path.join(dir, dist))
        if path.isfile(dist):
            toFile(view, point, dist)
        elif path.isdir(dist):
            dist = path.join(dist, 'index.js')
            if path.isfile(dist):
                toFile(view, point, dist)
        elif ext:
            dist += ext
            if path.isfile(dist):
                toFile(view, point, dist)