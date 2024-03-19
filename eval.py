
import tkinter as tk
from tkinter import scrolledtext
import sys
import io
from contextlib import redirect_stdout

# Function to execute python code and capture its output
def exec_and_capture(code):
    buffer = io.StringIO()  # Create a buffer to capture output
    with redirect_stdout(buffer):
        try:
            exec(code, globals())  # Execute the code in the global context
        except Exception as e:
            print(f"Error: {e}")  # Print any errors to the buffer
    return buffer.getvalue()  # Return the contents of the buffer

def combine_blocks(lines):
    blocks = []
    block = []

    for line in lines:
        if block:
            if len(line) - len(line.lstrip()) > len(block[0]) - len(block[0].lstrip()):
                block.append(line)
            else:
                blocks.append('\n'.join(block))
                block = [line]
        elif line.endswith(':'):
            block.append(line)
        else:
            blocks.append(line)

    if block:  # Add the last block if it exists
        blocks.append('\n'.join(block))
    
    return blocks

# Adjust the execute_next_line function to work with blocks
def execute_next_line():
    global current_line, code_blocks
    if current_line < len(code_blocks):
        block = code_blocks[current_line]
        output = exec_and_capture(block)
        output_text.insert(tk.END, f">>> {block}\n{output}")
        current_line += 1
    else:
        output_text.insert(tk.END, "End of code.\n")

# Adjust the execute_all function to execute all remaining blocks
def execute_all():
    global current_line, code_blocks
    while current_line < len(code_blocks):
        execute_next_line()

# Setup GUI (Assuming this is part of your existing code setup)
root = tk.Tk()
root.title("Code Executor")

code_text = scrolledtext.ScrolledText(root, height=10)
code_text.pack()

output_text = scrolledtext.ScrolledText(root, height=10)
output_text.pack()

execute_line_button = tk.Button(root, text="Execute Next Line", command=execute_next_line)
execute_line_button.pack()

execute_all_button = tk.Button(root, text="Execute All", command=execute_all)
execute_all_button.pack()

# Assume some example code is provided and processed
example_code = """
print("Hello, World!")
for i in range(3):
    print(f"Loop {i}")
"""
code_text.insert(tk.INSERT, example_code)
# Convert the example code into lines and then into blocks
code_lines = example_code.strip().split('\n')
code_blocks = combine_blocks(code_lines)
current_line = 0  # Keep track of the current block being executed

root.mainloop()
