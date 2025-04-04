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

### Python reference implementation

I provide [a Python reference implementation](https://git.dcs.gla.ac.uk/wim/cans/-/blob/main/AE1-part1-code/DynamicMemoryAllocReference.py?ref_type=heads) of `malloc()` and `free()` as defined in this exercise. This serves as the functional specification. I also provide [an Uxntal code skeleton](https://git.dcs.gla.ac.uk/wim/cans/-/blob/main/AE1-part1-code/dynamic-memory-alloc-skeleton.tal?ref_type=heads) with a suitable structure and helper functions for printing as well as an implementation of the allocation map code. 

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

- to provide a unit test program with unit tests for every subroutine used in your program. I provide [a Python reference implementation](https://git.dcs.gla.ac.uk/wim/cans/-/blob/main/AE1-part1-code/dynamicMemoryAllocReference-unit-tests.py?ref_type=heads) and [an Uxntal implementation](https://git.dcs.gla.ac.uk/wim/cans/-/blob/main/AE1-part1-code/dynamic-memory-alloc-unit-tests.tal?ref_type=heads) which does not contain the actual implementations.
- to provide an integration test program demonstrating that your `malloc()` and `free()` work as expected. I provide [a Python reference implementation](https://git.dcs.gla.ac.uk/wim/cans/-/blob/main/AE1-part1-code/dynamicMemoryAllocReference-integration-tests.py?ref_type=heads) and [an Uxntal implementation](https://git.dcs.gla.ac.uk/wim/cans/-/blob/main/AE1-part1-code/dynamic-memory-alloc-integration-tests.tal?ref_type=heads) which does not contain the actual implementations.

### Marking scheme

Total marks out of 50:

* [2 marks] Identifying information (in the form of comments at the beginning of the program). The first comments identify the program, giving your name and student ID, and saying what the program does. These may be the easiest marks you'll ever get!
* [3 marks] Your status report. State clearly whether the program works. If parts are not working, say so. 
* [5 marks] The bitmap and its low-level API: get-bit, set-bit, clear-bit (Uxntal code)
* [5 marks] Unit tests for the bitmap and its low-level API: get-bit, set-bit, clear-bit, mask_clear, mask_set (Uxntal code)
* [5 marks] Unit tests for alloc_sz_is_free_at_idx, claim_alloc_sz_at_idx, free_alloc_sz_at_idx (Uxntal code)
* [5 marks] The `malloc()` routine (including any auxiliary routines) (Uxntal code)
* [5 marks] The `free()` routine (including any auxiliary routines) (Uxntal code)
* [5 marks] Unit tests for malloc and free (Uxntal code)
* [5 marks] The code assembles and executes
* [10 marks] Integration tests for `malloc` and `free`. 

### What to submit

Please submit a zip file containing two Uxntal files: `dynamic-memory-alloc.tal` and `dynamic-memory-alloc-decl.tal`, and a `README` file or `README.md` file which contains your brief status report (a few hundred words is enough) as a text or markdown file.

The name of the zip file should be `CANS2025-AE1-partA-`*your-student-id*`*.zip`.

Note: if you don't submit exactly what is asked, 2 bands will be deduced as per School policy. 

### Due date

11 April 2025 via the Moodle submission link


     