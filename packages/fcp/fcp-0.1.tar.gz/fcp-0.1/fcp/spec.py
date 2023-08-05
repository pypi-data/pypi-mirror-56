from enum import Enum
from dataclasses import dataclass, field
from typing import *

from pprint import pprint

def make_dict():
    return {}


@dataclass
class Log():
    id: int = -1
    name: str = ""
    n_args: int = 3
    comment: str = ""
    string: str = ""

    def compile(self):
        return self.__dict__ 

    def decompile(self, d):
        self.__dict__.update(d)

    def get_id(self):
        return self.id
    def get_name(self):
        return self.name
    def get_n_args(self):
        return self.n_args
    def get_comment(self):
        return self.comment
    def get_string(self):
        return self.string

    def set_id (self, id):
        self.id  = int(id) 
    def set_name(self, name):
        self.name = name
    def set_n_args(self, n_args):
        self.n_args = int(n_args)
    def set_comment(self, comment):
        self.comment = comment
    def set_string(self, string):
        self.string = string

    def __hash__(self):
        return hash(self.name+str(self.id))


class Spec():
    def __init__(self):
        self.devices = {}
        self.common = Common()
        self.logs = {}

    def devices(self):
        return self.devices

    def add_device(self, device):
        if device == None:
            return False

        if device.name in self.devices.keys():
            return False

        self.devices[device.name] = device

        return True

    def add_log(self, log):
        if log == None:
            return False

        if log.name in self.logs.keys():
            return False

        self.logs[log.name] = log

        return True

    def get_device(self, id):
        return self.devices.get(id)

    def rm_device(self, id):
        if self.get_device(id) is None:
            return False

        del self.devices[id]
        return True

    def rm_message(self, name, id):
        for dev in self.devices.values():
            for msg in dev.msgs.values():
                if msg.name == name and msg.id == id:
                    dev.rm_message(name)
                    return 

    def rm_signal(self, name, start, length):
        for dev in self.devices.values():
            for msg in dev.msgs.values():
                for sig in msg.signals.values():
                    if sig.name == name and sig.start == start and sig.length == length:
                        msg.rm_signal(name)
                        return


    def compile(self):
        d = {"devices":{}, "logs": {}}

        for k, v in self.devices.items():
            d['devices'][k] = v.compile()
        
        for k, v in self.logs.items():
            d['logs'][k] = v.compile()

        d['common'] = self.common.compile()

        return d

    def decompile(self, d):
        self.devices = {}
        self.logs = {}
        self.common.decompile(d['common'])

        for k, v in d['devices'].items():
            dev = Device()
            dev.decompile(v)
            self.devices[k] = dev

        for k, v in d['logs'].items():
            log = Log()
            log.decompile(v)
            self.logs[k] = log


    def __repr__(self):
        out = "Spec: \n"
        for device in self.devices.values():
            out+=""
            out+= str(device)
            out+="\n"

        return out


@dataclass
class Signal():
    name: str = "default_name"
    start: int = 0
    length: int = 0
    scale: float = 1
    offset: float = 0
    unit: str = ""
    comment: str = ""
    min_value: int = 0
    max_value: int = 0
    type: str = "unsigned"
    byte_order: str = "little_endian"
    mux: str = ""
    mux_count: int = 0
    
    def set_name(self, name):
        self.name = name
    def set_start(self, start):
        self.start = int(start)
    def set_length(self, length):
        self.length = int(length)
    def set_scale(self, scale):
        self.scale = int(scale)
    def set_offset(self, offset):
        self.offset = int(offset)
    def set_unit(self, unit):
        self.unit = unit
    def set_comment(self, comment):
        self.comment = comment
    def set_min_value(self, min_value):
        self.min_value = int(min_value)
    def set_max_value(self, max_value):
        self.max_value = int(max_value)
    def set_type(self, type):
        self.type = type
    def set_byte_order(self, byte_order):
        self.byte_order = byte_order
    def set_mux(self, mux):
        self.mux = mux
    def set_mux_count(self, mux_count):
        self.mux_count = int(mux_count)

    def get_name(self):
        return self.name
    def get_start(self):
        return self.start
    def get_length(self):
        return self.length
    def get_scale(self):
        return self.scale
    def get_offset(self):
        return self.offset
    def get_unit(self):
        return self.unit
    def get_comment(self):
        return self.comment
    def get_min_value(self):
        return self.min_value
    def get_max_value(self):
        return self.max_value
    def get_type(self):
        return self.type
    def get_byte_order(self):
        return self.byte_order
    def get_mux(self):
        return self.mux
    def get_mux_count(self):
        return self.mux_count

    def compile(self):
        return self.__dict__ 

    def decompile(self, d):
        self.__dict__.update(d)

    def __hash__(self):
        return hash(self.name+str(self.start)+str(self.length))


