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

To help anyone who want to reproduce our work, We wrote our setup process in `setup.md`.