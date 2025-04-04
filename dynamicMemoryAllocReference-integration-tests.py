#!/usr/bin/env python3

# Dynamic memory allocation using pages and a bitmap
from DynamicMemoryAllocReference import *

# for mem_sz in range(1,55+1):
#     ptr = malloc(mem_sz) # so for 1..16 we have 1 page each; for 17, 18 etc we need to pages 
#     print(mem_sz,': ',ptr)
#     if (mem_sz>=30 and mem_sz<=40 and ptr<N_PAGES):
#         free(ptr)

ok=[False] * 9
def result(n):
    if ok[n]:        
        print('Test ',n,'. passed')
    else:
        print('Test ',n,'. failed')

# Helper function which does malloc/use/free
def test_local_alloc(sz):
    p = malloc(sz)
    memory[p+0]=1
    memory[p+sz-1]=sz
    res = memory[p+0]+memory[p+sz-1]
    free(p)
    return res

# 1. Call test_local_alloc repeatedly for MAX_N_ALLOCS*4 times
# It should not return any error
def integrationTest01():
    ok[1]=True
    for ii in range(1,MAX_N_ALLOCS*4+1):
        res = test_local_alloc(ii*2)
        if not res==ii*2+1:
            ok[1]=False
            print('Failed at ',ii,' with error ',errors[getError()])
            break
        if getError()!=0:
            ok[1]=False
            print('Failed at ',ii,' with error ',errors[getError()])
            break
    result(1)

    reset()

# 2. call malloc MAX_N_ALLOCS+1 times, see if it throws an error on MAX_N_ALLOCS
def integrationTest02():
    for ii in range(1,MAX_N_ALLOCS+1+1):
        ptr = malloc(ii*2)
        if getError()==5:
            if ii == MAX_N_ALLOCS+1:
                ok[2]=True
    if (not ok[2]):
        print('Failed with error ',errors[getError()])
    result(2)

    reset()

# 3. call malloc MAX_N_ALLOCS // 2 times, free every time
def integrationTest03():
    ok[3]=True
    for ii in range(1,MAX_N_ALLOCS // 2+1):
        ptr = malloc(ii*2)
        free(ptr)
        if getError()!=0:
            print('Failed at ',ii,' with error ',errors[getError()])
            ok[3]=False
            break
    result(3)

    reset()

# 4. call malloc with increasing size to see if it correctly returns the null pointer
def integrationTest04():
    ok[4]=True
    sz_tot=0
    for ii in range(1,MAX_N_ALLOCS // 2+1):
        sz = 4**ii
        ptr = malloc(sz)
        sz_tot = sz_tot + sz
        if ptr==0:
            if sz_tot<MAX_ALLOC_SZ:
                print('Failed at ',ii,' with alloc ',sz_tot,' and error ',errors[getError()])
                ok[4]=0
            break
    result(4)

    reset()

# 5. Do the same but free every time (should be the same)
def integrationTest05():
    ok[5]=True
    for ii in range(1,MAX_N_ALLOCS // 2+1):
        sz = 4**ii
        ptr = malloc(sz)    
        if ptr==0:
            if sz<MAX_ALLOC_SZ:
                print('Failed at ',ii,' with alloc ',sz,' and error ',errors[getError()])
                ok[5]=0
            break
        else:
            free(ptr)
    result(5)

    reset()

# 6. As 4 but in reverse order
def integrationTest06():
    ok[6]=True
    n_pages_tot=0
    for ii in range(1,MAX_N_ALLOCS // 2+1):
        sz = MAX_ALLOC_SZ>>ii
        ptr = malloc(sz)
        n_pages = ((sz-1) // PAGE_SZ)+1
        n_pages_tot = n_pages_tot + n_pages
        # print(ptr,sz,sz_tot//PAGE_SZ,N_PAGES)
        if ptr==0:
            if n_pages_tot<N_PAGES:
                print('Failed at ',ii,' with alloc ',n_pages_tot,N_PAGES,' and error ',errors[getError()])
                ok[6]=0
            break
    result(6)

    reset()

# 7. As 5 but in reverse order
def integrationTest07():
    ok[7]=True
    for ii in range(1,MAX_N_ALLOCS // 2+1):
        sz = MAX_ALLOC_SZ>>ii
        ptr = malloc(sz)
        # print(ptr,sz_tot)
        if ptr==0:
            if sz<MAX_ALLOC_SZ and sz>0:
                print('Failed at ',ii,' with alloc ',sz,' and error ',errors[getError()])
                ok[7]=0
            break
        else:
            free(ptr)
    result(7)

    reset()

# 8. Final test, 3 marks
# Allocate, free if the pointer was valid
def integrationTest08():
    n_pages_tot=0
    ok[8]=True
    for ii in range(1,200+1):
        mem_sz = ii*4
        ptr = malloc(mem_sz) # so for 1..16 we have 1 page each; for 17, 18 etc we need two pages
        # print(mem_sz,ptr)
        n_pages = ((mem_sz-1) // PAGE_SZ)+1
        n_pages_tot = n_pages_tot + n_pages
        if getError()!=0: # when we exceed N_PAGES we we expect error 4
            if ((n_pages_tot < N_PAGES) and getError()==4) or getError()!=4: 
                print('Failed at ',ii,' with alloc ',n_pages_tot,N_PAGES,' and error ',errors[getError()])
                ok[8]=False
                break
        if ptr>0:
            if (ii>=20 and ii<=50 or ii>=60 and ii<=100):
                # print('free',ptr)
                free(ptr)
                n_pages_tot = n_pages_tot - n_pages
        else:
            if n_pages_tot < N_PAGES: # means there was another error
                print('Failed at ',ii,' with alloc ',n_pages_tot,N_PAGES,' and error ',errors[getError()])
                ok[8]=False
                break
    result(8)

integrationTest01()
integrationTest02()
integrationTest03()
integrationTest04()
integrationTest05()
integrationTest06()
integrationTest07()
integrationTest08()