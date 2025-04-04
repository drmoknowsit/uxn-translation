#!/usr/bin/env python3

# Dynamic memory allocation using pages and a bitmap

from DynamicMemoryAllocReference import *

# We allocate 16 bytes per page
# PAGE_SZ = 16 # in bytes
# We have a total of 256 pages, so we can allocate at most 4kB
# N_PAGES = 1024>>2 
# VMEM_START = 64*1024-PAGE_SZ*N_PAGES

# N_PAGES bits, packed in bytes mean N_PAGES/8 entries, so with the above, the bitmap will take 64 bytes
# 0 means free
# bitmap = [0] * (N_PAGES>>3)


def testMaskClear():
    print("Test for mask_clear(bit_idx)")
    print( mask_clear(0x000) == 0xfe )
    print( mask_clear(0x0001) == 0xfd )
    print( mask_clear(0x0002) == 0xfb )
    print( mask_clear(0x0003) == 0xf7 )
    print( mask_clear(0x0004) == 0xef )
    print( mask_clear(0x0005) == 0xdf )
    print( mask_clear(0x0006) == 0xbf )
    print( mask_clear(0x0007) == 0x7f )
    print( '----')

def testMaskSet():
    print("Test for mask_set(bit_idx)")
    print( mask_set(0x0000) == 0x01 )
    print( mask_set(0x0001) == 0x02 )
    print( mask_set(0x0002) == 0x04 )
    print( mask_set(0x0003) == 0x08 )
    print( mask_set(0x0004) == 0x10 )
    print( mask_set(0x0005) == 0x20 )
    print( mask_set(0x0006) == 0x40 )
    print( mask_set(0x0007) == 0x80 )
    print( '----')

# ( define your tests here )
# ( 1/ test with 8 bytes in different locations with a different bit set )
# ( 2/ test with 8 bytes in different locations with multiple bits set )
# ( In both cases, read bits that are set and not set )
def testGetBit():
    print("Test for get_bit(idx)")
    # bitmap[0x0001] = 0x01 # positions: 16=1,15=0 
    # bitmap[0x0003] = 0x80 # positions: 24=1,25=0 
    # bitmap[0x0004] = 0x02 # positions: 38=1,39=0 
    # bitmap[0x0008] = 0x60 # positions: 65=1,66=1  
    # bitmap[0x000c] = 0x04 # positions: 101=1,102=0 
    # bitmap[0x000d] = 0x20 # position: 106=1,107=0 
    setBitmapA()

    print( get_bit(16)==0 and get_bit(15)==1 )
    print( get_bit(24)==1 and get_bit(25)==0 )
    print( get_bit(38)==1 and get_bit(39)==0 )
    print( get_bit(65)==1 and get_bit(66)==1 )
    print( get_bit(101)==1 and get_bit(102)==0 )
    print( get_bit(106)==1 and get_bit(107)==0 )

    setBitmapB()

    print( get_bit(16)==0 and get_bit(15)==1 )
    print( get_bit(24)==1 and get_bit(25)==1 )
    print( get_bit(38)==1 and get_bit(37)==1 )
    print( get_bit(65)==1 and get_bit(66)==1 )
    print( get_bit(100)==1 and get_bit(101)==1 )
    print( get_bit(106)==1 and get_bit(107)==1 )
    print( '----')

def testClearBit():
    print("Test for clear_bit(idx)")
    clear_bit(15)
    clear_bit(14)
    clear_bit(24)
    clear_bit(25)
    clear_bit(38)
    clear_bit(39)
    clear_bit(65)
    clear_bit(66)
    clear_bit(101)
    clear_bit(102)
    clear_bit(106)
    clear_bit(107)

    print( get_bit(15)==0 and get_bit(14)==0 )
    print( get_bit(24)==0 and get_bit(25)==0 )
    print( get_bit(38)==0 and get_bit(39)==0 )
    print( get_bit(65)==0 and get_bit(66)==0 )
    print( get_bit(101)==0 and get_bit(102)==0 )
    print( get_bit(106)==0 and get_bit(107)==0 )
    print( '----')

def testSetBit():
    print("Test for set_bit(idx)")
    set_bit(15)
    set_bit(14)
    set_bit(24)
    set_bit(25)
    set_bit(38)
    set_bit(39)
    set_bit(65)
    set_bit(66)
    set_bit(101)
    set_bit(102)
    set_bit(106)
    set_bit(107)

    print( get_bit(15) == 1 and get_bit(14) == 1 )
    print( get_bit(24) == 1 and get_bit(25) == 1 )
    print( get_bit(38) == 1 and get_bit(39) == 1 )
    print( get_bit(65) == 1 and get_bit(66) == 1 )
    print( get_bit(101) == 1 and get_bit(102) == 1 )
    print( get_bit(106) == 1 and get_bit(107) == 1 )
    print( '----')

def testAllocSzIsFreeAtIdx():
    print("Test for alloc_sz_is_free_at_idx(idx,alloc_sz)")
# All 0
    print("part1")
    print (alloc_sz_is_free_at_idx(15, 1)==0)
    print (alloc_sz_is_free_at_idx(15, 2)==0)
    print (alloc_sz_is_free_at_idx(15, 4)==0)
    print (alloc_sz_is_free_at_idx(15, 8)==0)
    print (alloc_sz_is_free_at_idx(15, 16)==0)
