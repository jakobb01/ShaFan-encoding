
# find a pdf file of your fav book and read the contents of the file into byte array
with open('invoicesample.pdf', 'rb') as file:
    byte_array = file.read()

print(byte_array)

# change bytes to bits to obtain a representation of the pdf file as a string of bits
string_bits = ''.join(f'{byte:08b}' for byte in byte_array)

print(string_bits)


# split the obtained sequence of bits into blocks of 16, and find the frequency of every possible block,
# and use the obtained frequencies to estimate the probability of all possible blocks of 16 bits




# Use the estimated probability distribution to obtain a Shannon-Fano code
# for the blocks of 16 bits.



# Use the Shannon-Fano code to encode the bit representation of the pdf
# file of the book.



# Compare the size of the compressed file with the sizes of the same book
# in some other document formats (DjVu etc.).

