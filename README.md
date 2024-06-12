# CNL

File Directory:

# Auto500Line.ijm 
A macro/tool for the Fiji / imageJ software that automatically creates a horiontal line of length 500 (um) starting from the current cursor position, and extending left / right as the user chooses. 
This file has a few key assumptions:
* The scale factor is .255 um/pixel (51 pixels for 200 um) -> if you wish to delete this, simply delete the line starting with 'setScale' after copying the code
* Line desired is perfectly horizontal (angle 0 with the x-axis)

To include this macro on startup, copy and paste the code into the (bottom of the) StartupMacros.ijm file found in the macros folder - restart Fiji and notice the red 'A5' in the top right. Pressing 'q' selects the macro, and pressing 'b' logs the length of the line under the results tab. 


To include this macro manually (not on startup):  
* first download the 'Auto500Line.ijm' file (found on top right under "..." after selecting 'Auto500Line.ijm' on the left side of current page)
* Move this file into your fiji software by:
* Opening Fiji File Folder - opening macro folder - pasting into macro folder
* On windows, this looked like: fiji-win64 -> Fiji.app -> macros
* In Fiji itself, simply click Plugins -> Macros -> Install -> Select the file


The current file icon is a red 'A5'. The icon must be clicked (darker background than all the other icons) in order to be active. 

# OvalEXAMPLE 
Some sample code given by FIJI (I did not develop it, but can answer questions about it if needed) - it simply creates a circle with radius "radius" centered at the current cursor position. Implementation is identical to the 'Auto500Line.ijm' implementation, outlined below.


Questions/Modifications requested?
Message me on discord: lion27
