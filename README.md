![image](https://github.com/kend95/talkdesk-JSON-modifier/assets/110085720/4397b700-5146-486f-81fe-9dbce8364903) 

**Background**

Every call queue or phone line created using the **Talkdesk Studio System** will often be reused for different purposes while keeping the original route and logic. However, other elements must change
to accommodate new needs as the company receives more contracts with new clients. Replacing the elements (variable) using Talkdesk Studio's current version is limited by using the search box from Talkdesk.
Searching the specific component or route within the Takdesk Studio limits the search function to replace one element one at a time, and a call queue can have anywhere from 5 to 10 elements, with each element 
needing to be replaced 5-10 times repeatedly. This creates repeatable mistakes and often frustrates the caller and end-user for receiving the wrong call and call-back message.

Since several people are designing the call queue and trying to complete each phone line within the day, a queue tester is needed to dedicate their time to check manually, which will take time and resource
eliminate the errors of elements before publishing the call queue.

![image](https://github.com/kend95/talkdesk-JSON-modifier/assets/110085720/a58a3317-8b7d-47bd-8d02-ac423dd7c9d0)

(A visual representation of a typical queue flow creation. This is taken from Talkdesk and hold no private information from the company the application was developed for use)

**For example:**

An agent using the phone line represented as Company A is routed to a Company A employee. However, the call queue was not connected to Company A due to the wrong element existing within the call queue system.

Or

An employee from Company B is calling the phone line, but the Agent does not pick up the call because the dedicated phone line for Company B is working but is not designated due to language different.

Or

The dedicated phone line indicated the wrong hour and region of operation, which made all callers unable to make the call due to different time zones. If an employee makes a phone call expecting 5 PM PST, but
the agent company already closed at 5PM EST.

The purpose of this repo is to take a standardized call queue design, copy the unstructured JSON file and exported from Talkdesk Studio to modify the specific elements such as:

**1. Language**

**2. Type of text message (SMS, non-SMS)**
   
**4. Date & Hours & Region**
   
**6. Subject**

and replace with new information suit the need of the business operation.


**Result:**

By using Create Queue Application, this eliminate the role of queue tester and allow the call queue to be free of error (100% accuracy). The queue designer is now able to focus on creating the queue without worrying
about creating mistake or even standardize the process of developing call queue.

(This Project was developed by me, but i do not have any formal education with computer science background. So there is certainly better way to do this, but I was on a time crunch and need to make it 
work as fast as possible with no guidance. However, please feel free to let me know if there is any fix that need to be done as i am always looking to learn more everyday.)

My Current email is: trinh_dang50@outlook.com
