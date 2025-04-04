---
linkcolor: blue
---
# Assessed Exercise 1: Uxntal and Uxn

## Part A: Uxntal programming exercise: dynamic memory allocation

### Aim

In this coursework you will create a mechanism for dynamic memory allocation in Uxntal, similar to the calls `malloc()` and `free()` in C. 
What this means is that, if you need a certain amount of memory `n_bytes`, calling `ptr = malloc(n_bytes)` should return a pointer `ptr` to the start of an area of at least that size. When you call `free(ptr)` the memory pointed to by `ptr` should be freed up so it can be reused. In Uxntal this could for example look as follows: 

    #0010 malloc ;ptr1 STA2 ( allocate ptr1, 16 bytes )
    ( use ptr1 )
    #0020 malloc ;ptr2 STA2 ( allocate ptr2, 32 bytes )
    ( use ptr2 )
    ;ptr1 LDA2 free ( free ptr1, 16 bytes )
    #40 malloc ;ptr3 STA2 ( allocate ptr3, 64 bytes )
    ( use ptr3 )
    ;ptr2 LDA2 free ( free ptr2, 32 bytes )
    ;ptr3 LDA2 free ( free ptr3, 64 bytes )

As the `free()` call only needs the pointer, the size of the allocated memory must be stored internally. 

In practice, a part of the Uxn VM's memory must be divided into chunks of a fixed size, typically called pages. Depending on how many bytes an allocation needs, one or more pages may be needed, and it is the assumption for this exercise that they are contiguous (i.e. you can only allocate consecutive pages).

You need datastructures to keep track of the free pages and the pages in use. A very common datastructure is a bitmap where every bit indicates if a page is free or allocated, and this is what you should use for the exercise.

For keeping track of the size of allocated memory for each pointer, we will use a map (what Python calls a dictionary).

The problem with allocation and deallocation of contiguous blocks of pages is that the memory gets fragmented: even thought there may be enough free memory in total, there might not be a large enough block left for a given allocation. In this exercise, you do not need to address this problem.

### Suggested approach

#### Creating and manipulating a bitmap

A bitmap is simply an array of bytes which represents the array of pages that makes up the dynamically allocatable memory. A `0` bit means the page is free, a `1` means it's claimed. Given a page index, you need to find the byte in which it occurs, and the find the bit in that byte. You then need to access (get, set or clear) this individual bit. For that, you need to use bit masking and shifting operations. These are the operations `&`, `|`, `<<` and `>>` in Python, in Uxntal the instructions are `AND`,`ORA` and `SFT`.

#### Allocating and de-allocating a number of bytes

- Allocating a number of bytes means first working out how many pages are needed, and then look for this number of contiguous pages in memory, using the bitmap. The result of the allocation is that the bitmap contains a contiguous sequence of `1` bits. 
- Dellocating a number of bytes means setting all the corresponding bits in the bitmap to `0`.

### Your task

Your task is:

- to create an equivalent Uxntal implementation which assembles and runs correctly. You don't have to follow the same code structure as the Python reference, but the functional behaviour must be the same, and the Uxntal subroutines must have the following signature:

        <size in bytes> malloc
        <16-bit address> <size in bytes> free

    - You must define `PAGE_SZ` , `N_PAGES` and `VMEM_START` as constants in the program, this has been done in the skeleton code.

    - `malloc` returns a pointer to the allocated area, i.e. a 16-bit unsigned number which is a valid address in Uxntal main memory, or `0` if the allocation failed.
    - `free` always succeeds and returns nothing
    - You *must* use a bitmap with the following low-level API
            
            <byte-sized index> get_bit ( returns 1 or 0 )
            <byte-sized index> set_bit ( sets the bit to 1 )
            <byte-sized index> clear_bit ( clears the bit to 0)



     
