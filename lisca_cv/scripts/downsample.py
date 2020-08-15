import argparse
import random
import kfold


def get_blocks_count(file_name):
    """Get the total number of sentences in the input file"""
    with open(file_name, "r", encoding="utf-8") as infile:
        file_data = infile.readlines()
        count = 0
        for lines in file_data:
            if lines.startswith("# sent_id"):
                count += 1
        return count


def check_constraints(a, b):
    """Check if the downsampling parameters are in range. If not, display error and quit"""
    if a < b:
        print("Size of output exceeds size of input. Check the arguments, and try again")
        exit(0)
    elif a == b:
        print("Nothing to do here")
        exit(0)


def generate_output_blocks(filename, output_size):
    """All conditions are correct, Randomly sample output_size number of instances"""
    contents = open(filename, "r", encoding="utf-8")
    data = kfold.organise_as_block(contents)
    contents.close()
    out = random.sample(data, k=output_size)
    return out


def write_data(output_file, output_block):
    """Iterate through the output_block param to write it in the output_file"""
    file_handle = open(output_file, "w", encoding="utf-8")
    for blocks in output_block:
        for line in blocks:
            file_handle.write(line)
    file_handle.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', "--input", type=str, help="Input file that needs to be downsampled, in CONLL-U format", required=True)
    group1 = parser.add_mutually_exclusive_group(required=True)
    group1.add_argument('-n', "--number", type=int, help="Number of instances to downsample to")
    group1.add_argument('-f', "--file", type=str, help="The file whose number of instances the input file should be downsampled to, in CONLLU format")
    args = parser.parse_args()

    input_size = get_blocks_count(args.input)
    output_size = get_blocks_count(args.file) if args.file else args.number
    check_constraints(input_size, output_size)
    # Seed so that the downsampled data can be reproduced
    random.seed(1618)
    # Use Write Output Method from genre_split.py file
    write_data(args.input+"_"+str(output_size), generate_output_blocks(args.input, output_size))
