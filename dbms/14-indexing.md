# Lecture 14: Indexing in DBMS

1. **Indexing** is used to **optimise the performance** of a database by minimising the number of disk accesses required when a query is processed.
    1. The data file sits on disk (inside the file system); disk access is slow, so fetching tuples straight from the data file is slow.
    2. Index = an extra layer on top of the data file (similar in spirit to caching, but not caching).
    3. Data file is also called main file / database file. Disk stores information in blocks (block 1, block 2, ... block n).
    4. Example: 10,000 records (student table), 10 records per block, so 1000 blocks. Roll number is the primary key, so the file is sorted on it.
    5. Query: get student no. 843.
        1. Without index: linear search, or binary search on the whole file (log2 n steps) over all 10,000 records.
        2. With index: search the small index file first (binary search over 1000 entries), get the block pointer (block 841), then go to that block and search inside it (linear or binary).
        3. Search space is reduced, so disk access is reduced: search the index file instead of the disk.
        4. Works because a block is small: once the block is known, searching inside it is cheap.
    6. If every record were indexed, there would be no gain: index search and data file search would cost the same. The index file must be small.
2. The index is a type of **data structure**. It is used to locate and access the data in a database table quickly.
3. Speeds up operation with read operations like **SELECT** queries, **WHERE** clause etc.
    1. Helps in search queries and WHERE clauses: anywhere the data file is accessed to retrieve data (read operations).
    2. Indexing is applied by default on the primary key in implementations (e.g. MySQL).
4. **Search Key**: Contains copy of primary key or candidate key of the table or something else.

    | Search Key | Data Reference |
    |------------|----------------|

    Key points to the Value (Data Reference).
    1. Search key can be any attribute (primary key, candidate key, or other). In the example the search key is roll number.
5. **Data Reference**: Pointer holding the address of disk block where the value of the corresponding key is stored.
    1. It is a block pointer (base pointer of a block), so the block can be accessed directly.
6. Indexing is **optional**, but increases access speed. It is not the primary mean to access the tuple, it is the secondary mean.
    1. Not needed for a very small database; useful when the database is big.
    2. The tuple can be found directly in the data file (linear/binary search); the index is a secondary, more optimised, faster way: search the index, take the block pointer, retrieve the tuples from that block.
7. **Index file is always sorted.**
    1. So binary search can be applied on it, instead of linear search (binary search is always better than linear search).
    2. Even if the data file is unsorted, the index file is kept sorted. An unsorted index gives no benefit.
