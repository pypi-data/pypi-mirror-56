#!/usr/bin/env python
#-*- coding: utf-8 -*-
#pylint: disable=
"""
File       : NATS.py
Author     : Valentin Kuznetsov <vkuznet AT gmail dot com>
Description: python implementation of NATS publisher manager based on
- python2 implemenation via tornado module, see
  https://github.com/nats-io/nats.py2
  https://pypi.org/project/nats-client/
- python3 implementation via asyncio module, see
  https://github.com/nats-io/nats.py
  https://pypi.org/project/asyncio-nats-client/
- external tool, via
  go get github.com/nats-io/go-nats-examples/tools/nats-pub

Basic usage instructions:
    
..doctest:

    data = [...]   # list of dicts
    topics = [...] # list of publisher topics, e.g. cms, T2
    attrs = [...]  # list of attributes to filter from data
    # server can be in a form of 'nats://host:port' or
    # nats with user/passwords 'nats://user:password@host:port'
    # tls  with user/password  'tls://user:password@host:port'
    server = 'nats://host:port'
    mgr = NATSManager(server, topics=topics, attrs=attrs, stdout=True)
    mgr.publish(data)
"""

# system modules
import os
import re
import sys
import random
import subprocess

try:
    # python3 NATS implemenation via asyncio module
    import asyncio
    from CMSMonitoring.nats3 import nats
    NATS2 = False
except ImportError:
    # python2 NATS implemenation via tornado module
    import tornado.ioloop
    import tornado.gen
    from CMSMonitoring.nats2 import nats
    NATS2 = True

def nats_encoder(doc, sep='   '):
    "CMS NATS message encoder"
    keys = sorted(doc.keys())
    msg = sep.join(['{}:{}'.format(k, doc[k]) for k in keys])
    return msg

def nats_decoder(msg, sep='   '):
    "CMS NATS message decoder"
    rec = {}
    for pair in msg.split(sep):
        arr = pair.split(':')
        rec.update({arr[0]:arr[1]})
    return rec

def def_filter(doc, attrs=None):
    "Default filter function for given doc and attributes"
    rec = {}
    if not attrs:
        yield doc
        return
    for attr in attrs:
        if attr in doc:
            rec[attr] = doc[attr]
    yield rec


class NATSManager(object):
    """
    NATSManager provide python interface to NATS server. It accepts:
    :param server: server name
    :param topics: list of topics, i.e. where messages will be published
    :param attrs: list of attributes to select for publishing
    :param default_topic: default topic 'cms'
    :param stdout: instead of piblishing print all messages on stdout, boolean
    :param cms_filter: name of cms filter function, by default `def_filter` will be used
    """
    def __init__(self, server=None, topics=None, attrs=None, sep='   ', default_topic='cms', stdout=False, cms_filter=None):
        self.topics = topics
        self.server = []
        self.sep = sep
        for srv in server.split(','):
            self.server.append(srv)
        self.def_topic = default_topic
        self.stdout = stdout
        self.attrs = attrs
        self.cms_filter = cms_filter if cms_filter else def_filter

    def __repr__(self):
        return 'NATSManager@{}, topics={} def_topic={} attrs={} cms_filter={} stdout={}'.format(hex(id(self)), self.topics, self.def_topic, self.attrs, self.cms_filter, self.stdout)

    def publish(self, data):
        "Publish given set of docs to topics"
        all_msgs = []
        mdict = {}
        if not self.topics:
            for doc in data:
                for rec in self.cms_filter(doc, self.attrs):
                    msg = nats_encoder(rec, self.sep)
                    for key, val in rec.items():
                        if key == 'exitCode' and val != "":
                            mdict.setdefault(key, []).append(msg)
                            mdict.setdefault(str(val), []).append(msg)
                        elif key == 'site' and val != "":
                            # collect site wilcards, use NATS '.' wildcard
                            subject = val.replace('_', '.')
                            mdict.setdefault(subject, []).append(msg)
                        elif key == 'task' and val != "":
                            # collect task wilcards, use NATS '.' wildcard
                            subject = val.replace('/', '.')
                            if subject.startswith('.'):
                                subject = subject[1:]
                            mdict.setdefault(subject, []).append(msg)
                        else:
                            if val != "":
                                # collect messages on invidual topics
                                mdict.setdefault(str(val), []).append(msg)
                    all_msgs.append(msg)
            # send all messages from collected mdict
            for key, msgs in mdict.items():
                self.send(key, msgs)
            # send message to default topic
            self.send(self.def_topic, all_msgs)
            return
        cms_msgs = []
        for topic in self.topics:
            top_msgs = []
            pat = re.compile(topic)
            for doc in data:
                for rec in self.cms_filter(doc, self.attrs):
                    msg = nats_encoder(rec, self.sep)
                    if msg.find(topic) != -1 or pat.match(msg):
                        top_msgs.append(msg) # topic specific messages
                    cms_msgs.append(msg) # cms messages
            self.send(topic, top_msgs)
        # always send all messages to default topic
        self.send(self.def_topic, cms_msgs)

    def send_stdout(self, subject, msg):
        "send subject/msg to stdout"
        if isinstance(msg, list):
            for item in msg:
                print("{}: {}".format(subject, item))
        else:
            print("{}: {}".format(subject, msg))

    def get_server(self):
        "Return random server from server pool"
        if len(self.server) > 1:
            return self.server[random.randint(0, len(self.server)-1)]
        return self.server[0]

    def send(self, subject, msg):
        "send given message to subject topic"
        if self.stdout:
            self.send_stdout(subject, msg)
        else:
            try:
                server = self.get_server()
                if NATS2:
                    tornado.ioloop.IOLoop.current().run_sync(lambda: nats(server, subject, msg))
                else:
                    # VK: we need to test initializing asyncio loop in ctor
                    # and potentially avoid loop creation here
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(nats(server, subject, msg, self.loop))
                    loop.close()
            except Exception as exp:
                print("Failed to send docs to NATS, error: {}".format(str(exp)))


