# CNL

File Directory:

'Auto500Line.ijm' is a macro/tool for the Fiji / imageJ software that automatically creates a horiontal line of length 500 (um) starting from the current cursor position, and extending left / right as the user chooses. 
This file has a few key assumptions:
* The scale factor is .255 um/pixel (51 pixels for 200 um)
* Line desired is perfectly horizontal (angle 0 with the x-axis)

How to Use: 
* first download the 'Auto500Line.ijm' file (found on top right under "..." after selecting 'Auto500Line.ijm' on the left side of current page)
* Move this file into your fiji software by:
* Opening Fiji File Folder - opening macro folder - pasting into macro folder
* On windows, this looked like: fiji-win64 -> Fiji.app -> macros
* In Fiji itself, simply click Plugins -> Macros -> Install -> Select the file

Alternatively, you could automatically include the macro when you launch Fiji by copy and pasting the code into the (bottom of the) StartupMacros.ijm file found in the macros folder

The current file icon is a red #5. The icon must be clicked (darker background than all the other icons) in order to be active. 

Questions/Modifications requested?
Message me on discord: lion27
