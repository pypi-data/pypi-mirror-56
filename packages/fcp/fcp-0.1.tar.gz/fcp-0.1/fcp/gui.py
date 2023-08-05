# This Python file uses the following encoding: utf-8
import sys
import json

from PySide2.QtWidgets import *

from PySide2.QtGui import QKeySequence
from PySide2.QtCore import Qt

from .spec import *
from .validator import validate

from .gui_lib.mainwindow import Ui_MainWindow
from .gui_lib.devicewidget import Ui_DeviceWidget
from .gui_lib.devicedetails import Ui_DeviceDetails
from .gui_lib.messagewidget import Ui_MessageWidget
from .gui_lib.messagedetails import Ui_MessageDetails
from .gui_lib.signalwidget import Ui_SignalWidget
from .gui_lib.signaldetails import Ui_SignalDetails
from .gui_lib.logwidget import Ui_LogWidget
from .gui_lib.logdetails import Ui_LogDetails
from .gui_lib.cfgwidget import Ui_CfgWidget
from .gui_lib.cfgdetails import Ui_CfgDetails
from .gui_lib.cmdwidget import Ui_CmdWidget
from .gui_lib.cmddetails import Ui_CmdDetails
from .gui_lib.cmdarg import Ui_CmdArg


class SignalDetails(QWidget):
    def __init__(self, gui, signal):
        QWidget.__init__(self)
        self.ui = Ui_SignalDetails()
        self.ui.setupUi(self)

        self.signal = signal
        self.gui = gui

        self.atts = [ 
                ( self.ui.nameEdit, self.signal.get_name,
                    self.signal.set_name),
                ( self.ui.startEdit, self.signal.get_start,
                    self.signal.set_start),
                ( self.ui.lengthEdit, self.signal.get_length,
                    self.signal.set_length),
                ( self.ui.muxEdit, self.signal.get_mux, 
                    self.signal.set_mux),
                ( self.ui.muxCountEdit, self.signal.get_mux_count,
                    self.signal.set_mux_count),
                ( self.ui.typeEdit, self.signal.get_type,
                    self.signal.set_type),
                ( self.ui.commentEdit, self.signal.get_comment,
                    self.signal.set_comment),
                ( self.ui.minValueEdit, self.signal.get_min_value,
                    self.signal.set_min_value),
                ( self.ui.maxValueEdit, self.signal.get_max_value,
                    self.signal.set_max_value),
                ( self.ui.byteOrderEdit, self.signal.get_byte_order,
                    self.signal.set_byte_order),
                ( self.ui.scaleEdit, self.signal.get_scale,
                    self.signal.set_scale),
                ( self.ui.offsetEdit, self.signal.get_offset,
                    self.signal.set_offset)
            ]
        
        for att, _, set_f in self.atts:
            att.textChanged.connect(set_f)
            att.textChanged.connect(gui.reload)
        
        self.ui.signalDeleteButton.clicked.connect(self.delete)

        self.reload()
        self.setVisible(False)
    
    def delete(self):
        return

    def save(self):
        for att, get_f, set_f in self.atts:
            set_f(att.text())

        self.gui.reload()

    def reload(self):
        for att, get_f, set_f in self.atts:
            att.setText(str(get_f()))


    def raise_widget(self, checked):
        self.setVisible(checked)


class SignalWidget(QWidget):
    def __init__(self, gui, signal):
        QWidget.__init__(self)
        self.ui = Ui_SignalWidget()
        self.ui.setupUi(self)
        
        self.signal = signal
        self.gui = gui

        self.atts = [ 
                ( self.ui.name, self.signal.get_name,
                    self.signal.set_name),
                ( self.ui.start, self.signal.get_start,
                    self.signal.set_start),
                ( self.ui.length, self.signal.get_length,
                    self.signal.set_length)
            ]

        self.reload()

        self.details = {}
        self.children = []

    def reload(self):
        for att, get_f, set_f in self.atts:
            att.setText(str(get_f()))

    def open_details(self, checked):
        if self.signal.name in self.details.keys():
            sig_details = self.details[self.signal.name]
        else:
            sig_details = SignalDetails(self.gui, self.signal)
            self.gui.ui.signalDetailsLayout.addWidget(sig_details)
            self.children.append(sig_details)
            self.details[self.signal.name] = sig_details

        sig_details.setVisible(checked)

