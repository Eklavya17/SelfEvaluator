import tkinter as tk
from subprocess import Popen, PIPE
import threading
import tempfile
import os

# Tkinter GUI setup
root = tk.Tk()
root.title("Code Executor")
# Frame for code and output
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

code_text = tk.Text(frame, height=10, width=80)
code_text.pack()


sample_code = """for i in range(3):\n    print("Hello World")\n    print(i, "this is value of i")"""
code_text.insert(tk.END, sample_code)


output_text = tk.Text(root, height=20, width=80)
output_text.pack()

def trace_code(code):
    def thread_target():
        try:
            # Create a temporary Python file with the code to trace
            with tempfile.NamedTemporaryFile(delete=False, suffix='.py', mode='w+t') as temp_file:
                temp_file_name = temp_file.name
                temp_file.write(code)
                temp_file.flush()

            # Command to trace Python code execution
            trace_cmd = ["py", "-m", "trace", "-t", temp_file_name]

            # Run the trace command in a separate process
            process = Popen(trace_cmd, stdout=PIPE, stderr=PIPE, text=True)

            # Display the output in the GUI
            for line in iter(process.stdout.readline, ''):
                root.after(1, lambda line=line: output_text.insert(tk.END, line))
            for line in iter(process.stderr.readline, ''):
                root.after(1, lambda line=line: output_text.insert(tk.END, line))

            process.stdout.close()
            process.stderr.close()
            process.wait()
        finally:
            # Cleanup temporary file after execution
            os.unlink(temp_file_name)
        root.after(1, output_text.insert(tk.END, "\n--- Trace Complete ---\n"))

    threading.Thread(target=thread_target).start()

# Button to start tracing
start_button = tk.Button(root, text="Execute code", command=lambda: trace_code("""for i in range(3):\n    print("Hello World")\n    print(i, "this is value of i")"""))
start_button.pack()

root.mainloop()
