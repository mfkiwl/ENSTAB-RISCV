#!/usr/bin/env python3

import os
import sys
from collections import OrderedDict


current_path = os.path.dirname(os.path.realpath(__file__))

# name,  (url, recursive clone, develop)
repos = [
    # HDL
    ("migen",      ("https://github.com/m-labs/",        True,  True)),

    # LiteX SoC builder
    ("litex",      ("https://github.com/enjoy-digital/", True,  True)),
]
repos = OrderedDict(repos)

if len(sys.argv) < 2:
    print("Available commands:")
    print("- init")
    print("- install (add --user to install to user directory)")
    print("- update")
    print("- driver")
    exit()

if "init" in sys.argv[1:]:
    
    os.system("wget https://static.dev.sifive.com/dev-tools/riscv64-unknown-elf-gcc-8.1.0-2019.01.0-x86_64-linux-ubuntu14.tar.gz")
    os.system("tar -xvf riscv64-unknown-elf-gcc-8.1.0-2019.01.0-x86_64-linux-ubuntu14.tar.gz")
    os.system("mv riscv64-unknown-elf-gcc-8.1.0-2019.01.0-x86_64-linux-ubuntu14 riscv64")
    
    for name in repos.keys():
        url, need_recursive, need_develop = repos[name]
        # clone repo (recursive if needed)
        print("[cloning " + name + "]...")
        full_url = url + name
        opts = "--recursive" if need_recursive else ""
        os.system("git clone " + full_url + " " + opts)

if "install" in sys.argv[1:]:
    for name in repos.keys():
        url, need_recursive, need_develop = repos[name]
        # develop if needed
        print("[installing " + name + "]...")
        if need_develop:
            os.chdir(os.path.join(current_path, name))
            if "--user" in sys.argv[1:]:
                os.system("python3 setup.py install --user")
            else:
                os.system("python3 setup.py install")

if "update" in sys.argv[1:]:
    for name in repos.keys():
        # update
        print("[updating " + name + "]...")
        os.chdir(os.path.join(current_path, name))
        os.system("git pull")
        
if "driver" in sys.argv[1:]:
    print("[installing adept.runtime]...")
    os.system("../../drivers_nexys4ddr/digilent.adept.runtime_2.19.2-x86_64/install.sh")
    print("[installing adept.utilities]...")
    os.system("../../drivers_nexys4ddr/digilent.adept.utilities_2.2.1-x86_64")
