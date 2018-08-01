# 1.treeView加载本地文件目录

```python
class CMyFileSystemModel(QtWidgets.QFileSystemModel):
    def __init__(self, parent=None):
        super(CMyFileSystemModel, self).__init__(parent)
        # 设置显示那些文件
        self.setFilter(QtCore.QDir.Files | QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot)

class CXXX(QtWidgets.QMainWindow, mainwidget_ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(CXXX, self).__init__(parent)
        self.treeView = CMyTreeView(self)
        
    def _LoadDirTree(self):
        oSystemModel = CMyFileSystemModel(self)
        index = oSystemModel.setRootPath(self.m_OpenDir)	# 设置根目录，并获取索引id
        self.treeView.SetFileSystemModel(oSystemModel)		# 设置文件系统模型
        self.treeView.header().hide()
        self.treeView.setModel(oSystemModel)			   # 传入模型对象，后续获取文件名用到
        self.treeView.setRootIndex(index)				   # 设置索引id（没有就直接显示系统跟目录）
```



# 2.treeView实现拖拽功能

```python
class CMyTreeView(QtWidgets.QTreeView):

    def __init__(self, parent=None):
        super(CMyTreeView, self).__init__(parent)
        self.m_DragPosition = None	# 记录拖拽起始点

    def SetFileSystemModel(self, obj):
        self.m_FileSystemModel = weakref.ref(obj)	# 保存文件系统模型对象

    def mousePressEvent(self, event):
        """鼠标点击时调用"""
        super(CMyTreeView, self).mousePressEvent(event)
        if(event.button() == QtCore.Qt.LeftButton):
            self.m_DragPosition = event.pos()
            index = self.indexAt(self.m_DragPosition)	# 从拖拽点获取拖拽文件的索引
            self.m_DragFile = self.m_FileSystemModel().filePath(index) # 根据索引获取对应的文件名

    def mouseMoveEvent(self, event):
        """鼠标移动时调用"""
        super(CMyTreeView, self).mousePressEvent(event)
        if(not (event.button and QtCore.Qt.LeftButton)):
            return
        if((event.pos() - self.m_DragPosition).manhattanLength() < QtWidgets.QApplication.startDragDistance()):	# 判断是否大于拖拽距离
            return

        drag = QtGui.QDrag(self)
        oMimeData = QtCore.QMimeData()
        oMimeData.setText(self.m_DragFile)	# 将文件名设置到MimeData对象里面，后续接受用到
        drag.setMimeData(oMimeData)

        pixMap = QtGui.QPixmap(120, 18)	# 拖拽时显示图标
        painter = QtGui.QPainter(pixMap)
        painter.drawText(QtCore.QRectF(0, 0, 120, 18), "drag", QtGui.QTextOption(QtCore.Qt.AlignVCenter))
        drag.setPixmap(pixMap)
        result = drag.exec(QtCore.Qt.MoveAction)
        del painter
        del pixMap
        del drag
```



# 3.接受拖拽事件

```python
class CCodeEdit(QtWidgets.QPlainTextEdit):
     def dragEnterEvent(self, event):
        """拖动操作进入本窗口"""
        # 注意以下两个一定需要有，少一个测试时dropEvent都没被调用
        event.accept()	
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        # dragMoveEvent也一定需要有
        event.accept()
        event.acceptProposedAction()

    def dropEvent(self, event):
        """放开了鼠标完成drop操作"""
        event.acceptProposedAction()
        self.m_CurFile = str(event.mimeData().text())
        if(self.m_CurFile.startswith("file:///")):
            self.m_CurFile = self.m_CurFile[8:]
        if(not os.path.exists(self.m_CurFile)):
            self.m_CurFile = ""
            return
```

