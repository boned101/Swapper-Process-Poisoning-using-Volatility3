import os
import shutil
import re

from volatility3.framework import contexts
from volatility3.framework.configuration import requirements
from volatility3.framework import exceptions
from volatility3.framework.layers import scanners
from volatility3.plugins.linux import pslist as linux_pslist

_required_framework_version = (2, 0, 1)

# ***************
#  Utilities functions
#  Some of them are not used
# ***************

def search_in_chunks(file_path, pattern, chunk_size=4096):
    """Generator to search for a pattern in chunks to handle large files."""
    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            for match in re.finditer(pattern, chunk):
                yield match.start() + file.tell() - chunk_size

def duplicate_dump(original_dump_path, modified_dump_path):
    """Duplicate the dump file to a new location."""
    shutil.copy2(original_dump_path, modified_dump_path)
    print(f"Dump file duplicated: {modified_dump_path}")

def modify_swapsign_in_dump(dump_path, swapper_signature, new_signature):
    """Search for swapper signatures in the dump and modify them."""
    if not (len(swapper_signature) == len(new_signature)):
        print(f"len(swapper_signature) = {len(swapper_signature)} and len(new_signature) = {len(new_signature)}")
        print("New signature must be the same length as the old signature")
        raise AssertionError("New signature must be the same length as the old signature")

    offsets = []
    
    # Search for swapper signature
    for offset in search_in_chunks(dump_path, swapper_signature):
        offsets.append(offset)
        print(f"Found swapper signature at offset: {offset}")

    # Modify found signatures
    if offsets:
        with open(dump_path, 'r+b') as file:
            for offset in offsets:
                file.seek(offset)
                file.write(new_signature)
            print(f"Modified {len(offsets)} occurrences of swapper signature.")
    else:
        print("Swapper signature not found.")
        
def modify_extension_in_dump(dump_path, wanted_signature, new_signature):
    """
    Search for process signatures in the dump and modify them
    by inserting new data without overwriting existing content.
    """
    import os
    
    # First, find all occurrences of the wanted signature
    offsets = []
    with open(dump_path, 'rb') as file:
        chunk_size = 4096
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            for match in re.finditer(wanted_signature, chunk):
                offsets.append(match.start() + file.tell() - chunk_size)

    # If no signature is found, exit the function
    if not offsets:
        print("Wanted signature not found.")
        return

    # Sort offsets in reverse order to avoid messing up the positions as we expand the file
    offsets.sort(reverse=True)

    # Modify found signatures by inserting new data
    with open(dump_path, 'r+b') as file:
        for offset in offsets:
            file.seek(offset)
            original_data = file.read(len(wanted_signature))
            file.seek(offset)

            if len(new_signature) > len(wanted_signature):
                # If new_signature is longer, we need to shift subsequent data
                rest_of_file = file.read()
                file.seek(offset)
                file.write(new_signature)
                file.write(rest_of_file)
            else:
                # If new_signature is shorter or equal, write it directly
                file.write(new_signature + original_data[len(new_signature):])

            print(f"Modified occurrence at offset: {offset} with new data.")

    print(f"Modified {len(offsets)} occurrences of the wanted signature.")
        

# function from volatility3/framework/automagic/linux.py        
def virtual_to_physical_address(cls, addr: int) -> int:
        """
        Converts a virtual linux address to a physical one (does not account
        of ASLR)
        """
        if addr > 0xFFFFFFFF80000000:
            return addr - 0xFFFFFFFF80000000
        return addr - 0xC0000000


def modify_dump_at_physical_offset(dump_path, offset_hex, new_signature):
    """Modify the dump at a specific physical offset with a new signature."""
    # Convert hex offset to integer
    physical_offset = int(offset_hex, 16)
    
    with open(dump_path, 'r+b') as file:
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        
        # Convert virtual address to a probable physical offset (if needed)
        # This step is where you need actual logic or a tool to convert addresses
        probable_physical_offset = physical_offset # Change this line to use a real conversion method
        
        # Check if the calculated physical offset is within the file size
        if probable_physical_offset >= file_size:
            print(f"Error: Physical offset {probable_physical_offset} is beyond the file size of {file_size}.")
            return
        
        file.seek(probable_physical_offset)
        file.write(new_signature)
        print(f"Modified dump at physical offset {probable_physical_offset}.")
        
def modify_process_name(context, kernel, pid, new_name):
    linux_pslist = linux_plugins.pslist.PsList(context, kernel.layer_name, kernel.symbol_table_name)

    # Find the task_struct for the specified PID
    for task in linux_pslist.list_tasks(context, kernel.symbol_table_name):
        if task.pid == pid:
            # Calculate the offset to the comm field (assuming offset is known)
            comm_offset = task.vol.offset + task.vol.type.object_type.relative_child_offset("comm")
            
            # Write the new name to the comm field, padded or trimmed to fit
            new_comm = new_name[:15].ljust(16, '\x00').encode('utf-8')
            context.layers[kernel.layer_name].write(comm_offset, new_comm)
            print(f"Process name for PID {pid} changed to {new_name}")
            break
    else:
        print("PID not found")
        
# ***************
#  TRAPS
# ***************
        
def trap1(original_dump_path, modified_dump_path, swapper_signature, new_signature):
    duplicate_dump(original_dump_path, modified_dump_path)
    modify_swapsign_in_dump(modified_dump_path, swapper_signature, new_signature)
    
def test_modify_process_name(profile_path, target_pid, new_process_name):
    ctx = contexts.Context()
    fail = ctx.config.read(profile_path)

    # Load the memory layer
    layer_name = "IntelLayer"
    symbol_table_name = "LinuxKernelSymbols"

    try:
        modify_process_name(ctx, layer_name, symbol_table_name, target_pid, new_process_name)
    except exceptions.VolatilityException as exc:
        print(f"An error occurred: {exc}")

def trap2(original_dump_path, modified_dump_path, swapper_signature, physical_offset):
    duplicate_dump(original_dump_path, modified_dump_path)
    modify_dump_at_physical_offset(modified_dump_path, physical_offset, swapper_signature)

if __name__ == "__main__":
    trap2()