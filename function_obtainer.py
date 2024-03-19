import tkinter as tk
from tkinter import ttk
import os
from openai import OpenAI
import json
from tkinter import scrolledtext
import sys
import io
from contextlib import redirect_stdout
import re
import openai

# Main application window
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API")
)

def get_completion_2(prompt):
    chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4",
    
    
    )
    return chat_completion.choices[0].message.content

def get_completion(messages):
    chat_completion = client.chat.completions.create(
            messages=messages
            ,
            model="gpt-4",
    
    
    )
    return chat_completion.choices[0].message.content


# x = get_completion("""Finish the following astronomy coding homework. Explain your code when necessary.
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


# prompt = "hi"
# response = get_completion_2(prompt)
# print(response)
# response = get_completion_2("Write me simple python code that has a loop for in range of 3, prints out hello world in one line and in the next prints out i, this is the value of i where i is the value of the loop iterator")
# print(response)
def extract_code_blocks(text):
    # Define the pattern to match Python code blocks
    pattern = r"```python(.*?)```"
    # Use re.DOTALL to match across multiple lines
    matches = re.findall(pattern, text, re.DOTALL)

    # Clean up the matches by stripping leading and trailing whitespace
    code_blocks = [match.strip() for match in matches]

    return code_blocks
# print(extract_code_blocks(response))
def extract_explanations(text):
    # Define the pattern to match Python code blocks, including the delimiters
    pattern = r"```python.*?```"
    # Split the text by the Python code blocks
    non_code_parts = re.split(pattern, text, flags=re.DOTALL)

    # Clean up the non-code parts by stripping leading and trailing whitespace
    explanations = [part.strip() for part in non_code_parts if part.strip()]

    return explanations