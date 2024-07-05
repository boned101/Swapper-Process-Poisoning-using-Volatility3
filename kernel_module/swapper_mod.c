#include <linux/module.h>  // Essential for all kernel modules
#include <linux/kernel.h>   // KERN_INFO
#include <linux/init.h>     // __init and __exit macros
#include <linux/fs.h>       // For device numbers
#include <linux/cdev.h>     // For character device registration
#include <linux/device.h>   // For device creation
#include <linux/sched.h>    // For task_struct
#include <linux/sched/signal.h>  // For each_task

// Function prototypes for file operations
static int device_open(struct inode *, struct file *);
static ssize_t device_read(struct file *, char __user *, size_t, loff_t *);
static ssize_t device_write(struct file *, const char __user *, size_t, loff_t *);
static int device_release(struct inode *, struct file *);

// Define the operations that can be performed on the device
static struct file_operations fops = {
    .open = device_open,
    .read = device_read,
    .write = device_write,
    .release = device_release,
};

// Implementation of the file operations
static int device_open(struct inode *inode, struct file *file) {
    printk(KERN_INFO "Device opened\n");
    return 0;
}

static ssize_t device_read(struct file *file, char __user *buffer, size_t length, loff_t *offset) {
    printk(KERN_INFO "Device read\n");
    return 0;  // Return 0 bytes read
}

static ssize_t device_write(struct file *file, const char __user *buffer, size_t length, loff_t *offset) {
    printk(KERN_INFO "Device write\n");
    return length;  // Pretend that whatever was written was written successfully
}

static int device_release(struct inode *inode, struct file *file) {
    printk(KERN_INFO "Device closed\n");
    return 0;
}

static int majorNumber;  // Store the device number -- dynamically allocated
static struct cdev swapper_cdev;
static struct class* swapperClass = NULL; // Device class
static struct device* swapperDevice = NULL; // Device object

static void modify_task_struct(void) {
    struct task_struct *task;

    printk(KERN_INFO "Starting to modify task_struct\n");

    // Loop through each process
    for_each_process(task) {
        if (task->pid == 0) {  // swapper has PID 0
            printk(KERN_INFO "Swapper task found: %s (PID: %d)\n", task->comm, task->pid);
            // Example modification: Change priority
            task->prio = 20; // Just as an example, not recommended!
            // but who cares
            printk(KERN_INFO "Modified swapper's priority\n");
            break;
        }
    }

    printk(KERN_INFO "Finished modifying task_struct\n");
}

static int __init mod_init(void) {
    dev_t dev_num;
    // Allocate a major number dynamically
    if (alloc_chrdev_region(&dev_num, 0, 1, "swapper_dev") < 0) {
        return -1;
    }
    majorNumber = MAJOR(dev_num);

    // Create a cdev and add it to the kernel
    cdev_init(&swapper_cdev, &fops);
    if (cdev_add(&swapper_cdev, dev_num, 1) < 0) {
        unregister_chrdev_region(dev_num, 1);
        return -1;
    }

    // Create a class
    swapperClass = class_create(THIS_MODULE, "swapper");
    if (IS_ERR(swapperClass)) {
        cdev_del(&swapper_cdev);
        unregister_chrdev_region(dev_num, 1);
        return -1;
    }

    // Create a device
    swapperDevice = device_create(swapperClass, NULL, dev_num, NULL, "swapper_device");
    if (IS_ERR(swapperDevice)) {
        class_destroy(swapperClass);
        cdev_del(&swapper_cdev);
        unregister_chrdev_region(dev_num, 1);
        return -1;
    }

    printk(KERN_INFO "Swapper device class created correctly\n");

    // Call the function to modify the swapper task_struct
    modify_task_struct();

    return 0;
}

static void __exit mod_exit(void) {
    device_destroy(swapperClass, MKDEV(majorNumber, 0));
    class_unregister(swapperClass);
    class_destroy(swapperClass);
    cdev_del(&swapper_cdev);
    unregister_chrdev_region(MKDEV(majorNumber, 0), 1);
    printk(KERN_INFO "Swapper device class removed\n");
}

MODULE_LICENSE("GPL");
module_init(mod_init);
module_exit(mod_exit);