# Last is 0 because 24 is set
    print("part2")
    print (alloc_sz_is_free_at_idx(16, 1)==1)
    print (alloc_sz_is_free_at_idx(16, 2)==1)
    print (alloc_sz_is_free_at_idx(16, 4)==1)
    print (alloc_sz_is_free_at_idx(16, 8)==1)
    print (alloc_sz_is_free_at_idx(16, 16)==0)
# 11100 because 24 is set
    print("part3")
    print (alloc_sz_is_free_at_idx(17, 1)==1)
    print (alloc_sz_is_free_at_idx(17, 2)==1)
    print (alloc_sz_is_free_at_idx(17, 4)==1)
    print (alloc_sz_is_free_at_idx(17, 8)==0)
    print (alloc_sz_is_free_at_idx(17, 16)==0)
# All one
    print("part4")
    print (alloc_sz_is_free_at_idx(108, 1)==1)
    print (alloc_sz_is_free_at_idx(108, 2)==1)
    print (alloc_sz_is_free_at_idx(108, 4)==1)
    print (alloc_sz_is_free_at_idx(108, 8)==1)
    print (alloc_sz_is_free_at_idx(108, 16)==1)

def testClaimAllocSzAtIdx() : 
    print("Test for claim_alloc_sz_at_idx(idx,alloc_sz)")
    print("part1")
    # claim alloc of 1,2,3,4,5 starting at 0 
    b0=bitmap[0] # stash first 2 bytes 
    b1=bitmap[1]
    bitmap[0]=0
    bitmap[1]=0 # clear the bitmap's first 2 bytes 
    # print(bitmap)
    claim_alloc_sz_at_idx(0x0000, 0x0001) # ( 1000 000 )
    print(hex( bitmap[0]), bitmap[0] == 0x80) 

    claim_alloc_sz_at_idx(0x0001, 0x0002) #  ( 1110 0000 )
    print(hex( bitmap[0]), bitmap[0] == 0xe0 )

    claim_alloc_sz_at_idx(0x0003, 0x0003) #  ( 1111 1100 )
    print(hex(bitmap[0]), bitmap[0] == 0xfc )

    claim_alloc_sz_at_idx(0x0006, 0x0004 ) #  ( 1111 1111 1100 0000 )
    print(hex(bitmap[0]), hex(bitmap[1]),end=' ')
    print(bitmap[0]== 0xff and bitmap[1] == 0xc0)

    claim_alloc_sz_at_idx(0x000a, 0x0005 ) #  ( 1111 1111 1111 1110 )
    print(hex(bitmap[0]),hex(bitmap[1]),end=' ')
    print( bitmap[0]==0xff and bitmap[1] == 0xfe)

    # restore to previous state 
    bitmap[0]=b0
    bitmap[1]=b1

    print("part2")
    # claim alloc
    claim_alloc_sz_at_idx(108, 16)
    # check if region beyond it is free, prints 1
    print (alloc_sz_is_free_at_idx(124, 16)==1)
    # check if region itself is claimed, prints 0
    print (alloc_sz_is_free_at_idx(108, 16)==0)
    
def testFreeAllocSzAtIdx() : 
    print("Test for free_alloc_sz_at_idx(idx,alloc_sz)")
    free_alloc_sz_at_idx(108,16) 
    print (alloc_sz_is_free_at_idx(124, 16)==1)
    print (alloc_sz_is_free_at_idx(108, 16)==1)

def testMalloc():
    global error
    print("Test for malloc(alloc_sz)")

    reset()
    ptr = malloc(MAX_ALLOC_SZ)
    print (ptr!=0)
    free(ptr)
    if error>0:
        print(False)

    reset()
    ptr = malloc(MAX_ALLOC_SZ*2+1)
    print (ptr,getError())
    print ((ptr==0) and getError()==7)

    reset()
    ptr = malloc(0)
    print(ptr==0 and getError()==1)
     
    ptr = malloc(1)
    print (ptr!=0 and getError()==0)

    ptr = malloc(16)    
    free(ptr)
    print(getError()==0)
     


def testFree(): 
    print("Test for free(ptr)")
    reset()
    free(0)
    print(getError()==2)

    reset()
    free(DMEM_START)
    print(getError()==6)

    free(DMEM_START-1)
    print(getError()==2)

    free(64*1024-1)
    print(getError()==6)

    ptr = malloc(16)    
    free(ptr)
    print(getError()==0)


def setBitmapA():
    global bitmap
    bitmap[0x0001] = 0x01 # positions: 16=1,15=0 
    bitmap[0x0003] = 0x80 # positions: 24=1,25=0 
    bitmap[0x0004] = 0x02 # positions: 38=1,39=0 
    bitmap[0x0008] = 0x60 # positions: 65=1,66=1  
    bitmap[0x000c] = 0x04 # positions: 101=1,102=0 
    bitmap[0x000d] = 0x20 # position: 106=1,107=0 

def setBitmapB():
    global bitmap
    
    bitmap[1]= 0x03 # 8
    bitmap[3]= 0xc0 # 24
    bitmap[4]= 0x07 # 32
    bitmap[8]= 0x60 # 64 0110 0000
    bitmap[12]= 0x0e
    bitmap[13]= 0x30
#    print(bitmap)
#    print('----')



# unit tests
testMaskClear()
testMaskSet()
testGetBit()
testClearBit()
testSetBit()
setBitmapB()
print( '----')
testAllocSzIsFreeAtIdx()
testClaimAllocSzAtIdx()
testFreeAllocSzAtIdx()
testMalloc()
testFree()