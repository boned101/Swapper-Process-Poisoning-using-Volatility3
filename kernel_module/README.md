# Kernel Module

This kernel module modified the swapper size


```sh
make clean
make

sudo rmmod swapper_mod
sudo insmod ./build/swapper_mod.ko

gcc -o build/swapper_user swapper_user.c
sudo ./build/swapper_user

```

```sh
sudo dmesg | tail -n 20
```

```
[ 4258.207263] RDX: 0000000000000000 RSI: 0000000000000800 RDI: 000056508185d7c8
[ 4258.207264] RBP: 0000000000000000 R08: 1999999999999999 R09: 0000000000000000
[ 4258.207264] R10: 00007f75f879bac0 R11: 0000000000000206 R12: 00007ffe680f92a0
[ 4258.207265] R13: 00007ffe680f97cf R14: 000056508185d2a0 R15: 00007ffe680f92a8
[ 4258.207267]  </TASK>
[ 4258.207267] ---[ end trace 0000000000000000 ]---
[ 4258.207270] Swapper device class removed
[ 4261.270085] Swapper device class created correctly
[ 4282.890394] Device opened
[ 4282.890475] Device closed
[ 4545.568984] Swapper device class removed
[ 4896.969329] Swapper device class created correctly
[ 4903.294762] Device opened
[ 4903.294786] Device closed
[ 5075.514893] Swapper device class removed
[ 5096.590044] Swapper device class created correctly
[ 5096.590049] Starting to modify task_struct
[ 5096.590081] Finished modifying task_struct
[ 5111.953781] Device opened
[ 5111.953815] Device closed
```

```sh
cd ../../LiME/src
output_file="../../data/memory_dmp_moded.lime"
sudo insmod lime-6.1.0-21-amd64.ko "path=$output_file format=lime"
```

If the above doesnt work then use absolute path like this below:

```sh
sudo insmod lime-6.1.0-22-amd64.ko path=/home/dorkt990/memory_dmp_moded.lime format=lime
```

```sh
sudo rmmod lime
sudo chown dadmin:dadmin $output_file
chmod 666 $output_file
```