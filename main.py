import os
import urllib.request
from collections import Counter

url = 'https://pdfobject.com/pdf/sample.pdf'

pdf_file = 'sample.pdf'
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

blocks, block_frequencies, block_probability = data_prep(url)


# implementation of shannon-fano algorithm
class Node:
    def __init__(self, symbol, probability):
        self.symbol = symbol
        self.probability = probability
        self.left = None
        self.right = None
        self.code = ''


# algorithm build on this source: https://www.geeksforgeeks.org/shannon-fano-algorithm-for-data-compression/
# nodes: list of probabilities for the set of symbols
def shannon_fano_algo(node_list):
    # end case for recursion
    if len(node_list) == 1:
        return node_list

    # total prob & comulative prob needed to compare when we are at the center of our nodes list
    total_probability = sum(node.probability for node in node_list)
    cumulative = 0
    split_index = 0

    # find split index
    for i, node in enumerate(node_list):
        cumulative += node.probability
        # try to find half-half (or as close as it gets) of probabilities
        if cumulative >= total_probability / 2:
            split_index = i + 1
            break
    # split to left and right
    left = node_list[:split_index]
    right = node_list[split_index:]

    # recursively go left -> '0' and right -> '1'
    for node in left:
        node.code += '0'
        #print(node.code)
    for node in right:
        node.code += '1'
        #print(node.code)
    return shannon_fano_algo(left) + shannon_fano_algo(right)


# Create nodes for each block - from list block probability - that will be used in shannon-fano algorithm
nodes = [Node(block, prob) for block, prob in block_probability.items()]
# sort nodes by probability -> most probability in the left and least probability on the right
# sort doc: https://docs.python.org/3/howto/sorting.html
nodes.sort(key=lambda x: x.probability, reverse=True)

# generate shannon-fano
coded_nodes = shannon_fano_algo(nodes)
# create a dictionary for the shannon-fano encoding ->
# node.symbol is what we will match with 16-bit block from pdf and encode this symbol with the 'code'
shannon_fano_code = {node.symbol: node.code for node in coded_nodes}
# print statement for dev
#for node in nodes:
#    if node.code != '':
#        print(node.code)

# encode the bit representation -> join it into one string
encoded_bits = ''.join(shannon_fano_code[block] for block in blocks)

# from shannon-fano algorithm we are going to get a bit string -> transform to byte string
with open(compressed_file, 'wb') as file:
    byte_array_encoded = bytearray(int(encoded_bits[i:i + 8], 2) for i in range(0, len(encoded_bits), 8))
    file.write(byte_array_encoded)

# todo: compare the size of the compressed file with the sizes of the same book
# todo: in some other document formats (DjVu etc.).

file_size_original = os.path.getsize(pdf_file)
file_size_compressed = os.path.getsize(compressed_file)


def print_sizes():
    print('Original size: ' + str(file_size_original) + ' bytes')
    print('Compressed size: ' + str(file_size_compressed) + ' bytes')


print_sizes()