@dataclass
class Message():
    name: str = "default_name"
    id: int = 0
    dlc: int = 8
    signals: Dict[str, Signal] = field(default_factory=make_dict)
    frequency: int = 0

    def set_name(self, name):
        self.name = name
    def set_id(self, id):
        self.id = int(id)
    def set_dlc(self, dlc):
        self.dlc = int(dlc)
    def set_frequency(self, frequency):
        self.frequency = int(frequency)

    def get_name(self):
        return self.name
    def get_id(self):
        return self.id
    def get_dlc(self):
        return self.dlc
    def get_frequency(self):
        return self.frequency

    def compile(self):
        msgs = {}
        for k, v in self.signals.items():
            msgs[k] = v.compile()
        
        att = self.__dict__
        att['signals'] = msgs
        return att

    def decompile(self, d):
        self.__dict__.update(d)
        sigs = {}
        for key, value in self.signals.items():
            sig = Signal()
            sig.decompile(value)
            sigs[key] = sig

        self.signals = sigs

    def add_signal(self, signal):
        if signal == None:
            return False

        if signal.name in self.signals.keys():
            self.signals[signal.name].mux_count += 1
            return True

        self.signals[signal.name] = signal

        return True

    def get_signal(self, name):
        return self.signals.get(name)

    def rm_signal(self, name):
        if self.get_signal(name) is None:
            return False

        del self.signals[name]
        return True

    def __hash__(self):
        return hash(self.name+str(self.id))

@dataclass
class Argument():
    name: str = ""
    id: int = 0
    comment: str = ""

    def get_name(self):
        return self.name
    def get_comment(self):
        return self.comment
    def get_id(self):
        return self.id

    def set_name(self, name):
        self.name = name
    def set_comment(self, comment):
        self.comment = comment
    def set_id(self, id):
        self.id = id

    def compile(self):
        return self.__dict__

    def decompile(self, d):
        self.__dict__.update(d)

@dataclass
class Command():
    name: str = ""
    n_args: int = 3
    comment: str = ""
    id: int = 0
    args: Dict[str, Argument] = field(default_factory=make_dict)
    rets: Dict[str, Argument] = field(default_factory=make_dict)
    
    def get_name(self):
        return self.name
    def get_n_args(self):
        return self.n_args
    def get_comment(self):
        return self.comment
    def get_id(self):
        return self.id

    def set_name(self, name):
        self.name = name
    def set_n_args(self, n_args):
        self.n_args = n_args
    def set_comment(self, comment):
        self.comment = comment
    def set_id(self, id):
        self.id = id

    def compile(self):
        args = {}
        rets = {}
        for k, v in self.args.items():
            args[k] = v.compile()
        
        for k,v in self.rets.items():
            rets[k] = v.compile()

        
        att = self.__dict__
        att['args'] = args
        att['rets'] = rets

        return att
    
    def add_arg(self, arg):
        self.args[arg.name] = arg

    def add_ret(self, ret):
        self.rets[ret.name] = ret

    def decompile(self, d):
        self.__dict__.update(d)
        args = {}
        rets = {}
        
        for k, v in self.args.items():
            arg = Argument()
            arg.decompile(v)
            args[k] = arg

        self.args = args

        for k, v in self.rets.items():
            ret = Argument()
            ret.decompile(v)
            rets[k] = ret
        
        self.rets = rets


