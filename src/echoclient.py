#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import socket
s = socket()
s.connect(("127.0.0.1", 1234))
while True:
    output_data = input("> ")
    if output_data:
        s.send(output_data.to_bytes())
        input_data = s.recv(1024)
        if input_data:
            print(input_data)