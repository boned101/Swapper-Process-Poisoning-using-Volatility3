obj-m += swapper_mod.o
BUILD_DIR := build

all: 
	@mkdir -p $(BUILD_DIR)
	@make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules
	@echo "Checking and moving files to $(BUILD_DIR)"
	@for file in $(PWD)/*.o $(PWD)/*.ko $(PWD)/*.mod.* $(PWD)/.*.cmd $(PWD)/modules.order $(PWD)/Module.symvers; do \
		if [ -f "$$file" ]; then \
			echo "Moving $$file"; \
			mv -f $$file $(BUILD_DIR)/ || echo "Failed to move $$file"; \
		else \
			echo "File not found: $$file"; \
		fi \
	done
	@mv -f swapper_mod.mod $(BUILD_DIR)/ || echo "Failed to move swapper_mod.mod"
	@echo "Files moved successfully"

clean:
	@make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
	@rm -rf $(BUILD_DIR)
