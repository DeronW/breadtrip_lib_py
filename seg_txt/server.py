#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.tcpserver import TCPServer
from tornado.ioloop import IOLoop
import jieba
import json
from tornado import stack_context

TCPSERVER_HOST = '0.0.0.0'


class SegTxtServer(TCPServer):
    def __init__(self, no_keep_alive=False, protocol=None, **kwargs):
        self.no_keep_alive = no_keep_alive
        self.protocol = protocol
        TCPServer.__init__(self, **kwargs)

    def handle_stream(self, stream, address):
        SegTxtConnection(stream, address, self.no_keep_alive, self.protocol)


class SegTxtConnection(object):

    def __init__(self, stream, address, no_keep_alive=False, protocol=None):
        self.stream = stream
        self.address = address
        self.no_keep_alive = no_keep_alive
        self.protocol = protocol
        self._requset = None
        self._requset_finished = False
        self._write_callback = None
        self._close_callback = None
        self._header_callback = stack_context.wrap(self._on_header)
        self.stream.read_until("&&", self._on_seg_txt)

    def _on_header(self, data):
        self.stream.read_until(data, self._on_seg_txt)

    def _on_seg_txt(self, data):
        data = data.split("&&")[0]
        modal, txt = data.split("|")
        if modal == "full":
            seg_list = list(jieba.cut(txt, cut_all=True))
            seg_list = [ x for x in seg_list if x]
        elif modal == "search":
            seg_list = list(jieba.cut_for_search(txt))
        else:
            seg_list = list(jieba.cut(txt))
        self.request_callback(json.dumps(seg_list))

    def request_callback(self, data):
        self.write(data, self.finish)

    def _clear_callbacks(self):
        self._write_callback = None
        self._close_callback = None

    def close(self):
        self.stream.close()
        self._header_callback = None
        self._clear_callbacks()

    def write(self, data, callback=None):
        if not self.stream.closed():
            self._write_callback = stack_context.wrap(callback)
            self.stream.write(data, self._on_write_complete)

    def _on_write_complete(self):
        if self._write_callback is not None:
            callback = self._write_callback
            self._write_callback = None
            callback()

        if self._requset_finished and not self.stream.writing():
            self._finish_request()

    def finish(self):
        self._requset_finished = True
        if not self.stream.writing():
            self._finish_request()

    def _finish_request(self):
        if self.no_keep_alive:
            disconnect = True
        else:
            disconnect = False

        if disconnect:
            self.stream.close()
            return


def main():
    segtxt_server = SegTxtServer()
    segtxt_server.listen(8888, address=TCPSERVER_HOST)
    IOLoop.instance().start()


if __name__ == '__main__':
    main()
