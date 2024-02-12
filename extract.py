import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 extract.py <input_image> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

