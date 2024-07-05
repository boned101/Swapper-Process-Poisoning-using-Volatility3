#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int main(void)
{
    int fd;

    fd = open("/dev/swapper_device", O_RDWR);
    if (fd < 0) {
        perror("Failed to open /dev/swapper_device");
        return 1;
    }

    printf("User-space program interacting with swapper device\n");

    close(fd);
    return 0;
}
