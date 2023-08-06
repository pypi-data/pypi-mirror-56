#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide2.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QTextBrowser, QTextEdit, QPlainTextEdit, QSizePolicy, \
    QMessageBox, QShortcut, QToolBar, QAction, QPushButton, QScrollBar, QAbstractSlider
from mistune import Markdown, Renderer
from PySide2.QtGui import QFont, QFontMetrics, QKeySequence, QKeyEvent, QTextDocument, QTextCursor
from PySide2.QtCore import QMargins, Signal
from PySide2.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from os import path, stat
from rx import operators as ops, scheduler
from .FileUtils import updateFile
import qtawesome as qta
import PySide2
import rx
import typing
from scheduler.PySild2QtScheduler import qtScheduler


class PreView(QTextBrowser):
    call = Signal(object)

    def __init__(self, parent=None):
        super(PreView, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.__html = ''
        self.setOpenLinks(False)
        self.networkAccessManager: QNetworkAccessManager = None
        self.imageDict: dict = dict()
        self.setReadOnly(True)

    @property
    def html(self):
        return self.__html

    @html.setter
    def html(self, html):
        self.__html = html
        self.setHtml(html)

    def notifyScroll(self, dx, dy):
        self.scroll(dx, dy)

    def openLinks(self) -> bool:
        print("openLinks")
        return False

    def openExternalLinks(self) -> bool:
        print("openExternalLinks")
        return False

    def loadResource(self, type: int, name: PySide2.QtCore.QUrl) -> typing.Any:
        if type == QTextDocument.ImageResource:
            if str(name.url()).startswith("http://") or str(name.url()).startswith("https://"):
                if not self.networkAccessManager:
                    self.networkAccessManager = QNetworkAccessManager(self)
                if not self.imageDict.get(name.url()):

                    self.imageDict[name.url()] = False
                    requst: QNetworkRequest = QNetworkRequest()
                    requst.setUrl(name)
                    reply = self.networkAccessManager.get(requst)
                    reply.finished.connect(self.replyFinished)
                    return
                else:
                    return

        # return QTextDocument.loadResource(type, name)

    def replyFinished(self):
        reply: QNetworkReply = self.sender()
        reply.deleteLater()
        self.document().addResource(QTextDocument.ImageResource, reply.url(), reply.readAll())
        self.imageDict[reply.url()] = True
        self.document().adjustSize()

    def scrollToLine(self, lineNumber):
        cursor = QTextCursor(self.document().findBlockByLineNumber(lineNumber))
        self.topText.setTextCursor(cursor)


class LeftEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        QPlainTextEdit.__init__(self, parent)
        self.init()
        self.initEvent()

    def init(self):
        self.scrollCallBack = None
        self.haseSave = True
        self.showLineCount = None

    def initEvent(self):
        scrollBar: QScrollBar = self.verticalScrollBar()
        scrollBar.mi = self.sliderChangeCall

    def sliderChangeCall(self, change: QAbstractSlider.SliderChange):
        print(change)
        print("#sliderChangeCall change:%s" % change)

    def scroll(self, dx: int, dy: int):
        print("scroll dx:%s dy:%s" % (dx, dy))
        super(LeftEdit, self).scroll(dx, dy)

    def scrollContentsBy(self, dx: int, dy: int):

        if dy > 0:
            print("下滑 第一个可见line:%s| 最后一个可见行: %s" % (
                self.firstVisibleBlock().blockNumber(), self.getLastVisibleBlock()))
            if self.scrollCallBack:
                self.scrollCallBack(self.firstVisibleBlock().blockNumber(), -1)

        elif dy < 0:
            print("上滑 第一个可见line:%s| 最后一个可见行: %s" % (
                self.firstVisibleBlock().blockNumber(), self.getLastVisibleBlock()))
            if self.scrollCallBack:
                self.scrollCallBack(self.firstVisibleBlock().blockNumber(), 1)

        super(LeftEdit, self).scrollContentsBy(dx, dy)

    def scrollCallBack(self, firstVisitLine, up):
        pass

    def keyPressEvent(self, e: QKeyEvent):
        print(e.key())
        print(e.text())
        if e.key() == 16777217:
            self.handleTest(e)
        else:
            super(LeftEdit, self).keyPressEvent(e)

    def handleTest(self, e: QKeyEvent):
        tab = "\t"

        cursor = self.textCursor()

        if cursor.hasSelection():
            start = cursor.selectionStart()
            end = cursor.selectionEnd()
            # 设置游标位置到最后
            cursor.setPosition(end)

            # 移动到选择的行的最后位置
            cursor.movePosition(cursor.StartOfLine)
            # 获取选择的段落的最终位置
            end = cursor.position()
            # cursor.movePosition(cursor.StartOfBlock)
            # endNumber = cursor.blockNumber()

            # 游标恢复到选择的开始位置
            cursor.setPosition(start)
            # cursor.movePosition(cursor.StartOfBlock)
            # startNumber = cursor.blockNumber()
            # print("startNumber = %s and endNumber = %s" % (startNumber, endNumber))
            # self.insertTab(startNumber, endNumber)
            # 移动到开始的问题的行头
            cursor.movePosition(cursor.StartOfLine)
            # 获取开始位置
            start = cursor.position()

            while start < end:
                cursor.movePosition(cursor.StartOfLine)

                _left = cursor.position()
                cursor.movePosition(cursor.EndOfLine)
                _right = cursor.position()

                cursor.movePosition(cursor.StartOfLine)
                cursor.insertText(tab)
                cursor.movePosition(cursor.NextBlock)
                cursor.movePosition(cursor.StartOfLine)
                lineLenght = _right - _left
                start = start + lineLenght
                # cursor.movePosition(cursor.StartOfLine)
        else:
            super(LeftEdit, self).keyPressEvent(e)

    def insertTab(self, satrt, end):
        self.document()
        txt = self.toPlainText()
        lines = txt.split("\n")
        for index, value in enumerate(lines):
            if index >= satrt and index <= end:
                lines[index] = "%s%s\n" % ("\t", value)
            else:
                lines[index] = "%s\n" % value

        self.setPlainText("".join(lines))

    def getLastVisibleBlock(self) -> int:
        if not self.showLineCount:
            self.showLineCount = self.getShowLines()
        lastVisibleBlockNumber = int(self.showLineCount) + self.firstVisibleBlock().blockNumber()
        return lastVisibleBlockNumber

    def getShowLines(self) -> int:
        height = self.height()
        lineHeight = self.blockBoundingRect(self.firstVisibleBlock()).height()
        showLineCount = height / lineHeight
        return int(showLineCount)


class ToolBarButton(QPushButton):
    def __init__(self, parent=None):
        QPushButton.__init__(self, parent)

    def setAwesomeIcon(self, iconName):
        icon = qta.icon(iconName,
                        active=iconName,
                        color='gray',
                        color_active='blue')
        self.setIcon(icon)


class ToolBarMenuInfo:
    def __init__(self, id: str = None, icon: str = None, shortcut: str = None, separator: bool = False):
        self.id = id
        self.icon = icon
        self.shortcut = shortcut
        self.separator = separator


class MkEdit(QWidget):
    def __init__(self, parent=None):
        print("EditWidget __init__")
        QWidget.__init__(self, parent)
        self.init()
        self.initUI()
        self.initEvent()
        self.initToolBar()
        self.refreshToolBar()

    def init(self):
        renderer = Renderer(escape=True, hard_wrap=True)
        self.markdown = Markdown(renderer=renderer)
        self.toolBar: QToolBar = QToolBar(self)
        self.toolBarMenusList = list()
        self.enableRightPreView: bool = False
        self.fullScreenPreModel: bool = False

        self.rightPreView = None
        self.lastModifyTime = None

    def initUI(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.contentLayout = QHBoxLayout(self)
        self.contentLayout.setSpacing(0)
        self.leftEdit = LeftEdit(self)
        self.initLeftEdit()
        self.contentLayout.addWidget(self.leftEdit, 1)
        self.enableRightView(self.enableRightPreView)
        if self.toolBar:
            self.mainLayout.addWidget(self.toolBar)
        self.mainLayout.addLayout(self.contentLayout, 1)
        self.setLayout(self.mainLayout)

    def initLeftEdit(self):
        shortcut = QShortcut(QKeySequence("Ctrl+S"), self.leftEdit)
        shortcut.activated.connect(self.save)
        font = QFont("Menlo", 14)
        self.leftEdit.setFont(font)
        self.leftEdit.setTabStopWidth(4 * QFontMetrics(font).width(" "))

    def initEvent(self):
        self.leftEdit.textChanged.connect(self.leftEditTextChange)
        self.startAutoSaveTask()
        # self.leftEdit.scrollCallBack = self.fireScroll

    def fireScroll(self, firstVisitLine, up):
        if self.rightPreView:
            self.leftEdit.document()
            print("fireScroll# firstVisitLine:%s up%s" % (firstVisitLine, up))
            cursor = QTextCursor(
                self.rightPreView.document().findBlockByLineNumber(int(firstVisitLine)))
            self.rightPreView.setTextCursor(cursor)

    def startAutoSaveTask(self):
        rx.interval(10).pipe(
            qtScheduler.QtScheduler()
        ).subscribe(
            on_next=lambda v: self.trySave()
        )

    def trySave(self):
        print("trySave window is active:%s" % self.isActiveWindow())
        if not self.isActiveWindow():
            return
        if self.checkFileChange():
            # 提示用户源文件已发生改变
            msgBox = QMessageBox()
            msgBox.setText("%s-源文档已被修改" % self.fileName)
            msgBox.setInformativeText("点击YES将更新改动内容至当前文档,点击NO将以当前文本内容覆盖本地内容")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgBox.setDefaultButton(QMessageBox.Yes)
            ret = msgBox.exec_()
            print("ret:%s" % ret)
            if ret == QMessageBox.Yes:
                print("Yes")
                self.loadData(self.filePath)

            elif ret == QMessageBox.No:
                print("No")

                self.startSave()

    def initToolBar(self):
        self.toolBarMenusList.clear()
        self.toolBar.clear()
        self.toolBarMenusList.append(ToolBarMenuInfo("undo", "fa5s.undo-alt"))

        self.toolBarMenusList.append(ToolBarMenuInfo("redo", "fa5s.redo-alt"))

        self.toolBarMenusList.append(ToolBarMenuInfo("save", "fa5s.save"))

        self.toolBarMenusList.append(ToolBarMenuInfo(separator=True))

        self.toolBarMenusList.append(ToolBarMenuInfo("bold", "fa5s.bold"))

        self.toolBarMenusList.append(ToolBarMenuInfo("italic", "fa5s.italic"))

        self.toolBarMenusList.append(ToolBarMenuInfo("heading", "fa5s.heading"))
        self.toolBarMenusList.append(ToolBarMenuInfo(separator=True))

        self.toolBarMenusList.append(ToolBarMenuInfo("quote", "fa5s.quote-left"))

        self.toolBarMenusList.append(ToolBarMenuInfo("list-ul", "fa5s.list-ul"))

        self.toolBarMenusList.append(ToolBarMenuInfo("list-ol", "fa5s.list-ol"))

        self.toolBarMenusList.append(ToolBarMenuInfo(separator=True))

        self.toolBarMenusList.append(ToolBarMenuInfo("link", "fa5s.link"))
        self.toolBarMenusList.append(ToolBarMenuInfo("images", "fa5s.images"))
        self.toolBarMenusList.append(ToolBarMenuInfo(separator=True))

        self.toolBarMenusList.append(ToolBarMenuInfo("eye", "fa5s.eye"))
        self.toolBarMenusList.append(ToolBarMenuInfo("exchange", "fa5s.exchange-alt", shortcut='Ctrl+E'))
        self.toolBarMenusList.append(ToolBarMenuInfo("arrows", "fa5s.arrows-alt"))
        self.toolBarMenusList.append(ToolBarMenuInfo(separator=True))

        self.toolBarMenusList.append(ToolBarMenuInfo("question", "fa5s.question-circle"))

    def refreshToolBar(self):
        for data in self.toolBarMenusList:
            if data.separator:
                self.toolBar.addSeparator()
            else:
                menu = ToolBarButton()
                menu.setAwesomeIcon(data.icon)
                menu.setProperty("id", data.id)
                menu.clicked.connect(self.clickToolBarMenu)

                if data.shortcut:
                    shortcut = QShortcut(QKeySequence(data.shortcut), self)
                    shortcut.setProperty("id", data.id)
                    shortcut.setProperty("shortcut", data.shortcut)
                    shortcut.activated.connect(self.fireToolBarMenusShortcut)
                self.toolBar.addWidget(menu)

    def fireToolBarMenusShortcut(self):
        shortcut = self.sender().property("shortcut")
        print("fireToolBarMenusShortcut# shortcut=%s" % shortcut)
        if shortcut == "Ctrl+E":
            self.enableRightView(not self.enableRightPreView)

    def clickToolBarMenu(self):
        id = self.sender().property("id")
        print("clickToolBarMenu# id=%s" % id)
        if id == 'exchange':
            self.enableRightView(not self.enableRightPreView)
        elif id == "redo":
            self.leftEdit.redo()
        elif id == "undo":
            self.leftEdit.undo()
        elif id == "save":
            self.save()
        elif id == "arrows":
            self.enableFullScreenPreModel()

    def enableFullScreenPreModel(self):
        pass

    def enableRightView(self, enable):
        if self.enableRightPreView != enable:
            self.enableRightPreView = enable
            if self.enableRightPreView:
                if not self.rightPreView:
                    self.rightPreView = PreView(self)
                    self.contentLayout.addWidget(self.rightPreView, 1)
                    self.foreRefreshPreViewInfo()

            else:
                if self.rightPreView:
                    self.contentLayout.removeWidget(self.rightPreView)
                    self.rightPreView.deleteLater()
                    del self.rightPreView
                    self.rightPreView = None

    def interceptClose(self):
        if path.exists(self.filePath) and not self.haseSave:
            msgBox = QMessageBox()
            msgBox.setText("%s-文档已被修改" % self.fileName)
            msgBox.setInformativeText("是否保存修改后的文档")
            msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Save)
            ret = msgBox.exec_()
            print("ret:%s" % ret)
            if ret == QMessageBox.Save:
                print("save")
                self.save()
                self.haseSave = True
            elif ret == QMessageBox.Cancel:
                print("cancel")
                self.haseSave = False
            elif ret == QMessageBox.Discard:
                return False

        return not self.haseSave

    def save(self):
        if not self.haseSave:
            print("satrt save data")
            if not path.exists(self.filePath):
                msgBox = QMessageBox()
                msgBox.setText("%s-文档不存在" % self.fileName)
                msgBox.setInformativeText("请检查是否文件已被删除或转移至其他目录")
                msgBox.setStandardButtons(QMessageBox.Close)
                msgBox.setDefaultButton(QMessageBox.Close)
            else:
                self.startSave()

    def startSave(self):
        updateFile(self.filePath, self.leftEdit.toPlainText()).pipe(
            ops.subscribe_on(scheduler.ThreadPoolScheduler())
        ).subscribe(on_completed=lambda: self.handlerSaveResult())

    def handlerSaveResult(self):
        self.haseSave = True
        self.setFileLastModifyTime()

    def loadData(self, filePath):
        self.filePath = filePath
        self.fileName = path.basename(self.filePath)
        with open(self.filePath, mode='r') as f:
            self.leftEdit.setPlainText("".join(f.readlines()))
        self.setFileLastModifyTime()
        self.haseSave = True

    def setFileLastModifyTime(self):
        if path.exists(self.filePath):
            self.lastModifyTime = stat(self.filePath).st_mtime

    def checkFileChange(self) -> bool:
        currentModifyTime = stat(self.filePath).st_mtime
        if currentModifyTime != self.lastModifyTime:
            print("文件有改动")
            return True
        else:
            return False

    def __del__(self):
        print("EditWidget __del__")

    def setPlainText(self, text: str = ""):
        self.leftEdit.setPlainText(text)

    def getDocument(self) -> QTextDocument:
        return self.leftEdit.document()

    def leftEditTextChange(self):
        self.haseSave = False
        if self.rightPreView:
            self.rightPreView.setHtml(self.markdown.parse(self.leftEdit.toPlainText()))
            self.rightPreView.moveCursor(QTextCursor.End)

    def foreRefreshPreViewInfo(self):
        if self.rightPreView:
            self.rightPreView.setHtml(self.markdown.parse(self.leftEdit.toPlainText()))

    def enterEvent(self, event: PySide2.QtCore.QEvent):
        self.trySave()