class MessageDetails(QWidget):
    def __init__(self, gui, message):
        QWidget.__init__(self)
        self.ui = Ui_MessageDetails()
        self.ui.setupUi(self)
        
        self.message = message

        self.atts = [
                (self.ui.nameEdit, message.get_name, message.set_name),
                (self.ui.idEdit, message.get_id,message.set_id),
                (self.ui.dlcEdit, message.get_dlc, message.set_dlc),
                (self.ui.frequencyEdit, message.get_frequency, message.set_frequency)
            ]
        
        self.reload()

        self.gui = gui

        self.children = []

        self.setVisible(False)

        for ui, _, set_f in self.atts:
            ui.textChanged.connect(set_f)
            ui.textChanged.connect(gui.reload)


        for sig in self.message.signals.values():
            sig = SignalWidget(self.gui, sig)
            self.ui.verticalLayout_2.addWidget(sig)
            sig.ui.signalDetailsButton.clicked.connect(sig.open_details)
            self.children.append(sig)
        
        self.ui.deleteMessageButton.clicked.connect(self.delete)

    def delete(self):
        return 

    def save(self):
        for att, _, set_f in self.atts:
            set_f(att.text())

        self.gui.reload()

    def reload(self): 
        for att, get_f, _ in self.atts:
            att.setText(str(get_f()))

    def raise_widget(self, checked):
        self.setVisible(checked)

class MessageWidget(QWidget):
    def __init__(self, gui, message):
        QWidget.__init__(self)
        self.ui = Ui_MessageWidget()
        self.ui.setupUi(self)
        
        self.message = message
        self.gui = gui

        self.atts = [ 
            (self.ui.id, message.get_id, message.set_id), 
            (self.ui.name, message.get_name, message.set_name),
            (self.ui.dlc, message.get_dlc, message.set_dlc), 
            (self.ui.frequency, message.get_frequency, message.set_frequency)
        ]
        self.children = []
        self.reload()
        self.details = {}

    def reload(self):
        for att, get_f, _ in self.atts:
            att.setText(str(get_f()))

    def save(self):
        for att, _, set_f in self.atts:
            set_f(att.text())

    def open_details(self, checked):
        if self.message.name in self.details.keys():
            msg_details = self.details[self.message.name]
        else:
            msg_details = MessageDetails(self.gui, self.message)
            self.gui.ui.messageDetailsLayout.addWidget(msg_details)
            self.children.append(msg_details)
            self.details[self.message.name] = msg_details

        msg_details.setVisible(checked)

class ArgDetails(QWidget):
    def __init__(self, gui, arg):
        QWidget.__init__(self)
        self.ui = Ui_CmdArg()
        self.ui.setupUi(self)

        self.atts = [
                (self.ui.nameEdit, arg.get_name, arg.set_name),
                (self.ui.commentEdit, arg.get_comment, arg.set_comment),
                (self.ui.idEdit, arg.get_id, arg.set_id)
            ]

        self.reload()

        self.ui.deleteArgButton.clicked.connect(self.delete)

    def delete(self):
        return

    def save(self):
        for att, get_f, set_f in self.atts:
            set_f(att.text())

        self.gui.reload()

    def reload(self):
        for att, get_f, set_f in self.atts:
            att.setText(str(get_f()))

class CmdDetails(QWidget):
    def __init__(self, gui, cmd):
        QWidget.__init__(self)
        self.ui = Ui_CmdDetails()
        self.ui.setupUi(self)
        
        self.gui = gui

        self.children = []

        self.atts = [
                (self.ui.nameEdit, cmd.get_name, cmd.set_name),
                (self.ui.n_argsEdit, cmd.get_n_args, cmd.set_n_args),
                (self.ui.commentEdit, cmd.get_comment, cmd.set_comment),
                (self.ui.idEdit, cmd.get_id, cmd.set_id)
            ]

        self.reload()
        
        self.ui.addArgButton.clicked.connect(self.add_arg)
        for arg in cmd.args.values():
            self.add_arg(arg)

        self.ui.deleteCmdButton.clicked.connect(self.delete)

    def delete(self):
        return

    def add_arg(self, arg=None):
        if not arg:
            arg = Argument()

        arg_widget = ArgDetails(self.gui, arg)
        self.children.append(arg_widget)
        self.ui.CmdArgContents.addWidget(arg_widget)

    def save(self):
        for att, get_f, set_f in self.atts:
            set_f(att.text())

        self.gui.reload()

    def reload(self):
        for att, get_f, set_f in self.atts:
            att.setText(str(get_f()))


class CmdWidget(QWidget):
    def __init__(self, gui, cmds):
        QWidget.__init__(self)
        self.ui = Ui_CmdWidget()
        self.ui.setupUi(self)

        self.setVisible(False)

        self.cmds = cmds

        self.gui = gui

        self.children = []

        self.ui.addCmdButton.clicked.connect(self.add_cmd)
        for cmd in self.cmds.values():
            self.add_cmd(cmd)

    def add_cmd(self, cmd=None):
        if not cmd:
            cmd = Command()

        cmd_details = CmdDetails(self.gui, cmd) 
        self.ui.CmdScrollContents.addWidget(cmd_details)
        self.children.append(cmd_details)
        

