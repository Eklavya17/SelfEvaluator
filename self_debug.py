# this is a more complex evaluator which builds on the self-debugger, now what
# I do here is when I get in a response , I run the response in a new temp file
# delete the temp file after each execution, after the execution store the feedback in the JSON file
# if the execution is not successful then the error is passed on to the model api call as well as including 
# a code explanation also generated by the model to be stored in the feedback as well and supplied to the model
from function_obtainer import get_completion, extract_code_blocks,extract_explanations
from only_execute import execute_code
import json



def debugging_loop():
    flag = True
    i = 0
    messages = []
    messages.append({"role": "system", "content": "You are a python programmer, your task is to write python code based on the user query and provide an explanation for any code you write. For any User query, answer all questions in completely and provide the entire code every time , not leaving code blocks blank, every single time a new response is recieved make sure the entirety of the code is there. Since the code that will be executed every time will start from a blank file"})
    new_prompt = ("""Finish the following astronomy coding homework. Explain your code when necessary.
# ASTR 596: FDS Homework 5: Hunting for Exoplanets (Due April 1 at Noon)
# The Kepler satellite has discovered many multi-planet systems. You can download artwork for some of them even at the Exoplanet Travel Bureau
# But is there a system like our own Solar system with 8 planets (sorry Pluto)? In fact, there may be at least one - Kepler 90. This along with most other Kepler planets, were not discovered through radial velocity measurements like our example in class (i.e. that nice parameteric model doesn't apply), but were rather discovered through transits - dips in the light of the star as the planet moves around it.
# You get to find 3 exoplanets in the Kepler-90 system with the techniques in class.
# To get and analyze the Kepler data, you'll need the lightkurve package
# python -m pip install lightkurve --upgrade
# I've included some code to get the light curve, clean it and remove the NaNs, and some outliers (you can judge the wisdom of strong outlier removal when you are hunting for planets), and bin the light curve a little bit in time.

# Hints:
# * lightkurve has a bunch of useful tutorials, in particular this one
# * once you get to a periodogram with lightkurve, find_peaks in scipy can help identify the exoplanet peaks
# * You might find it easier to remove the signal of each planet as you find it and work with the residual light curve to find the next. This isn't strictly necessary if you do the previous steps well, but can be helpful. The tutorials page has a demo.
# * The Exoplanet Archive might be of help

# Happy (planet) hunting!

# import numpy as np
# import astropy.table as at
# import astropy.units as u
# import matplotlib.pyplot as plt
# import lightkurve as lk
# from scipy.signal import find_peaks, find_peaks_cwt

# ### RUN THIS
# lcfs = lk.search_lightcurve('Kepler-90', mission='Kepler').download_all()[:12]

# ### RUN THIS
# def squelch_rednoise(lc):
#     corrected_lc = lc.remove_outliers(sigma_upper=10, sigma_lower=10).normalize().flatten(window_length=101)
#     return corrected_lc

# ### RUN THIS - it will take a while.
# stitched_lc = lcfs.stitch(corrector_func=squelch_rednoise)

# clc = stitched_lc.remove_nans().bin(time_bin_size=15*u.min)
# clc.scatter();
# Q1. First, calculate the periodogram using lightkurve. Use the bls method. Look for planets between 50 and 500 day periods with a grid spacing of 0.01d - this is coarse. Use scipy.signal.find_peaks to identify peaks in the periodogram. Remember to exclude any peaks arising from the Earth's revolution. Plot the periodogram and highlight the peak locations. (25 pts)
# Q2. a. The periodogram function from lightkurve can also get a transit time and peak power using periodogram.transit_time and periodogram.power - you'll want both. Get a sorted list of candidate periods, and print it sorted by peak power. (10 pts)
# Q2. b. Next sort the list of periods from longest to shorted. Check if each period has a period in your list that is either 1/2 or 1/3 the same value. If it is, exclude it. If not keep it. Select the four periods with the highest power between 0 to 100d, 100d and 200d, 200d and 300d and 300d and 400d. (15 pts)
# Q3. Select each peak period from the coarse grid in Q2.b. and then use lightkurve algorithm to refine the period within +/- 5 days, and get the best period. (25 pts)

# Q4. Use lightkurve.fold to plot the folded light curve for each of the best periods in Q3. (25 pts)""")
    # new_prompt = input("Input prompt")
    messages.append({"role": "user", "content": new_prompt})
    feedback_info = []
    while(flag):
        response = get_completion(messages)
        print(response)
        code = extract_code_blocks(response)
        print(code)
        result,stderr = execute_code(code)
        print(result)
        messages.append({"role": "assistant", "content": response})
        if stderr:
            # print(stderr)
            feedback_res = extract_explanations(response)
            if (isinstance(feedback_res, list)):
                feedback = '\n'.join(feedback_res)
            else:
                feedback = feedback_res
            feedback_info.append({
                "index": len(messages) - 1,  # Link to the last message
                "System_feedback": stderr,
                "Model_feedback": feedback
            })
            feedback += stderr
            messages.append({"role": "user", "content": f"this code failed to execute the following is the feedback and the error message it generated {feedback}"})
        else:
            print("No errors in execution. Exiting loop.")
            break
        i += 1
        if (i == 5):
            flag = False

    return messages,feedback_info

messages,feedback_info = debugging_loop()
print( " \n Here are the messages  \n", messages)

def self_save_feedback(messages,feedback_info):
    file_path = r"C:\Users\eklav\OneDrive - University of Illinois - Urbana\SP2024_Research\feedback_self.json"

    feedback_entries = []

    feedback_dict = {item["index"]: item for item in feedback_info}  # Convert feedback_info to a dict for easy lookup

    for i in range(len(messages)):
        if messages[i]['role'] == 'user' and i+1 < len(messages) and messages[i+1]['role'] == 'assistant':
            entry = {
                'Prompt': messages[i]['content'],
                'Response': messages[i+1]['content'],
                'System_feedback': None,
                'Model_feedback': None
            }
            # Check if there is associated feedback info
            if (i+1) in feedback_dict:
                entry['System_feedback'] = feedback_dict[i+1]['System_feedback']
                entry['Model_feedback'] = feedback_dict[i+1]['Model_feedback']
            feedback_entries.append(entry)
    # Load or initialize existing data
    try:
        with open(file_path, 'r') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_data.extend(feedback_entries)  # Append new feedback entries

    # Write the updated list back to the file
    with open(file_path, 'w') as f:
        json.dump(existing_data, f, indent=4)
self_save_feedback(messages, feedback_info)