@dataclass 
class Config():
    name: str = ""
    id : int = 0
    comment: str = ""
        
    def set_name(self, name):
        self.name = name
    def set_id (self, id ):
        self.id  = id 
    def set_comment(self, comment):
        self.comment = comment

    def get_name(self):
        return self.name
    def get_id (self):
        return self.id 
    def get_comment(self):
        return self.comment

    def compile(self):
        return self.__dict__ 

    def decompile(self, d):
        self.__dict__.update(d)

@dataclass
class Device():
    name: str = "default_name"
    id: int = 0
    msgs: Dict[str, Message] = field(default_factory=make_dict)
    cmds: Dict[str, Command] = field(default_factory=make_dict)
    cfgs: Dict[str, Config] = field(default_factory=make_dict)
    
    def set_name(self, name):
        self.name = name
    def set_id(self, id):
        self.id = int(id)

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def add_cmd(self, cmd):
        self.cmds[cmd.name] = cmd
    
    def add_cfg(self, cfg):
        self.cfgs[cfg.name] = cfg

    def compile(self):
        msgs = {}
        cmds = {}
        cfgs = {}

        for k, v in self.msgs.items():
            msgs[k] = v.compile()
        
        for k,v in self.cmds.items():
            cmds[k] = v.compile()

        for k,v in self.cfgs.items():
            cfgs[k] = v.compile()

        att = self.__dict__
        att['msgs'] = msgs
        att['cmds'] = cmds
        att['cfgs'] = cfgs

        return att

    def decompile(self, d):
        self.__dict__.update(d)
        msgs = {}
        cmds = {}
        cfgs = {}
        
        for k, v in self.msgs.items():
            msg = Message()
            msg.decompile(v)
            msgs[k] = msg

        self.msgs = msgs

        for k, v in self.cmds.items():
            cmd = Command()
            cmd.decompile(v)
            cmds[k] = cmd

        self.cmds = cmds

        for k, v in self.cfgs.items():
            cfg = Config()
            cfg.decompile(v)
            cfgs[k] = cfg
        
        self.cfgs = cfgs


    def add_msg(self, msg):
        if msg == None:
            return False

        if msg.name in self.msgs.keys():
            return False
        
        self.msgs[msg.name] = msg

        return True

    def get_msg(self, id):
        return self.msgs.get(id)

    def rm_msg(self, name):
        if self.get_msg(name) is None:
            return False

        del self.msgs[name]
        return True
    
    def get_cmd(self, name):
        return self.cmds.get(name)

    def rm_cmd(self, name):
        if self.get_cmd(name) is None:
            return False

        del self.cmds[name]
        return True

    def get_cfg(self, name):
        return self.cfgs.get(name)

    def rm_cfg(self, name):
        if self.get_cfg(name) is None:
            return False

        del self.cfgs[name]
        return True

    def __hash__(self):
        return hash(self.name+str(self.id))

@dataclass
class Common():
    name: str = "common"
    id: int = 0
    msgs: Dict[str, Message] = field(default_factory=make_dict)
    
    def add_msg(self ,msg):
        if msg == None:
            return False
        
        if msg.name in self.msgs.keys():
            return False

        self.msgs[msg.name] = msg
        return True

    def compile(self):
        d = {}
        for name, msg in self.msgs.items():
            d[name] = msg.compile()
        
        att = self.__dict__
        att['msgs'] = d
        return att

    def decompile(self, d):
        self.__dict__.update(d)
        d = {}
        for key, value in self.msgs.items():
            msg = Message()
            msg.decompile(value)
            d[key] = msg

        self.msgs = d

def make_sid(dev_id, msg_id):
    return msg_id * 32 + dev_id

def decompose_id(sid):
    return sid & 0x1F, (sid >> 5) & 0x3F