class CfgDetails(QWidget):
    def __init__(self, gui, cfg):
        QWidget.__init__(self)
        self.ui = Ui_CfgDetails()
        self.ui.setupUi(self)

        self.atts = [
                (self.ui.nameEdit, cfg.get_name, cfg.set_name),
                (self.ui.idEdit, cfg.get_id, cfg.set_id),
                (self.ui.commentEdit, cfg.get_comment, cfg.set_comment)
            ]

        self.reload()

        self.ui.deleteCfgButton.clicked.connect(self.delete)
    
    def delete(self):
        return

    def save(self):
        for att, get_f, set_f in self.atts:
            set_f(att.text())

        self.gui.reload()

    def reload(self):
        for att, get_f, set_f in self.atts:
            att.setText(str(get_f()))

class CfgWidget(QWidget):
    def __init__(self, gui, cfgs):
        QWidget.__init__(self)
        self.ui = Ui_CfgWidget()
        self.ui.setupUi(self)
        
        self.setVisible(False)

        self.cfgs = cfgs

        self.gui = gui
        

        self.children = []

        self.ui.addCfgButton.clicked.connect(self.add_cfg)

        for cfg in self.cfgs.values():
            self.add_cfg(cfg)

    def add_cfg(self, cfg=None):
        if not cfg:
            cfg = Config()

        cfg_details = CfgDetails(self.gui, cfg) 
        self.ui.CfgScrollContents.addWidget(cfg_details)
        self.children.append(cfg_details)



class DeviceDetails(QWidget):
    def __init__(self, gui, device):
        QWidget.__init__(self)
        self.ui = Ui_DeviceDetails()
        self.ui.setupUi(self)
        
        self.device = device

        self.atts = [
                (self.ui.idEdit, device.get_id, device.set_id),
                (self.ui.nameEdit, device.get_name, device.set_name)
            ]


        self.gui = gui

        self.children = []

        self.setVisible(False)
        
        self.cfg_widget = CfgWidget(self.gui, self.device.cfgs)
        self.ui.cfgDetails.addWidget(self.cfg_widget)


        self.cmd_widget = CmdWidget(self.gui, self.device.cmds)
        self.ui.cmdDetails.addWidget(self.cmd_widget)

        self.ui.addButton.clicked.connect(self.add_message)
        self.ui.cfgsButton.clicked.connect(self.add_cfg)
        self.ui.cmdsButton.clicked.connect(self.add_cmd)

        for att, _, set_f in self.atts:
            att.textChanged.connect(set_f)
            att.textChanged.connect(gui.reload)

        for msg in self.device.msgs.values():
            m = MessageWidget(self.gui, msg)
            self.ui.verticalLayout.addWidget(m)
            m.ui.messageDetailsButton.clicked.connect(m.open_details)
            self.children.append(m)

        self.reload()

        self.ui.deleteDeviceButton.clicked.connect(self.delete)

    def delete(self):
        return 

    def save(self):
        for att, get_f, set_f in self.atts:
            set_f(att.text())

        self.gui.reload()

    def reload(self):
        for att, get_f, set_f in self.atts:
            att.setText(str(get_f()))

    def add_cfg(self, clicked):
        self.cfg_widget.setVisible(clicked)
        return


    def add_cmd(self, clicked):
        self.cmd_widget.setVisible(clicked)
        return

    def add_message(self, clicked):
        return

    #def raise_widget(self, checked):
    #    self.setVisible(checked)

class DeviceWidget(QWidget):
    def __init__(self, gui, device):
        QWidget.__init__(self)
        self.ui = Ui_DeviceWidget()
        self.ui.setupUi(self)
        
        self.device = device
        self.gui = gui

        self.atts = [
            (self.ui.id, device.get_id, device.set_id),
            (self.ui.name, device.get_name, device.set_name)
        ]

        self.children = []

        self.reload()

        self.details = {}

    def reload(self):
        for att, get_f, _ in self.atts:
            att.setText(str(get_f()))

    def save(self):
        for att, _, set_f in self.atts:
            set_f(att.text())

    def open_details(self, checked):
        if self.device.name in self.details.keys():
            dev_details = self.details[self.device.name]
        else:
            dev_details = DeviceDetails(self.gui, self.device)
            self.gui.ui.deviceDetailsLayout.addWidget(dev_details)
            self.children.append(dev_details)
            self.details[self.device.name] = dev_details

        dev_details.setVisible(checked)

