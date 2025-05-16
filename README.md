# DCT
Disk Capacity Test

![image](https://github.com/user-attachments/assets/9e357ef5-cc8b-4a34-a38a-7fe8e01e1f64)


Project writen in python

Here is a practical and robust Python script to verify the actual size of a disk by writing and reading data across the volume. This is useful for validating suspicious or counterfeit drives that falsely report capacity. The script writes temporary test files in sequential blocks, measures the total writable space, and then removes the test data.

⚠️ Warning: This script can consume the entire free space of the selected disk and should not be run on a system or drive in active use. Use it only on test systems or mounted storage you are validating.

✅ Script Features
Writes test blocks until failure or user-defined limit.

Calculates total successfully written space.

Cleans up after completion (optional).

Uses configurable block size and limit.

script usage: 
python disk_test.py /mnt/testdrive --block-size-mb 50 --max-write-gb 10
Writes 50 MB blocks up to 10 GB on /mnt/testdrive.

Add --no-cleanup to inspect the files afterward.

