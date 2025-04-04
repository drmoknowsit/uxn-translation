
idx = 174
byte_idx = idx >> 3
bit_idx = 7 - idx + (byte_idx<<3)
print("byte_idx",  byte_idx)
print("bit_idx",  bit_idx)