8. **Indexing Methods**
    1. **Primary Index (Clustering Index)**
        1. A file may have several indices, on different search keys. If the data file containing the records is sequentially ordered, a Primary index is an index whose search key also defines the sequential order of the file.
            1. Applies where the data file is in sequential order: sorted on some one key / attribute.
            2. A file can be sorted on only one attribute at a time (e.g. sorted on roll number means unsorted on age or name).
        2. **NOTE**: The term primary index is sometimes used to mean an index on a primary key. However, such usage is **nonstandard** and **should be avoided**.
            1. Primary index does not mean the search key must be the primary key; it can be a non-primary key too.
        3. All files are ordered sequentially on some search key. It could be Primary Key or non-primary key.
        4. **Dense And Sparse Indices**
            1. **Dense Index**
                1. The dense index contains an index record for every search key value in the data file.
                    1. E.g. roll numbers 1 to 10,000: entries for 1, 2, 3, ... 10,000 are all in the index. The whole data file is indexed.
                2. The index record contains the search-key value and a pointer to the first data record with that search-key value. The rest of the records with the same search-key value would be stored sequentially after the first record.
                3. It needs more space to store index record itself. The index records have the search key and a pointer to the actual record on the disk.
            2. **Sparse Index**
                1. An index record appears for only some of the search-key values.
                    1. E.g. one entry per block: the first search key of each block (1, 11, 21, ...), a gap of 10. No entry for every search key.
                2. Sparse Index helps you to resolve the issues of dense Indexing in DBMS. In this method of indexing technique, a range of index columns stores the same data block address, and when data needs to be retrieved, the block address will be fetched.
                3. Which one is better depends on the case.
        5. Primary Indexing can be based on Data file is sorted w.r.t Primary Key attribute or non-key attributes.
        6. **Based on Key attribute**
            1. Data file is sorted w.r.t primary key attribute.
            2. PK will be used as search-key in Index.
            3. Sparse Index will be formed i.e., no. of entries in the index file = no. of blocks in datafile.
                1. Since the file is sorted and key values are unique, only the first key of each block (block base pointer) is stored; the rest of the block's keys (e.g. 12, 13, ... 20) are found by searching inside the block. No need for dense indexing.
                2. Example: 1000 blocks, so 1000 index entries to access a 10,000-record data file.
        7. **Based on Non-Key attribute**
            1. Data file is sorted w.r.t non-key attribute.
            2. No. Of entries in the index = unique non-key attribute value in the data file.
            3. This is dense index as, all the unique values have an entry in the index file.
                1. Values can repeat (e.g. 1 1 1 2 3 3 3 4 4 4 5), and it is not known how many times a value repeats, so every unique value gets an entry.
            4. E.g., Let's assume that a company recruited many employees in various departments. In this case, clustering indexing in DBMS should be created for all employees who belong to the same dept.
                1. Each unique value is indexed once, with the base pointer of the block where it first occurs.
                2. To search a value: go to the block of its first occurrence, binary search inside that block for the first occurrence, then keep moving to the next records (next blocks if needed) until the value ends; return all of them.
                3. Used where grouping is needed: GROUP BY department (average salary per department, who works in a department), or course-wise enrolled students.
                4. Clustering: records with the same value form a cluster.
            5. Some writers call this non-key case "clustering indexing" and say it is not part of primary indexing. Here: it is still primary indexing. Primary indexing has one criterion only: the data file is sorted on some one search key.
            6. Dense and sparse are just two schemes (ideas) used inside primary indexing: sorted on a key attribute gives sparse; sorted on a non-key attribute gives dense.
        8. **Multi-level Index**
            1. Index with two or more levels.
            2. If the single level index become enough large that the binary search it self would take much time, we can break down indexing into multiple levels.
                1. Index the index: a further (outer) index is built on top of the first-level (inner) index.
                2. Example: data file with roll numbers 100, 101, 102, ...; first-level index has one entry per block (100, 110, 120, ...), pointing to data blocks. The outer index groups them (100, 200, 300, ...), each pointing to an index block of the inner index.
                3. Search 109: outer index finds the 100 entry, which gives the inner index block; the inner index gives the data block of 100; binary search inside the data block finds 109.
                4. Search 209: outer index finds the 200 entry (covers 200 up to before 300), then the inner index block, then the data block, then the record.
                5. Needed when the first-level index table becomes very big (e.g. population of India): the big first-level index is stored on hard disk, and the small outer index table is kept in RAM.

                ![Two-level sparse index](img/lec-14-two-level-sparse-index.png)

    2. **Secondary Index (Non-Clustering Index)**
        1. Datafile is unsorted. Hence, Primary Indexing is not possible.
            1. The data file is sorted on one attribute only (say roll number), so it is unsorted on all other attributes (age, name, address). Indexing on those needs secondary indexing.
            2. Binary search cannot be applied on the data file: the next value after 1 may not be 2 or 3, so values lie scattered across blocks.
        2. Can be done on key or non-key attribute.
            1. Search key can be a key or non-key (candidate key too); it makes no difference.
        3. Called secondary indexing because normally one indexing is already applied.
            1. Usually a primary index already exists on the file (on the sorting key) and a search on another key is needed.
        4. No. Of entries in the index file = no. of records in the data file.
            1. Every search key needs an entry with its block pointer (no sparse possible, as order is unknown).
            2. If the search key values repeat, entries = unique values of the search key; each entry holds a list (linked list, or an extra index level) of all the blocks where that value lies. E.g. 1 is in B1 and B19; 2 is in B2 and B19.
        5. It's an example of Dense index.
            1. Index file is sorted, so binary search can be applied on the index even though the data file is unsorted. Without the index: linear search over all records (e.g. 1 lakh records). With it: binary search over the index, get the block pointer(s). Interview question: what is the benefit of indexing when the data file is unsorted? This is the answer.
            2. Called non-clustering index.
9. **Advantages of Indexing**
    1. Faster access and retrieval of data.
    2. IO is less.
10. **Limitations of Indexing**
    1. Additional space to store index table
    2. Indexing Decrease performance in INSERT, DELETE, and UPDATE query.