class LogDetails(QWidget):
    def __init__(self, gui, log):
        QWidget.__init__(self)
        self.ui = Ui_LogDetails()
        self.ui.setupUi(self)
        
        self.log = log

        self.atts = [
                (self.ui.idEdit, log.get_id, log.set_id),
                (self.ui.nameEdit, log.get_name, log.set_name),
                (self.ui.n_argsEdit, log.get_n_args, log.set_n_args),
                (self.ui.commentEdit, log.get_comment, log.set_comment),
                (self.ui.stringEdit, log.get_string, log.set_string)
            ]


        self.gui = gui

        self.children = []

        self.setVisible(True)

        for att, _, set_f in self.atts:
            att.textChanged.connect(set_f)
            att.textChanged.connect(gui.reload)

        self.reload()

        self.ui.logDeleteButton.clicked.connect(self.delete)

    def delete(self):
        return


    def save(self):
        for att, get_f, set_f in self.atts:
            set_f(att.text())

        self.gui.reload()

    def reload(self):
        for att, get_f, set_f in self.atts:
            att.setText(str(get_f()))


class LogWidget(QWidget):
    def __init__(self, gui, logs):
        self.Window = True
        QWidget.__init__(self)
        self.ui = Ui_LogWidget()
        self.ui.setupUi(self)
        
        self.logs = logs
        self.gui = gui
        
        self.atts = {}

        self.children = []

        self.reload()

        self.details = {}
        
        self.ui.addLogButton.clicked.connect(self.add_log)
        for log in logs.values():
            self.add_log(log)


    def reload(self):
        return

    def save(self):
        return

    def add_log(self, log=None):
        if log == None or log == False:
            log = Log()

        log_widget = LogDetails(self, log)
        self.ui.logContents.addWidget(log_widget)
        self.children.append(log_widget)


class Gui(QMainWindow):
    def __init__(self, logger):
        self.logger = logger
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
         
        self.ui.actionOpen.triggered.connect(self.open_json)
        self.ui.actionSave.triggered.connect(self.save_json)
        self.ui.actionValidate.triggered.connect(self.validate)

        self.spec = Spec()
        self.children = []

        shortcutSave = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_S), self)
        shortcutSave.setContext(Qt.ApplicationShortcut)
        shortcutSave.activated.connect(self.save_json)

        shortcutOpen = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_O), self)
        shortcutOpen.setContext(Qt.ApplicationShortcut)
        shortcutOpen.activated.connect(self.open_json)

        self.ui.addButton.clicked.connect(self.add_device)
        self.ui.logsButton.clicked.connect(self.open_log_widget)
        
        self.log_widget = None

    def open_log_widget(self, checked):
        if self.log_widget is None:
            print("log not openned")
            return

        self.log_widget.setVisible(checked)

    def validate(self):
        msg = QMessageBox(self)
        msg.setStandardButtons(QMessageBox.Ok)
        r, m = validate(self.logger, '{}', spec=self.spec)
        if r:
            msg.setIcon(QMessageBox.Information)
            msg.setText("Spec passed")
        else:
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Failed:" + m) 

        msg.show()


    def add_device(self, device=None):
        if device == None or device == False:
            device = Device()

        dev_widget = DeviceWidget(self, device)
        self.ui.verticalLayout.addWidget(dev_widget)
        dev_widget.ui.deviceDetailsButton.clicked.connect(dev_widget.open_details)
        self.children.append(dev_widget)


    def open_json(self):
        filename = QFileDialog.getOpenFileName(self, self.tr("Open JSON"), self.tr("JSON (*.json)"))
        self.load_json(filename[0])

        self.log_widget = LogWidget(self.ui, self.spec.logs)
        self.log_widget.setVisible(False)
        self.ui.logDetailsLayout.addWidget(self.log_widget)

    def save_json(self):
        filename = QFileDialog.getSaveFileName(self, self.tr("Open JSON"), self.tr("JSON (*.json)"))

        with open(filename[0], 'w') as f:
            j = self.spec.compile()
            f.write(json.dumps(j, indent=4))

    def load_json(self, filename):
        with open(filename) as f:
            j = json.loads(f.read())

        self.spec.decompile(j)
        
        for device in sorted(self.spec.devices.values(), key=lambda x: x.id):
            self.add_device(device)

    def reload(self):
        for dev in self.children:
            for dev_details in dev.children:
                for msg in dev_details.children:
                    for msg_details in msg.children:
                        for sig in msg_details.children:
                            for sig_details in sig.children:
                                sig_details.reload()
                            sig.reload()
                        msg_details.reload()
                    msg.reload()
                dev_details.reload()
            dev.reload()


def gui(logger):
    app = QApplication([])
    window = Gui(logger)
    window.show()
    sys.exit(app.exec_())
