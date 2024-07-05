```sh
git clone https://github.com/volatilityfoundation/volatility3.git
```

as a repository or if you want via pip3 as a library!

or install it from the git repo after cloning.

```sh
sudo apt install golang-go
git clone https://github.com/volatilityfoundation/dwarf2json.git
cd dwarf2json
go build
sudo mv dwarf2json /usr/local/bin/

sudo dwarf2json linux --elf /usr/lib/debug/boot/vmlinux-$(uname -r) --system-map /usr/lib/debug/boot/System.map-$(uname -r) > debian.json


vol -f ./memory_dump.lime -s ./Forensic/ linux.pslist
```


we used code to run our notebook. 

```sh
sudo apt install software-properties-common apt-transport-https wget
wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
sudo apt update
sudo apt install code

cd ~/
git clone https://gitlab.eurecom.fr/veysseyr/forensics_pr3.git
cd forensics_pr3

sudo apt install python3-venv python3-pip
source venv/bin/activate
```

after this try running the notebook, it may ask you to install ipyknernel

we may need to install volatility 3 for this new environment
```sh
pip install git+https://github.com/volatilityfoundation/volatility3.git
```


after setting all this up.

We recommend setting up a separate folder for profiles in the home directory and placing the json profile. Th first part of the notebook must be setup for it to work


After the first part we will have to use the kernel module we made.

Please refer to the README file in the kernel module folder for command instructions after you cd into the kernel module directory in a terminal.
