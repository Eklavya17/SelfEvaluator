import subprocess
import tempfile
import os


# code = """for i in range(3):\n    print("Hello World")\n    print(f"This is the value of i: {i}") """
def execute_code(code):
    if isinstance(code, list):
        code = '\n'.join(code)
    # Create a temporary Python file with the code
    temp_dir = r"C:\Users\eklav\OneDrive - University of Illinois - Urbana\SP2024_Research"
    with tempfile.NamedTemporaryFile(delete=False, suffix='.py', mode='w+t',encoding='utf-8', dir=temp_dir) as temp_file:
        temp_file_name = temp_file.name
        temp_file.write(code)
        temp_file.flush()
    
    # Run the code and capture output
    result = subprocess.run(["python", temp_file_name], capture_output=True, text=True)
    
    # Cleanup temporary file after execution
    # os.unlink(temp_file_name)
    
    # Return stdout, stderr
    return result.stdout, result.stderr
# result = execute_code(code)
# print(result)