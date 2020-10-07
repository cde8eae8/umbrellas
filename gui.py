from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading
import importlib
import os.path


#TODO: disable multi choice
#TODO: disable descriptions editing
#TODO: add run button
#TODO: if none selected

class ModuleInfo:
    def __init__(self, module):
        self.module = module

    def info(self, name, description, args):
        self.name = name
        self.description = description
        self.args = args

    def run(self, args):
        self.module.run(args)

class MainWindow(QMainWindow):
    def __init__(self, modules, *args):
        QMainWindow.__init__(self, *args)
        self.modules = []
        for m in modules:
            print(self.modules)
            module = importlib.import_module(f'modules.{m}')
            minfo = ModuleInfo(module)
            module.register(minfo)
            self.modules.append(minfo)
            print(minfo.name, minfo.args)
        widget = QWidget()
        layout = QHBoxLayout()
        descrLayout = QVBoxLayout()
        table = QTableWidget()
        table.setColumnCount(1)
        table.setRowCount(len(self.modules))

        table.setEditTriggers(QAbstractItemView.NoEditTriggers);
        table.horizontalHeader().setStretchLastSection(True);
        table.horizontalHeader().hide()
        table.verticalHeader().hide()
        for i, m in enumerate(self.modules):
            table.setItem(i, 0, QTableWidgetItem(m.name))
        self.description = QTextEdit()
        self.description.setReadOnly(True)
        self.runButton = QPushButton('Выбрать')
        descrLayout.addWidget(table)
        descrLayout.addWidget(self.runButton)
        layout.addLayout(descrLayout)
        layout.addWidget(self.description)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.selected = -1
        table.cellClicked.connect(lambda x, y: self._cellActivated(x, y))
        self.runButton.clicked.connect(lambda: self._runScript())

    def start(self):
        self.show()

    def _cellActivated(self, row, column):
        self.description.setText(self.modules[row].description)
        self.selected = row
    
    def _runScript(self):
        self.runButton.setEnabled(False)
        if self.selected != -1:
            self.modules[self.selected].run([])
        self.runButton.setEnabled(True)

class Gui(QMainWindow):
    def __init__(self, callback, widget_types, *args):
        QMainWindow.__init__(self, *args)
        self.callback = callback
        scroll = QScrollArea()
        widget = QWidget()
        layout = QVBoxLayout()

        #window.showMaximized()
        if (len(set(w[0] for w in widget_types)) != len(widget_types)):
            raise Exception('duplicated keys in gui description')

        self.widgets = [Widget(descr, t(), *args) for name, t, descr, *args in widget_types]
        for w in self.widgets:
            layout.addWidget(w)
        self.widgets = {name:w for (name, *oth), w in zip(widget_types, self.widgets)}
        print(self.widgets)
        widget.setLayout(layout)

        submitLayout = QHBoxLayout()
        self.submitButton = QPushButton('Начать')
        submitLayout.addWidget(self.submitButton)
        layout.addLayout(submitLayout)
        self.submitButton.clicked.connect(lambda: self._submit())

        widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        #scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        #scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #scroll.setWidgetResizable(True)
        #scroll.setWidget(widget)
        #window.setCentralWidget(scroll)
        #scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(widget)

    def _submit(self):
        data = {}
        for key, w in self.widgets.items():
            if w.hasData():
                data.update({key:w.data()})
            else:
                w.markRed()
        if (len(data) == len(self.widgets)):
            self.submitButton.setText('Working...')
            self.submitButton.setEnabled(False)
            thread = threading.Thread(target=self.run, args=(data,))
            thread.start()
            #pass

    def finished(self):
        self.submitButton.setText('Начать')
        self.submitButton.setEnabled(True)

    def run(self, data):
        try:
            self.callback(data)
        finally:
            self.finished()





# submit button
# mark empty cells red
# check before execution empty cells
# add file filters
# add tables preview
# types:
#   int, float, path:file, path:dir, string
#   for files: inpath and outpath
#   default arguments

class Description:
    def __init__(self, key, type, user_description):
        self.key = key
        self.type = type
        self.user_description = user_description

def startGui(callback, description):
    gui = Gui(callback, description)
    gui.show()


class Widget(QWidget):
    def __init__(self, name, impl, *args, **kwargs):
        super(Widget, self).__init__(*args, **kwargs)
        self._name = name
        self.impl = impl

        layout2 = QVBoxLayout()
        label = QLabel(name)
        layout2.addWidget(label)
        layout2.addWidget(impl)

        self.setLayout(layout2)

    def hasData(self):
        return self.data() != ''

    def data(self):
        return self.impl.data()

    def name(self):
        return self._name

    def markRed(self):
        self.impl.markRed()


class PathWidget(QWidget):
    def __init__(self, buttonText, *args, **kwargs):
        super(PathWidget, self).__init__(*args, **kwargs)
        layout = QHBoxLayout()
        self.fileLineEdit = QLineEdit()
        layout.addWidget(self.fileLineEdit)
        self.fileLineEdit.setMinimumSize(500, 10)

        self.open = QPushButton(buttonText)
        self.open.clicked.connect(lambda: self._buttonClicked())
        layout.addWidget(self.open)

        self.setLayout(layout)

    def _buttonClicked(self):
        self.fileLineEdit.setText(self.buttonClickedImpl())

    def markRed(self):
        palette = self.fileLineEdit.palette();
        palette.setColor(QPalette.Base, Qt.red);
        self.fileLineEdit.setPalette(palette);

    def data(self):
        return self.fileLineEdit.text()

class InPathWidget(PathWidget):
    def __init__(self, *args, **kwargs):
        super(InPathWidget, self).__init__('Выбрать...', *args, **kwargs)

    def buttonClickedImpl(self):
        f, _ = QFileDialog.getOpenFileName()
        return f

class OutPathWidget(PathWidget):
    def __init__(self, *args, **kwargs):
        super(OutPathWidget, self).__init__('Выбрать...', *args, **kwargs)

    def buttonClickedImpl(self):
        f, _ = QFileDialog.getSaveFileName()
        return f

