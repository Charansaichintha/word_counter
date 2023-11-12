import sys

def count_chars_words_lines(input_text):
    lines = input_text.split('\n')
    num_lines = len(lines)
    num_words = sum(len(line.split()) for line in lines)
    num_chars = sum(len(line) for line in lines)
    return num_lines, num_words, num_chars

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            with open(filename, 'r') as file:
                file_contents = file.read()
        except FileNotFoundError:
            print(f"Error: File not found: {filename}")
            sys.exit(1)
    else:
        # Read from stdin if no filename is provided
        try:
            input_text = sys.stdin.read()
        except KeyboardInterrupt:
            sys.exit(1)

    try:
        num_lines, num_words, num_chars = count_chars_words_lines(file_contents)
        print(f"{num_lines:7} {num_words:7} {num_chars:7} {filename}")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
