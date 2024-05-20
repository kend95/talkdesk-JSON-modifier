import json
import pandas as pd
import pathlib
from pathlib import Path
import os
import tkinter as tk
from tkinter import Text, Scrollbar

def on_exit():
    root.destroy()

def check_queue():
    try:
        
        path = str(os.path.realpath(__file__)).replace("\\", "/").replace("/Queue Checker.pyw","/Queue to Check/")
        dir_list = os.listdir(path)[0]

        with open("Queue to Check/" + dir_list) as f:
            data = f.read()
            data = json.loads(data)

        df = pd.json_normalize(data["steps"])
        ring_group = df["properties.assignment_parameters.ring_groups.ring_groups_list"].value_counts()

           # Extract time-based rules from the DataFrame
        for i,value in df[df["component.name"]=="time_based_rules-NDU4NTVlNz"]["exits"].items():
            df_time=pd.json_normalize(value[1])
            for i,value in df_time["condition.ranges"].items():
                time=pd.json_normalize(value)
            for i,value in df_time["condition.timezone"].items():
                time["Time Zone"] = value.split("/")[1].replace("_"," ")

        pd.set_option('max_colwidth', None)
        
        
        time = time[["days","time.from","time.to","Time Zone"]]
        List_of_Column = ["Days","From Time","To Time", "Time Zone"]
        time.columns = List_of_Column
        
        result = "\n" + f"File in Folder: {dir_list}\n" + 70 * "_" + "\n" + \
                 "List of ring group in the studio:\n" + str(ring_group) + "\n" + 70 * "_" + "\n" + \
                 "Date and Time Zone:\n" + "\n"+ str(time.iloc[:,1:]) + "\n" + str(time.iloc[:,:1])+ "\n" + 70 * "_"
                 

        text_output.config(state=tk.NORMAL)
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, result)
        text_output.config(state=tk.DISABLED)

    except Exception as e:
        result = f"Error: {e}"
        text_output.config(state=tk.NORMAL)
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, result)
        text_output.config(state=tk.DISABLED)

# Create main window
root = tk.Tk()
root.title("Queue Checker App")

# Create a Text widget and a Scrollbar to display the output
text_output = Text(root, wrap="word", height=22, width=70, state=tk.DISABLED)
scrollbar = Scrollbar(root, command=text_output.yview)
text_output.config(yscrollcommand=scrollbar.set)
text_output.pack(side=tk.LEFT, padx=10, pady=10)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a button to run the check_queue function and place it at the bottom
check_button = tk.Button(root,
                         height=18,
                         width= 20,
                         anchor="center",
                         text="Check Queue", command=check_queue)

check_button.pack(side="top", anchor="center", pady=5)
# check_button.pack(side=tk.BOTTOM, pady=10)

exit_button = tk.Button(root, height=5, width=20,text="Exit",command=on_exit)
exit_button.pack(side="top", anchor="center", pady=5)

# Run the Tkinter event loop
root.mainloop()
