# Copyright (c) 2008 The Board of Trustees of The Leland Stanford Junior University
# Copyright (c) 2011, 2012 Open Networking Foundation
# Copyright (c) 2012, 2013 Big Switch Networks, Inc.
# See the file LICENSE.pyloxi which should have been included in the source distribution

# Automatically generated by LOXI from template module.py
# Do not modify

import struct
import loxi
import const
import bsn_tlv
import meter_band
import instruction
import oxm
import common
import instruction_id
import action
import message
import action_id
import util
import loxi.generic_util

class action(loxi.OFObject):
    subtypes = {}


    def __init__(self, type=None):
        if type != None:
            self.type = type
        else:
            self.type = 0
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append('\x00' * 4)
        length = sum([len(x) for x in packed])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        subtype, = reader.peek('!H', 0)
        subclass = action.subtypes.get(subtype)
        if subclass:
            return subclass.unpack(reader)

        obj = action()
        obj.type = reader.read("!H")[0]
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        reader.skip(4)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        if self.type != other.type: return False
        return True

    def pretty_print(self, q):
        q.text("action {")
        with q.group():
            with q.indent(2):
                q.breakable()
            q.breakable()
        q.text('}')


class experimenter(action):
    subtypes = {}

    type = 65535

    def __init__(self, experimenter=None, data=None):
        if experimenter != None:
            self.experimenter = experimenter
        else:
            self.experimenter = 0
        if data != None:
            self.data = data
        else:
            self.data = ''
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!L", self.experimenter))
        packed.append(self.data)
        length = sum([len(x) for x in packed])
        packed.append(loxi.generic_util.pad_to(8, length))
        length += len(packed[-1])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        subtype, = reader.peek('!L', 4)
        subclass = experimenter.subtypes.get(subtype)
        if subclass:
            return subclass.unpack(reader)

        obj = experimenter()
        _type = reader.read("!H")[0]
        assert(_type == 65535)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        obj.experimenter = reader.read("!L")[0]
        obj.data = str(reader.read_all())
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        if self.experimenter != other.experimenter: return False
        if self.data != other.data: return False
        return True

    def pretty_print(self, q):
        q.text("experimenter {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("data = ");
                q.pp(self.data)
            q.breakable()
        q.text('}')

action.subtypes[65535] = experimenter

class bsn(experimenter):
    subtypes = {}

    type = 65535
    experimenter = 6035143

    def __init__(self, subtype=None):
        if subtype != None:
            self.subtype = subtype
        else:
            self.subtype = 0
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!L", self.experimenter))
        packed.append(struct.pack("!L", self.subtype))
        packed.append('\x00' * 4)
        length = sum([len(x) for x in packed])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        subtype, = reader.peek('!L', 8)
        subclass = bsn.subtypes.get(subtype)
        if subclass:
            return subclass.unpack(reader)

        obj = bsn()
        _type = reader.read("!H")[0]
        assert(_type == 65535)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        _experimenter = reader.read("!L")[0]
        assert(_experimenter == 6035143)
        obj.subtype = reader.read("!L")[0]
        reader.skip(4)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        if self.subtype != other.subtype: return False
        return True

    def pretty_print(self, q):
        q.text("bsn {")
        with q.group():
            with q.indent(2):
                q.breakable()
            q.breakable()
        q.text('}')

experimenter.subtypes[6035143] = bsn

class bsn_checksum(bsn):
    type = 65535
    experimenter = 6035143
    subtype = 4

    def __init__(self, checksum=None):
        if checksum != None:
            self.checksum = checksum
        else:
            self.checksum = 0
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!L", self.experimenter))
        packed.append(struct.pack("!L", self.subtype))
        packed.append(util.pack_checksum_128(self.checksum))
        length = sum([len(x) for x in packed])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = bsn_checksum()
        _type = reader.read("!H")[0]
        assert(_type == 65535)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        _experimenter = reader.read("!L")[0]
        assert(_experimenter == 6035143)
        _subtype = reader.read("!L")[0]
        assert(_subtype == 4)
        obj.checksum = util.unpack_checksum_128(reader)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        if self.checksum != other.checksum: return False
        return True

    def pretty_print(self, q):
        q.text("bsn_checksum {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("checksum = ");
                q.pp(self.checksum)
            q.breakable()
        q.text('}')

bsn.subtypes[4] = bsn_checksum

class bsn_gentable(bsn):
    type = 65535
    experimenter = 6035143
    subtype = 5

    def __init__(self, table_id=None, key=None):
        if table_id != None:
            self.table_id = table_id
        else:
            self.table_id = 0
        if key != None:
            self.key = key
        else:
            self.key = []
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!L", self.experimenter))
        packed.append(struct.pack("!L", self.subtype))
        packed.append(struct.pack("!L", self.table_id))
        packed.append(loxi.generic_util.pack_list(self.key))
        length = sum([len(x) for x in packed])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = bsn_gentable()
        _type = reader.read("!H")[0]
        assert(_type == 65535)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        _experimenter = reader.read("!L")[0]
        assert(_experimenter == 6035143)
        _subtype = reader.read("!L")[0]
        assert(_subtype == 5)
        obj.table_id = reader.read("!L")[0]
        obj.key = loxi.generic_util.unpack_list(reader, bsn_tlv.bsn_tlv.unpack)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        if self.table_id != other.table_id: return False
        if self.key != other.key: return False
        return True

    def pretty_print(self, q):
        q.text("bsn_gentable {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("table_id = ");
                q.text("%#x" % self.table_id)
                q.text(","); q.breakable()
                q.text("key = ");
                q.pp(self.key)
            q.breakable()
        q.text('}')

bsn.subtypes[5] = bsn_gentable

class bsn_mirror(bsn):
    type = 65535
    experimenter = 6035143
    subtype = 1

    def __init__(self, dest_port=None, vlan_tag=None, copy_stage=None):
        if dest_port != None:
            self.dest_port = dest_port
        else:
            self.dest_port = 0
        if vlan_tag != None:
            self.vlan_tag = vlan_tag
        else:
            self.vlan_tag = 0
        if copy_stage != None:
            self.copy_stage = copy_stage
        else:
            self.copy_stage = 0
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!L", self.experimenter))
        packed.append(struct.pack("!L", self.subtype))
        packed.append(struct.pack("!L", self.dest_port))
        packed.append(struct.pack("!L", self.vlan_tag))
        packed.append(struct.pack("!B", self.copy_stage))
        packed.append('\x00' * 3)
        length = sum([len(x) for x in packed])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = bsn_mirror()
        _type = reader.read("!H")[0]
        assert(_type == 65535)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        _experimenter = reader.read("!L")[0]
        assert(_experimenter == 6035143)
        _subtype = reader.read("!L")[0]
        assert(_subtype == 1)
        obj.dest_port = reader.read("!L")[0]
        obj.vlan_tag = reader.read("!L")[0]
        obj.copy_stage = reader.read("!B")[0]
        reader.skip(3)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        if self.dest_port != other.dest_port: return False
        if self.vlan_tag != other.vlan_tag: return False
        if self.copy_stage != other.copy_stage: return False
        return True

    def pretty_print(self, q):
        q.text("bsn_mirror {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("dest_port = ");
                q.text("%#x" % self.dest_port)
                q.text(","); q.breakable()
                q.text("vlan_tag = ");
                q.text("%#x" % self.vlan_tag)
                q.text(","); q.breakable()
                q.text("copy_stage = ");
                q.text("%#x" % self.copy_stage)
            q.breakable()
        q.text('}')

bsn.subtypes[1] = bsn_mirror

class bsn_set_tunnel_dst(bsn):
    type = 65535
    experimenter = 6035143
    subtype = 2

    def __init__(self, dst=None):
        if dst != None:
            self.dst = dst
        else:
            self.dst = 0
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!L", self.experimenter))
        packed.append(struct.pack("!L", self.subtype))
        packed.append(struct.pack("!L", self.dst))
        length = sum([len(x) for x in packed])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = bsn_set_tunnel_dst()
        _type = reader.read("!H")[0]
        assert(_type == 65535)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        _experimenter = reader.read("!L")[0]
        assert(_experimenter == 6035143)
        _subtype = reader.read("!L")[0]
        assert(_subtype == 2)
        obj.dst = reader.read("!L")[0]
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        if self.dst != other.dst: return False
        return True

    def pretty_print(self, q):
        q.text("bsn_set_tunnel_dst {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("dst = ");
                q.text("%#x" % self.dst)
            q.breakable()
        q.text('}')

bsn.subtypes[2] = bsn_set_tunnel_dst

class copy_ttl_in(action):
    type = 12

    def __init__(self):
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append('\x00' * 4)
        length = sum([len(x) for x in packed])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = copy_ttl_in()
        _type = reader.read("!H")[0]
        assert(_type == 12)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        reader.skip(4)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        return True

    def pretty_print(self, q):
        q.text("copy_ttl_in {")
        with q.group():
            with q.indent(2):
                q.breakable()
            q.breakable()
        q.text('}')

action.subtypes[12] = copy_ttl_in

class copy_ttl_out(action):
    type = 11

    def __init__(self):
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append('\x00' * 4)
        length = sum([len(x) for x in packed])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = copy_ttl_out()
        _type = reader.read("!H")[0]
        assert(_type == 11)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        reader.skip(4)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        return True

    def pretty_print(self, q):
        q.text("copy_ttl_out {")
        with q.group():
            with q.indent(2):
                q.breakable()
            q.breakable()
        q.text('}')

action.subtypes[11] = copy_ttl_out

class dec_mpls_ttl(action):
    type = 16

    def __init__(self):
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append('\x00' * 4)
        length = sum([len(x) for x in packed])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = dec_mpls_ttl()
        _type = reader.read("!H")[0]
        assert(_type == 16)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        reader.skip(4)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        return True

    def pretty_print(self, q):
        q.text("dec_mpls_ttl {")
        with q.group():
            with q.indent(2):
                q.breakable()
            q.breakable()
        q.text('}')

action.subtypes[16] = dec_mpls_ttl

class dec_nw_ttl(action):
    type = 24

    def __init__(self):
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append('\x00' * 4)
        length = sum([len(x) for x in packed])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = dec_nw_ttl()
        _type = reader.read("!H")[0]
        assert(_type == 24)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        reader.skip(4)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        return True

    def pretty_print(self, q):
        q.text("dec_nw_ttl {")
        with q.group():
            with q.indent(2):
                q.breakable()
            q.breakable()
        q.text('}')

action.subtypes[24] = dec_nw_ttl

class group(action):
    type = 22

    def __init__(self, group_id=None):
        if group_id != None:
            self.group_id = group_id
        else:
            self.group_id = 0
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!L", self.group_id))
        length = sum([len(x) for x in packed])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = group()
        _type = reader.read("!H")[0]
        assert(_type == 22)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        obj.group_id = reader.read("!L")[0]
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        if self.group_id != other.group_id: return False
        return True

    def pretty_print(self, q):
        q.text("group {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("group_id = ");
                q.text("%#x" % self.group_id)
            q.breakable()
        q.text('}')

action.subtypes[22] = group

class nicira(experimenter):
    subtypes = {}

    type = 65535
    experimenter = 8992

    def __init__(self, subtype=None):
        if subtype != None:
            self.subtype = subtype
        else:
            self.subtype = 0
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!L", self.experimenter))
        packed.append(struct.pack("!H", self.subtype))
        packed.append('\x00' * 2)
        packed.append('\x00' * 4)
        length = sum([len(x) for x in packed])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        subtype, = reader.peek('!H', 8)
        subclass = nicira.subtypes.get(subtype)
        if subclass:
            return subclass.unpack(reader)

        obj = nicira()
        _type = reader.read("!H")[0]
        assert(_type == 65535)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        _experimenter = reader.read("!L")[0]
        assert(_experimenter == 8992)
        obj.subtype = reader.read("!H")[0]
        reader.skip(2)
        reader.skip(4)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        if self.subtype != other.subtype: return False
        return True

    def pretty_print(self, q):
        q.text("nicira {")
        with q.group():
            with q.indent(2):
                q.breakable()
            q.breakable()
        q.text('}')

experimenter.subtypes[8992] = nicira

class nicira_dec_ttl(nicira):
    type = 65535
    experimenter = 8992
    subtype = 18

    def __init__(self):
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!L", self.experimenter))
        packed.append(struct.pack("!H", self.subtype))
        packed.append('\x00' * 2)
        packed.append('\x00' * 4)
        length = sum([len(x) for x in packed])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = nicira_dec_ttl()
        _type = reader.read("!H")[0]
        assert(_type == 65535)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        _experimenter = reader.read("!L")[0]
        assert(_experimenter == 8992)
        _subtype = reader.read("!H")[0]
        assert(_subtype == 18)
        reader.skip(2)
        reader.skip(4)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        return True

    def pretty_print(self, q):
        q.text("nicira_dec_ttl {")
        with q.group():
            with q.indent(2):
                q.breakable()
            q.breakable()
        q.text('}')

nicira.subtypes[18] = nicira_dec_ttl

class output(action):
    type = 0

    def __init__(self, port=None, max_len=None, length=None):
        if port != None:
            self.port = port
        else:
            self.port = 0
        if max_len != None:
            self.max_len = max_len
        else:
            self.max_len = 0
        if length != None:
            self.length = length
        else:
            self.length = None
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(util.pack_port_no(self.port))
        packed.append(struct.pack("!H", self.max_len))
        packed.append('\x00' * 6)
        length = sum([len(x) for x in packed])
        if self.length is not None:
            length = self.length
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = output()
        _type = reader.read("!H")[0]
        assert(_type == 0)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        obj.port = util.unpack_port_no(reader)
        obj.max_len = reader.read("!H")[0]
        reader.skip(6)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        if self.port != other.port: return False
        if self.max_len != other.max_len: return False
        return True

    def pretty_print(self, q):
        q.text("output {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("port = ");
                q.text(util.pretty_port(self.port))
                q.text(","); q.breakable()
                q.text("max_len = ");
                q.text("%#x" % self.max_len)
            q.breakable()
        q.text('}')

action.subtypes[0] = output

class pop_mpls(action):
    type = 20

    def __init__(self, ethertype=None):
        if ethertype != None:
            self.ethertype = ethertype
        else:
            self.ethertype = 0
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!H", self.ethertype))
        packed.append('\x00' * 2)
        length = sum([len(x) for x in packed])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = pop_mpls()
        _type = reader.read("!H")[0]
        assert(_type == 20)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        obj.ethertype = reader.read("!H")[0]
        reader.skip(2)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        if self.ethertype != other.ethertype: return False
        return True

    def pretty_print(self, q):
        q.text("pop_mpls {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("ethertype = ");
                q.text("%#x" % self.ethertype)
            q.breakable()
        q.text('}')

action.subtypes[20] = pop_mpls

class pop_pbb(action):
    type = 27

    def __init__(self):
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append('\x00' * 4)
        length = sum([len(x) for x in packed])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = pop_pbb()
        _type = reader.read("!H")[0]
        assert(_type == 27)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        reader.skip(4)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        return True

    def pretty_print(self, q):
        q.text("pop_pbb {")
        with q.group():
            with q.indent(2):
                q.breakable()
            q.breakable()
        q.text('}')

action.subtypes[27] = pop_pbb

class pop_vlan(action):
    type = 18

    def __init__(self):
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append('\x00' * 4)
        length = sum([len(x) for x in packed])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = pop_vlan()
        _type = reader.read("!H")[0]
        assert(_type == 18)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        reader.skip(4)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        return True

    def pretty_print(self, q):
        q.text("pop_vlan {")
        with q.group():
            with q.indent(2):
                q.breakable()
            q.breakable()
        q.text('}')

action.subtypes[18] = pop_vlan

class push_mpls(action):
    type = 19

    def __init__(self, ethertype=None):
        if ethertype != None:
            self.ethertype = ethertype
        else:
            self.ethertype = 0
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!H", self.ethertype))
        packed.append('\x00' * 2)
        length = sum([len(x) for x in packed])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = push_mpls()
        _type = reader.read("!H")[0]
        assert(_type == 19)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        obj.ethertype = reader.read("!H")[0]
        reader.skip(2)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        if self.ethertype != other.ethertype: return False
        return True

    def pretty_print(self, q):
        q.text("push_mpls {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("ethertype = ");
                q.text("%#x" % self.ethertype)
            q.breakable()
        q.text('}')

action.subtypes[19] = push_mpls

class push_pbb(action):
    type = 26

    def __init__(self, ethertype=None):
        if ethertype != None:
            self.ethertype = ethertype
        else:
            self.ethertype = 0
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!H", self.ethertype))
        packed.append('\x00' * 2)
        length = sum([len(x) for x in packed])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = push_pbb()
        _type = reader.read("!H")[0]
        assert(_type == 26)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        obj.ethertype = reader.read("!H")[0]
        reader.skip(2)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        if self.ethertype != other.ethertype: return False
        return True

    def pretty_print(self, q):
        q.text("push_pbb {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("ethertype = ");
                q.text("%#x" % self.ethertype)
            q.breakable()
        q.text('}')

action.subtypes[26] = push_pbb

class push_vlan(action):
    type = 17

    def __init__(self, ethertype=None):
        if ethertype != None:
            self.ethertype = ethertype
        else:
            self.ethertype = 0
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!H", self.ethertype))
        packed.append('\x00' * 2)
        length = sum([len(x) for x in packed])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = push_vlan()
        _type = reader.read("!H")[0]
        assert(_type == 17)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        obj.ethertype = reader.read("!H")[0]
        reader.skip(2)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        if self.ethertype != other.ethertype: return False
        return True

    def pretty_print(self, q):
        q.text("push_vlan {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("ethertype = ");
                q.text("%#x" % self.ethertype)
            q.breakable()
        q.text('}')

action.subtypes[17] = push_vlan

class set_field(action):
    type = 25

    print("aaaaaaaaaaaaaaaaaaaaaaaaa")

    def __init__(self, field=None,length=None):
        if field != None:
            self.field = field
        else:
            self.field = None
        if length != None:
            self.length = length
        else:
            self.length = None
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(self.field.pack())
        length = sum([len(x) for x in packed])
        packed.append(loxi.generic_util.pad_to(8, length))
        if self.length is not None:
            length = self.length
        else:
            length += len(packed[-1])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = set_field()
        _type = reader.read("!H")[0]
        assert(_type == 25)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        obj.field = oxm.oxm.unpack(reader)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        if self.field != other.field: return False
        return True

    def pretty_print(self, q):
        q.text("set_field {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("field = ");
                q.pp(self.field)
            q.breakable()
        q.text('}')

action.subtypes[25] = set_field

class set_mpls_ttl(action):
    type = 15

    def __init__(self, mpls_ttl=None):
        if mpls_ttl != None:
            self.mpls_ttl = mpls_ttl
        else:
            self.mpls_ttl = 0
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!B", self.mpls_ttl))
        packed.append('\x00' * 3)
        length = sum([len(x) for x in packed])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = set_mpls_ttl()
        _type = reader.read("!H")[0]
        assert(_type == 15)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        obj.mpls_ttl = reader.read("!B")[0]
        reader.skip(3)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        if self.mpls_ttl != other.mpls_ttl: return False
        return True

    def pretty_print(self, q):
        q.text("set_mpls_ttl {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("mpls_ttl = ");
                q.text("%#x" % self.mpls_ttl)
            q.breakable()
        q.text('}')

action.subtypes[15] = set_mpls_ttl

class set_nw_ttl(action):
    type = 23

    def __init__(self, nw_ttl=None):
        if nw_ttl != None:
            self.nw_ttl = nw_ttl
        else:
            self.nw_ttl = 0
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!B", self.nw_ttl))
        packed.append('\x00' * 3)
        length = sum([len(x) for x in packed])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = set_nw_ttl()
        _type = reader.read("!H")[0]
        assert(_type == 23)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        obj.nw_ttl = reader.read("!B")[0]
        reader.skip(3)
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        if self.nw_ttl != other.nw_ttl: return False
        return True

    def pretty_print(self, q):
        q.text("set_nw_ttl {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("nw_ttl = ");
                q.text("%#x" % self.nw_ttl)
            q.breakable()
        q.text('}')

action.subtypes[23] = set_nw_ttl

class set_queue(action):
    type = 21

    def __init__(self, queue_id=None):
        if queue_id != None:
            self.queue_id = queue_id
        else:
            self.queue_id = 0
        return

    def pack(self):
        packed = []
        packed.append(struct.pack("!H", self.type))
        packed.append(struct.pack("!H", 0)) # placeholder for len at index 1
        packed.append(struct.pack("!L", self.queue_id))
        length = sum([len(x) for x in packed])
        packed[1] = struct.pack("!H", length)
        return ''.join(packed)

    @staticmethod
    def unpack(reader):
        obj = set_queue()
        _type = reader.read("!H")[0]
        assert(_type == 21)
        _len = reader.read("!H")[0]
        orig_reader = reader
        reader = orig_reader.slice(_len, 4)
        obj.queue_id = reader.read("!L")[0]
        return obj

    def __eq__(self, other):
        if type(self) != type(other): return False
        if self.queue_id != other.queue_id: return False
        return True

    def pretty_print(self, q):
        q.text("set_queue {")
        with q.group():
            with q.indent(2):
                q.breakable()
                q.text("queue_id = ");
                q.text("%#x" % self.queue_id)
            q.breakable()
        q.text('}')

action.subtypes[21] = set_queue


