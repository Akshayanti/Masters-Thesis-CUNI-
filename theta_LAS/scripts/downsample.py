import argparse
import random

random.seed(1618)

def get_blocks_count(file_name):
    with open(file_name, "r", encoding="utf-8") as infile:
        count = 0
        for line in infile.readlines():
            if line.startswith("# sent_id"):
                count += 1
        return count

def check_constraints(a, b):
    if a < b:
        print("Size of output exceeds size of input. Check the arguments, and try again")
        exit(0)
    elif a == b:
        print("Nothing to do here")
        exit(0)


def organise_as_block(file_contents):
    """Read the incoming file as a block"""
    outset = []
    block = []
    for lines in file_contents:
        if lines != "\n":
            block.append(lines)
        if lines == "\n":
            block.append(lines)
            outset.append(block)
            block = []
    return outset


def generate_output_blocks(filename, output_size):
    contents = open(filename, "r", encoding="utf-8")
    data = organise_as_block(contents)
    contents.close()
    out = random.sample(data, k=output_size)
    return out
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', "--input", type=str, help="Input file that needs to be downsampled, in CONLL-U format", required=True)
    group1 = parser.add_mutually_exclusive_group(required=True)
    group1.add_argument('-n', "--number", type=int, help="Number of instances to downsample to")
    group1.add_argument('-f', "--file", type=str, help="The file whose number of instances the input file should be downsampled to, in CONLLU format")
    parser.add_argument('-o', "--output", type=str, help="Output file to store data in")
    args = parser.parse_args()

    input_size = get_blocks_count(args.input)
    output_size = get_blocks_count(args.file) if args.file else args.number
    check_constraints(input_size, output_size)
    output_data = generate_output_blocks(args.input, output_size)
    
    output_file = args.output if args.output else args.input.strip().split(".")[0] + "_" + str(output_size) + ".conllu"
    with open(output_file, "w", encoding="utf-8") as outfile:
        for blocks in output_data:
            for line in blocks:
                outfile.write(line)