def nats_cmd(cmd, server, subject, msg):
    "NATS publisher via external nats cmd tool"
    if not os.path.exists(cmd):
        print("Unable to locate publisher tool '{}' on local file system".format(cmd))
        return
    if not server:
        print("No NATS server...")
        return
    if isinstance(msg, list):
        for item in msg:
            pcmd = '{} -s {} {} "{}"'.format(cmd, server, subject, msg)
            proc = subprocess.Popen(pcmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=os.environ)
            proc.wait()
    else:
        pcmd = '{} -s {} {} "{}"'.format(cmd, server, subject, msg)
        proc = subprocess.Popen(pcmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=os.environ)
        proc.wait()
        return proc.returncode

class NATSManagerCmd(NATSManager):
    "NATS manager based on external publisher tool"
    def __init__(self, cmd, server=None, topics=None, attrs=None, sep='   ', default_topic='cms', stdout=False, cms_filter=None):
        self.pub = cmd
        super(NATSManagerCmd, self).__init__(server, topics, attrs, sep, default_topic, stdout, cms_filter)

    def __repr__(self):
        return 'NATSManagerCmd@{}, topics={} def_topic={} attrs={} cms_filter={} stdout={}'.format(hex(id(self)), self.topics, self.def_topic, self.attrs, self.cms_filter, self.stdout)

    def send(self, subject, msg):
        "Call NATS function, user can pass either single message or list of messages"
        if self.stdout:
            self.send_stdout(subject, msg)
        else:
            server = self.get_server()
            nats_cmd(self.cmd, server, subject, msg)

def test():
    "Test function"
    subject = 'cms'
    msg = 'test from python'
    doc = {'site':'1', 'attr':'1'}
    sep = '   '
    msg = nats_encoder(doc, sep)
    print(msg)
    rec = nats_decoder(msg)
    print(doc, rec)

    data = [{'site':'Site_TEST', 'attr':str(i), 'task':'task-%s'%i} for i in range(10)]
    server = '127.0.0.1,127.0.0.2'
    attrs = ['site', 'attr', 'task']
    mgr = NATSManager(server, attrs=attrs, stdout=True)
    print("Test NATSManager", mgr)
    mgr.publish(data)
    # create new manager with topics
    topics = ['attr']
    mgr = NATSManager(server, topics=topics, attrs=attrs, stdout=True)
    print("Test NATSManager", mgr)
    mgr.publish(data)

    # create new manager with custom filter and topics
    def custom_filter(doc, attrs=None):
        "Custom filter function for given doc and attributes"
        rec = {}
        for attr in attrs:
            if attr in doc:
                rec[attr] = doc[attr]
        rec['enriched'] = True
        yield rec
    mgr = NATSManager(server, topics=topics, attrs=attrs, cms_filter=custom_filter, stdout=True)
    print("Test NATSManager", mgr)
    mgr.publish(data)

    # test with real server
    server = 'test:test@127.0.0.1:4222'
    mgr = NATSManager(server, topics=topics, attrs=attrs)
    print("Test NATSManager", mgr)
    mgr.publish(data)

if __name__ == '__main__':
    test()
