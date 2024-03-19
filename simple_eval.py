import tkinter as tk
from tkinter import messagebox, Label, Entry, StringVar, OptionMenu
import json
import os
import itertools

# Function to simulate response generation
def generate_response(prompt):
    # You would replace this with actual response generation logic
    return ["This is a sample response line 1.",
            "This is a sample response line 2. This line contains an error.",
            "This is a sample response line 3."]

# Function to save feedback to a JSON file
def save_feedback(prompt, response, erroneous_idx, content_type, user_feedback):
    file_path = r"C:\Users\eklav\OneDrive - University of Illinois - Urbana\SP2024_Research\feedback.json"
    data_to_save = {
        "Question": prompt,
        "Response": response,
        "First error observation": erroneous_idx,
        "User Feedback": user_feedback,
        "Content-Type": content_type
    }
    
    existing_data = []
    
    # Check if the file exists and has content; if so, load existing data
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as f:
            existing_data = json.load(f)  # Ensure this loads a list
        # Validate that existing_data is a list before appending
        if isinstance(existing_data, list):
            existing_data.append(data_to_save)  # Append the new data
        else:
            # Handle cases where the data is not a list (shouldn't happen with the correct initial structure)
            existing_data = [data_to_save]
    else:
        existing_data = [data_to_save]  # Start a new list if the file doesn't exist or is empty
    
    # Write the updated list back to the file
    with open(file_path, 'w') as f:
        json.dump(existing_data, f, indent=4)
    
    messagebox.showinfo("Info", "Feedback submitted successfully")

# Function to load the next prompt and response
def load_next_prompt_response():
    try:
        global current_prompt, current_response
        current_prompt, current_response = next(prompts_responses_iterator)
        prompt_text_area.config(state=tk.NORMAL)
        prompt_text_area.delete('1.0', tk.END)
        prompt_text_area.insert(tk.END, current_prompt)
        prompt_text_area.config(state=tk.DISABLED)
        
        response_text_area.config(state=tk.NORMAL)
        response_text_area.delete('1.0', tk.END)
        for idx, line in enumerate(current_response, 1):
            response_text_area.insert(tk.END, f"{idx}: {line}\n")
        response_text_area.config(state=tk.DISABLED)
        
        erroneous_line_entry.delete(0, tk.END)
        feedback_entry.delete(0, tk.END)
        content_type_var.set(content_type_options[0])  # Reset dropdown to default value
    except StopIteration:
        messagebox.showinfo("Info", "All prompts have been processed.")
        root.quit()
# Sample prompts and responses
sample_prompts_responses = [
    ("Prompt 1", generate_response("Prompt 1")),
    ("Prompt 2", generate_response("Prompt 2")),
    # Add more sample prompts and responses as needed
]
# Function to submit feedback, separate from load_next_prompt_response to keep the logic clear
def submit_feedback():
    erroneous_idx = erroneous_line_entry.get()
    user_feedback = feedback_entry.get()
    content_type = content_type_var.get()
    # Validate erroneous line input is a number
    if erroneous_idx.isdigit():
        erroneous_idx = int(erroneous_idx)
    else:
        messagebox.showerror("Error", "Please enter a valid line number.")
        return
    save_feedback(current_prompt, current_response, erroneous_idx, content_type, user_feedback)
# Create an iterator over the sample prompts and responses
prompts_responses_iterator = iter(sample_prompts_responses)

# Main GUI window setup
root = tk.Tk()
root.title("Code Evaluator")

# Text area for prompt
prompt_text_area = tk.Text(root, height=5, wrap="word")
prompt_text_area.pack(fill=tk.BOTH, expand=True)

# Text area for response
response_text_area = tk.Text(root, height=10, wrap="word")
response_text_area.pack(fill=tk.BOTH, expand=True)

# Entry for erroneous line
erroneous_line_label = Label(root, text="Enter the line number with the error first observed:")
erroneous_line_label.pack()
erroneous_line_entry = Entry(root, width=5)
erroneous_line_entry.pack()

# Entry for additional feedback
feedback_label = Label(root, text="Additional Feedback:")
feedback_label.pack()
feedback_entry = Entry(root, width=50)
feedback_entry.pack()

# Dropdown menu for content type
content_type_label = Label(root, text="Content Type:")
content_type_label.pack()
content_type_options = ['coding', 'theory', 'general']
content_type_var = StringVar(root)
content_type_var.set(content_type_options[0])  # default value
content_type_menu = OptionMenu(root, content_type_var, *content_type_options)
content_type_menu.pack()

# Button to submit feedback and load next prompt/response
submit_btn = tk.Button(root, text="Submit Feedback and Load Next", command=lambda: [submit_feedback(), load_next_prompt_response()])
submit_btn.pack(pady=10)

# Load the first prompt and response
load_next_prompt_response()

root.mainloop()

