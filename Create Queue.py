import json
import os
import pandas as pd
from pathlib import Path
from datetime import datetime


def get_queue_path(what_queue):  # Define paths for completed queues based on user input
    options = {1: "/English and Spanish (SMS)/Completed/",
               2: "/English and Spanish Queue (NO SMS)/Completed/",
               3: "/English (SMS)/Completed/"}
    return options.get(what_queue)

def get_template_path(what_queue): # Define paths for template queues based on user input
    options = {1: "/English and Spanish (SMS)/Template (DO NOT TOUCH)/",
               2: "/English and Spanish Queue (NO SMS)/Template (DO NOT TOUCH)/",
               3: "/English (SMS)/Template (DO NOT TOUCH)/"}
    return options.get(what_queue)

def validate_queue_option(option): # Validate user input for queue option
    return option in [1, 2, 3]

def find_ring_group_name(ring_group_list): # Find the ring group name with the minimum length
    min_length = min(len(group[0]) for group in ring_group_list.index.to_list())
    ring = next(group[0] for group in ring_group_list.index.to_list() if len(group[0]) == min_length)
    return str(ring)

def time_zone(zone): # Map user-input time zone to actual time zone
    time_zones = {"central": "America/Chicago",
                  "pacific": "America/Los_Angeles",
                  "east": "America/New_York",
                  "hawaii": "Pacific/Honolulu",
                  "mountain": "America/Denver"}
    return time_zones.get(zone.lower())

def time_convert(hour): # Convert user-input hour to 24-hour format
    hour = "0"+hour
    t = datetime.strptime(hour, "%I %p").strftime("%H:%M:%S")
    return(t)


def write_json_file(file_path, data): # Write data to a JSON file
    with open(file_path, 'w') as outfile:
        outfile.write(data)


def main():
    run = True
    line = 120 * "_"
    print("\033[1mPlease Enter either of the option below:\033[0m")
    print("Option 1 = English and Spanish (SMS)")
    print("Option 2 = English and SPanish (NO SMS)")
    print("Option 3 = English (SMS)")
    print(line)

    while run == True :
        try:
            
            what_queue = int(input("What is the Queue to create (only input number 1 / 2 / 3): "))

            # Validate user input for the queue option
            while not validate_queue_option(what_queue):
                print("\n")
                print("Not a valid option! Please double-check your input and enter a single-digit number!")
                what_queue = int(input("Please Reenter your Input! What is the Queue to create (only input number 1 or 2 or 3): "))

            # Get the folder path for the queue template
            queue_folder_path = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")

            # Construct paths for completed and template queues
            queue_path_completed = get_queue_path(what_queue)
            queue_path_template = get_template_path(what_queue)

            # Get the directory list of the template queue
            dir_list = queue_folder_path + queue_path_template+ os.listdir(queue_folder_path + queue_path_template)[0]

            try:
                # Read data from the template queue
                with open(dir_list) as f:
                    data = f.read()
                    data = json.loads(data)

                # Normalize the JSON data into a DataFrame
                df = pd.json_normalize(data["steps"])


                # Extract ring group information
                ring_group = df["properties.assignment_parameters.ring_groups.ring_groups_list"].value_counts()
                ring_group_name = find_ring_group_name(ring_group)

                print("The ring group template for the new Queue is extract from:", ring_group_name)
                print("The Folder location is in: ", queue_path_template[1:][:-1])
                print("\033[1mPlease consult with Trinh before changing the template in folder!\033[0m")
                print(line)

                # Extract time-based rules from the DataFrame
                for i,value in df[df["component.name"]=="time_based_rules-NDU4NTVlNz"]["exits"].items():
                    df_time=pd.json_normalize(value[1])
                    for i,value in df_time["condition.ranges"].items():
                        time=pd.json_normalize(value)
                    for i,value in df_time["condition.timezone"].items():
                        time["Time Zone"] = value.split("/")[1].replace("_"," ")

                    # Extract relevant columns from the time data
                    time = time[["days","time.from","time.to","Time Zone"]]
                    List_of_Column = ["Days","From Time","To Time", "Time Zone"]
                    time.columns = List_of_Column


                # Get user input for the new queue
                with open(dir_list) as f:
                    data = f.read()
                print("\n")
                queue_name = input("Please Enter The New Queue name only:")
                from_hour = input("Please Enter Starting Hours (1-12) AM: ")
                end_hour = input(("Please Enter Ending Hours (1-12) PM: "))
                region = input("Please Enter Time Zone from the list (Central/Pacific/East/Mountain/Hawaii): ")


                # Convert user input to required formats
                from_hour = time_convert(from_hour + " AM")
                end_hour = time_convert(end_hour + " PM")
                region = time_zone(region)

                print(line)
                print("\n")
                print("Request information sent for new queue:")
                print("Queue Name: ", queue_name)
                print("Business Hours: ",from_hour + " AM - " + end_hour,"PM")
                print("Queue Region Time: ", region)
                print(line)
                
                # Replace relevant information in the template with user input
                Head = data[:254].replace(ring_group_name, queue_name)
                Tail= data[254:].replace(ring_group_name, queue_name.lower())
                data = Head + Tail
                data = data.replace(str(time["From Time"][0]), from_hour)
                data = data.replace(str(time["To Time"][0]), end_hour)
                data = data.replace("America/"+str(time["Time Zone"][0]),region)

                # Export New File
                new_queue_completed = str(queue_folder_path + queue_path_completed + queue_name + " - v1.json")
                write_json_file(new_queue_completed, data)

            except Exception as e:
                print(f"Error: {e}")
            
            # Read the newly created queue file
            with open(new_queue_completed) as f:
                data = f.read()
                data = json.loads(data)

                # Normalize the JSON data into a DataFrame
                df=pd.json_normalize(data["steps"])


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

            # Count the occurrences of ring groups in the DataFrame
            ring_group=df["properties.assignment_parameters.ring_groups.ring_groups_list"].value_counts()

            print("\n")
            print("Information embedded in new queue file: ")
            print(ring_group)
            print(time)
            print(line)

        # Handle the ValueError exception (non-numeric input)
        except ValueError as e:
            print("\nPlease Enter Number only: ", e, "\n")

        # Prompt user to exit or create a new queue
        finally:
            out = input("Press Y to exit N for a new queue or re-enter: ")
            if out.lower in ["y","yes"]:
                run = False


# Execute main function if the script is run directly
if __name__ == "__main__":
    main()
