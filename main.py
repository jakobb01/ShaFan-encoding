
# find a pdf file of your fav book and read the contents of the file into byte array
with open('invoicesample.pdf', 'rb') as file:
    byte_array = file.read()

print(byte_array)

# change bytes to bits to obtain a representation of the pdf file as a string of bits
string_bits = ''.join(f'{byte:08b}' for byte in byte_array)

print(string_bits)


# split the obtained sequence of bits into blocks of 16, and find the frequency of every possible block,
# and use the obtained frequencies to estimate the probability of all possible blocks of 16 bits


from collections import Counter

blocks = [string_bits[i:i+16] for i in range(0, len(string_bits), 16)]

block_frequencies = Counter(blocks)


# Use the estimated probability distribution to obtain a Shannon-Fano code
# for the blocks of 16 bits.

num_blocks = len(blocks)
# .items() must be in place so it works
block_probability = {block : (frequency/num_blocks) for block, frequency in block_frequencies.items()}


# Use the Shannon-Fano code to encode the bit representation of the pdf
# file of the book.



# Compare the size of the compressed file with the sizes of the same book
# in some other document formats (DjVu etc.).

