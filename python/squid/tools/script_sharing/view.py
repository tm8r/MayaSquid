# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets

from squid.core.libs.maya import collector
from squid.core.libs.maya import dialog
from squid.core.libs.maya.layout import delete_window
from squid.core.libs.qt.layout import clear_layout
from squid.core.libs.qt.maya_window import MayaWindow
from squid.core.libs.qt.stylesheet import StyleSheet

_TOOL_DICT = {
    "test_widget": "https://gist.github.com/tm8r/e1b4d8071e8137c21f4f18e6f0aef9ed",
    "extract": "https://gist.github.com/tm8r/5afcbe35f00324c5dade98a7fd4cedcb",
    "convert_file_path": "https://gist.github.com/tm8r/2cf9c3c01b34c6467898aeb652b97f41"

}

_CACHE = {}


def _convert_api_url(url):
    return "https://api.github.com/gists/" + url.split("/")[-1]


class ScriptSharing(MayaWindow):
    _ID = "squid_tools_script_sharing"

    def __init__(self):
        u"""initialize"""
        super(ScriptSharing, self).__init__()
        self._makeMayaStandaloneWindow()
        self.setWindowTitle("Script Sharing")
        self.setWindowFlags(QtCore.Qt.Window)
        self.setObjectName(self.window_name())
        self.setProperty("saveWindowPref", True)
        self.setStyleSheet(StyleSheet().core_css)

    @classmethod
    def open(cls, *args):
        u"""UIを表示"""
        delete_window(cls.window_name())
        win = cls()
        win._create_ui()
        win.show()

    def _create_ui(self):
        u"""UIを生成"""
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        self.root_widget = QtWidgets.QFrame(self)
        self.root_widget.setObjectName("root")
        self.setMinimumSize(QtCore.QSize(480, 200))
        self.setCentralWidget(self.root_widget)

        root_layout = QtWidgets.QGridLayout(self.root_widget)
        root_layout.setObjectName("root_layout")
        root_layout.setContentsMargins(8, 8, 8, 8)

        # main_widget = QtWidgets.QFrame()
        # self.content_layout = QtWidgets.QVBoxLayout()
        # main_widget.setLayout(self.inspector_layout)

        # tool_content_wrapper = QtWidgets.QScrollArea()
        # tool_content_wrapper.setWidget(main_widget)
        # tool_content_wrapper.setFrameShape(QtWidgets.QFrame.NoFrame)
        # tool_content_wrapper.setWidgetResizable(True)
        # tool_content_wrapper.setContentsMargins(0, 0, 0, 0)
        #
        # root_layout.addWidget(tool_content_wrapper, 0, 0, 1, 1)
        tool_list_widget = QtWidgets.QFrame()
        self.tool_list_layout = QtWidgets.QVBoxLayout(tool_list_widget)
        self.tool_list_layout.setContentsMargins(0, 0, 0, 0)
        tool_list_widget.setFixedWidth(200)
        # tool_list_size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # tool_list_size_policy.setHorizontalStretch(1)
        # tool_list_widget.setSizePolicy(tool_list_size_policy)
        root_layout.addWidget(tool_list_widget, 0, 0, 1, 1)

        self.tool_detail_layout = QtWidgets.QVBoxLayout()
        root_layout.addLayout(self.tool_detail_layout, 0, 1, 1, 1)

        self._create_content()

    def _create_content(self):
        self._create_tool_list_content()
        self._create_tool_detail_content()

    def _create_tool_list_content(self):
        clear_layout(self.tool_list_layout)

        self.search_line = QtWidgets.QLineEdit()
        self.search_line.setPlaceholderText(u"Search Text...")
        self.tool_list_layout.addWidget(self.search_line)
        self.tools_list_view = QtWidgets.QListWidget()
        self.tool_list_layout.addWidget(self.tools_list_view)
        self.tools_list_view.addItems(_TOOL_DICT.keys())
        self.tools_list_view.currentItemChanged.connect(self._on_tool_select_changed)

    def _on_tool_select_changed(self, current, previous):
        title = current.text()
        url = _TOOL_DICT[title]
        self._update_detail(title, url)

    def get_gist_content(self, url):
        content = _CACHE.get(url, None)
        if content:
            return content

        return self.get_gist(url)

    def get_gist(self, url):
        api_url = _convert_api_url(url)

        import urllib2
        req = urllib2.Request(api_url)
        try:
            response = urllib2.urlopen(req)
            res = response.read()

        except:
            res = ""
        if not res:
            return None

        import json

        content = json.loads(res)
        print("res", content)
        _CACHE[url] = content
        return content

    def _update_detail(self, title, url):
        clear_layout(self.title_layout)
        clear_layout(self.detail_layout)

        heading = QtWidgets.QLabel(title)
        font = QtGui.QFont()
        font.setPointSize(20)
        heading.setFont(font)
        self.title_layout.addWidget(heading)

        content = self.get_gist_content(url)
        print(content)
        self.title_layout.addWidget(QtWidgets.QLabel("description: {0}".format(content["description"].encode('utf-8'))))
        self.title_layout.addWidget(QtWidgets.QLabel("owner: {0}".format(content["owner"]["login"])))
        self.title_layout.addWidget(QtWidgets.QLabel("updated at: {0}".format(content["updated_at"])))

        text = ""
        for name, data in content["files"].items():
            self.detail_layout.addWidget(QtWidgets.QLabel(name))
            text_field = QtWidgets.QPlainTextEdit()
            text_field.setPlainText(data["content"])
            self.detail_layout.addWidget(text_field)

    def _create_tool_detail_content(self):
        clear_layout(self.tool_detail_layout)
        title_widget = QtWidgets.QFrame()
        self.title_layout = QtWidgets.QVBoxLayout(title_widget)

        self.tool_detail_layout.addWidget(title_widget)

        detail_widget = QtWidgets.QFrame()
        self.detail_layout = QtWidgets.QVBoxLayout()
        detail_widget.setLayout(self.detail_layout)

        tool_content_wrapper = QtWidgets.QScrollArea()
        tool_content_wrapper.setWidget(detail_widget)
        tool_content_wrapper.setFrameShape(QtWidgets.QFrame.NoFrame)
        tool_content_wrapper.setWidgetResizable(True)
        tool_content_wrapper.setContentsMargins(0, 0, 0, 0)

        self.tool_detail_layout.addWidget(tool_content_wrapper)


ScriptSharing.open()
