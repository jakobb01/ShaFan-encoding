import os
import urllib.request
from collections import Counter

url = 'https://www.princexml.com/samples/invoice/invoicesample.pdf'

pdf_file = 'book.pdf'
compressed_file = pdf_file + '.compressed.bin'


def data_prep(url):
    # download pdf file
    urllib.request.urlretrieve(url, pdf_file)

    # find a pdf file of your fav book and read the contents of the file into byte array
    with open(pdf_file, 'rb') as file:
        byte_array = file.read()

    # change bytes to bits to obtain a representation of the pdf file as a string of bits
    string_bits = ''.join(f'{byte:08b}' for byte in byte_array)

    # split the obtained sequence of bits into blocks of 16, and find the frequency of every possible block,
    # and use the obtained frequencies to estimate the probability of all possible blocks of 16 bits
    blocks = [string_bits[i:i + 16] for i in range(0, len(string_bits), 16)]
    block_frequencies = Counter(blocks)

    # Use the estimated probability distribution to obtain a Shannon-Fano code
    # for the blocks of 16 bits.
    num_blocks = len(blocks)
    # .items() must be in place so it works
    block_probability = {block: (frequency / num_blocks) for block, frequency in block_frequencies.items()}

    return blocks, block_frequencies, block_probability


# Use the Shannon-Fano code to encode the bit representation of the pdf
# file of the book.


# todo: implement shannon-fano algorithm


# example of the algorithm output
encoded_bits = '01010100001110010101010101111011101000011110001010101010101'
# from shannon-fano algorithm we are going to get a bit string -> transform to byte string
with open(compressed_file, 'wb') as file:
    byte_array_encoded = bytearray(int(encoded_bits[i:i + 8], 2) for i in range(0, len(encoded_bits), 8))
    file.write(byte_array_encoded)

# Compare the size of the compressed file with the sizes of the same book
# in some other document formats (DjVu etc.).

file_size_original = os.path.getsize(pdf_file)
file_size_compressed = os.path.getsize(compressed_file)

print('Original size: ' + str(file_size_original) + ' bytes')
print('Compressed size: ' + str(file_size_compressed) + ' bytes')
