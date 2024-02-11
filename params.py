# Colors
RGB_WHITE = (255, 255, 255)
RGB_BLACK = (0, 0, 0)
WHITE = 255
BLACK = 0
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
HIGHLIGHT_COLOR = (0, 255, 0, 128)  # transparent green

# Params
MARK_THRESHOLD = 0.35
WRITE_THRESHOLD = 0.1
FILE_HEADER_BUFFER = 600

# Answer embedder constants
MAX_LENGTH = 510
BLOCK_SIZE = 5
FOOTER = '111'
ALPHABET_TO_BINARY = {
    'A': '000',
    'B': '001',
    'C': '010',
    'D': '011',
    'E': '100',
    ' ': '101',
}
BINARY_TO_ALPHABET = {v: k for k, v in ALPHABET_TO_BINARY.items()}

# Injector/Extractor params
MARGIN = 10
FRAME_THICKNESS = 5
