# Volatility 3 Swapper Poisoning

## Problem Statement

**P3 -  Volatility3 Poisoning (1-2 students, 3 groups)**

Volatility 3 uses a signature to detect the correct radix-tree to start the analysis of a Linux dump. 
The signature ("swapper\0") is the name of the idle process and is contained in a field of its  task_struct. What happens if the signature is overwritten by a malicious kernel module? 
The system continue to run correctly or crash? Volatility is able to continue the analysis? 

What happens if multiple process have this signature? Volatility is able to distinguish them?

This project is composed by two parts:
- (EASY) modify a memory dump by overwriting the "swapper\0" string and check the behaviour of Volatility3. Overwrite also other process names with the signature to check if Volatility 3 is able to distinguish them.
- (MEDIUM) write a simple kernel module that modifies the task_struct of swapper\0 and check the system stability. Create also other user-space program with the name equal to the signature and check the system behaviour.



## Project Introduction

This project is composed of  `development.ipynb` notebook based on our `poisoning.py` library.

`development.ipynb` notebook compiles commands and modifications to  memory dumps we took on a Debian 12 system and using volatility3.

We also developed a user space kernel module `swapper_mod.c`  and `swapper_user.c` using C to modify the guest VM's swapper process , specifically the task struct so we can check system stability via volatility3. 


We took a dump of the modified system and then ran some volatility3 plugins. the results are all in the report `P3_Final_Report.pdf`.

## Setup Instructions

Please note you will need:
1. volatility3
2. dwarf2json
3. LiME

Dont hesitate to contact us. if there are issues at any step. 

To help anyone who want to reproduce our work,Please follow the process below, it is also separately available in the setup.md 

# Setup

## How to make it start working!

Please set up a Debian 12 VM first, get it at https://www.debian.org/download

and we recommend making a directory called Forensic.

Install necessary packages:

```sh
sudo apt update
sudo apt-get install -y build-essential linux-headers-$(uname -r) git
sudo apt-get install -y unzip
sudo apt install golang-go
```

- Now take the memory dump using Lime, get it at https://github.com/504ensicsLabs/LiME


Installing and building LiME:

```sh
cd ~/Forensic
git clone https://github.com/504ensicsLabs/LiME.git
cd ~/Forensic/LiME/src
make clean
make
```

Loading the LiME kernel module:
```sh
sudo insmod lime-$(uname -r).ko "path=/path/to/output.lime format=lime"
```

Unloading the LiME kernel module after you get the memory dump, **important!**:
```sh
sudo rmmod lime
```

PLEASE PLEASE MAKE SURE TO Change ownership and permissions of the memory dump and all future memory dumps:

```sh
sudo chown user:group /path/to/output.lime
chmod 666 /path/to/output.lime
```


## How to use volatility3 and dwarf2json

So we need to build volatility3 profile using dwarf2json, using both the SystemMap and vmlinux file. Then you should be ready to run volatility3 using the profile and memory dump.


```sh
git clone https://github.com/volatilityfoundation/volatility3.git
```

as a repository or if you want via pip3 as a library!

or install it inside from the git repo after cloning using the setup.py

```sh
sudo apt install golang-go
git clone https://github.com/volatilityfoundation/dwarf2json.git
cd dwarf2json
go build
sudo mv dwarf2json /usr/local/bin/
```

NOW we can finally get a profile!
```sh
sudo dwarf2json linux --elf /usr/lib/debug/boot/vmlinux-$(uname -r) --system-map /usr/lib/debug/boot/System.map-$(uname -r) > debian.json
```

move the profile you built into a folder called profiles. We recommend it!

```sh
mv debian.json > ~/Forensic/profiles
```

## The notebook and kernel module

we used code to run our notebook which is a ipynb file. Quickly get VS code here if you dont have it!
 
```sh
sudo apt install software-properties-common apt-transport-https wget
wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
sudo apt update
sudo apt install code
```
Now get our repository if you haven't already: 

```sh
cd ~/Forensics
git clone https://gitlab.eurecom.fr/veysseyr/forensics_pr3.git
cd forensics_pr3
```

Just make a new environment for python for best practice , also we need ipykernel in this environment without conflicts.

```sh
sudo apt install python3-venv python3-pip
pip install ipykernel 
source venv/bin/activate
```

after this try running the notebook, it may ask you to install ipyknernel, hopefully you can switch the python environment inside code to the virtual environment one.

we need to install volatility 3 for this new environment. Or you can do it yourself from the repo directly! just make sure your IDE has access to the volatility3 python package.

```sh
pip install git+https://github.com/volatilityfoundation/volatility3.git
```

Now setup your folders inside the `development.ipynb` notebook in a similar manner.

```sh
homedir = "/home/dorkt990"
symboldir = "/home/dorkt990/profiles"
volpypath = "/home/dorkt990/Forensic/volatility3"
datapath = "/home/dorkt990"
dumppath = f"{datapath}/memory_dump.lime"
dumppath_corrupt1 = f"{datapath}/corrupt1_memory_dmp.lime"
dumppath_corrupt2 = f"{datapath}/corrupt2_memory_dmp.lime"
dumppath_moded = f"{datapath}/memory_dmp_moded.lime"
original_path = os.getcwd()
```
After you should be able to run the notebook and follow the Instructions inside uptil the end of part 1. 

Before you start section 2.1 you should follow the section below

## Kernel Module 
Okay now you basically need to build our user space kernel module.

```sh
cd ~/Forensic/LiME/src
make clean
make
```

Make sure you dont have the module already loaded. Just to be sure.
```sh
sudo rmmod swapper_mod
```
Now use the module!
```sh
sudo insmod ./build/swapper_mod.ko

gcc -o build/swapper_user swapper_user.c
sudo ./build/swapper_user
```


Check your kernel logs to see the swapper device being used and unloaded.
```sh
sudo dmesg | tail -n 30
```

Now remember you need to take a fresh memory dump of your guest VM, which just had it's swapper modified.

```sh
cd ~/Forensic/LiME/src
sudo insmod lime-6.1.0-22-amd64.ko path=~/memory_dmp_moded.lime format=lime
```
Now go back to the notebook, the last part!

After this you should be able to run the last pslist command. you are free to run any other volatility commands as you wish.

We recommend the following plugins for interesting details!:

```
- linux.pslist
- linux.proc.Map
- linux.check_idt
- linux.check_syscall
```

Please read the report for more! 
