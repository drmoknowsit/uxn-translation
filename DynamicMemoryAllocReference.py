#!/usr/bin/env python3

# Dynamic memory allocation using pages and a bitmap

# We allocate 16 bytes per page
PAGE_SZ = 16 # in bytes 0x0010
MAX_N_ALLOCS = 32 # no more than 32 allocations are supported in a program

# We have a total of 256 pages, so we can allocate at most 4kB
N_PAGES = 1024>>2 # 0x0100
MAX_ALLOC_SZ = PAGE_SZ*N_PAGES
DMEM_START = 64*1024-PAGE_SZ*N_PAGES

# N_PAGES bits, packed in bytes mean N_PAGES/8 entries, so with the above, the bitmap will take 64 bytes
# 0 means free
bitmap = [0] * (N_PAGES>>3)


# We need to keep track of how many bytes are allocated for each pointer returned by malloc. 
# In Python, this is easy, we use a dictionary:

allocated = {}
n_allocs = 0
error = 0
errors= [ "",
    # ( 1 )
    "Null pointer",
    # ( 2 )
    "Invalid pointer:",
    # ( 3 )
    "Invalid access:",
    # ( 4 )
    "Outside of page range:",
    # ( 5 )
    "Max number of allocations reached",
    # ( 6 )
    "Pointer was not allocated",
    # ( 7 )
    "Allocation too large"
]

# To test this we need to create the actual memory, the pointer returned by malloc is the index into this memory.
memory = [0] * (64*1024) # 64kB

# Takes the number of bytes to be allocated
# returns a pointer, i.e. the address of the start of the allocated memory region
def malloc(n_bytes) :
    global n_allocs, allocated, error
    error = 0
    if n_bytes==0:
        error = 1
        return 0
    n_pages = ((n_bytes-1) // PAGE_SZ) + 1 # integer division
    # print('n_pages:',n_pages,PAGE_SZ*n_pages,n_bytes)
    if n_pages>N_PAGES:
        error = 7
        return 0
    # print('M',n_bytes)
    for idx in range(N_PAGES): # 0 .. N_PAGES-1
        # print('malloc:',idx,n_pages)
        if alloc_sz_is_free_at_idx(idx, n_pages):
            if error>0:
                return 0
            claim_alloc_sz_at_idx(idx, n_pages)
            if n_allocs == MAX_N_ALLOCS:
                error = 5
                return 0
            else:
                # exit(0)                
                n_allocs = n_allocs + 1
                ptr = idx*PAGE_SZ+DMEM_START
                # print('M',ptr,n_bytes)
                allocated[ptr]=n_bytes
                return ptr
    return 0 # Null pointer

def free(ptr) :    
    global n_allocs, allocated, error
    idx = (ptr-DMEM_START) // PAGE_SZ
    if idx<0 or idx>N_PAGES-1:
        error=2
        # raise NameError("Invalid pointer")
    else:
        if ptr in allocated:
            error=0
            n_bytes = allocated[ptr]
            # print('F',n_bytes)
            n_pages = ((n_bytes-1) // PAGE_SZ) + 1 # integer division
            
            # print('F',n_pages,ptr)
            free_alloc_sz_at_idx(idx, n_pages)
            del allocated[ptr] 
            n_allocs = n_allocs - 1
        else:
            error=6
            # raise NameError("Pointer was not allocated")

def get_bit(idx) :
    global bitmap, error
    byte_idx = idx >> 3
    bit_idx = 7 - (idx - (byte_idx<<3))
    if byte_idx > N_PAGES-1:
        # raise NameError("Outside of page range")
        error=4
        # exit(0)
    byte = bitmap[byte_idx]
    # if byte is None:
    #     print("Invalid access:", byte_idx)
    #     exit(0)
    bit = (byte >> bit_idx) & 0x01
    return bit

def set_bit(idx) :
    global bitmap
    byte_idx = idx >> 3
    bit_idx = 7 - idx + (byte_idx<<3)
    byte = bitmap[byte_idx]
    bitmap[byte_idx] = byte | mask_set(bit_idx)

def mask_set(bit_idx):
    return (1 << bit_idx)

def clear_bit(idx) :
    global bitmap
    byte_idx = idx >> 3
    bit_idx = 7 - idx + (byte_idx<<3)
    byte = bitmap[byte_idx]
    # mask = 0xFF ^ (1 << bit_idx) # 1110111
    bitmap[byte_idx] = byte & mask_clear(bit_idx)

def mask_clear(bit_idx):
    return (0xFF ^ (1 << bit_idx))

# allocation size is in pages
def alloc_sz_is_free_at_idx(idx, alloc_sz) :
    global bitmap, error
    for jj in range(alloc_sz) : 
        # print('alloc_sz_is_free_at_idx:',idx,jj)
        if(idx+jj>N_PAGES-1):
            error=4
            return 0 
        if (get_bit(idx+jj)==1):
            # print(bitmap)
            # print('alloc_sz_is_free_at_idx: get_bit(',idx+jj,') == 1')
            return 0
    return 1

# allocation size is in pages
def claim_alloc_sz_at_idx(idx, alloc_sz) : 
    for jj in range(alloc_sz):
        # print('claim_alloc_sz_at_idx:',idx,alloc_sz,jj)
        set_bit(idx+jj)

# allocation size is in pages
def free_alloc_sz_at_idx(idx, alloc_sz) :
    for jj in range(alloc_sz):
        clear_bit(idx+jj)

# These functions are for unit testing and integration testing.
# They are defined here because the globals they access are defined here

# This resets memory, allocated and n_allocs for test purposes
def reset():
    global n_allocs, allocated, bitmap, memory
    n_allocs = 0
    bitmap = [0] * (N_PAGES>>3)
    allocated = {}
    memory = [0] * (64*1024) 
    error = 0

def getError():
    global error
    return error

def setError(err):
    global error
    error = err