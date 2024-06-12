// This macro tool creates a perfect horiontal line of length 500um, starting from the current cursor position (assuming 51 pixels is 200 um).
// Press ctrl-i (Macros>Install Macros) to reinstall after
// making changes. Double click on the tool icon (red # 5)
// to set which direction you want the line to be created from (based on cursor position, extend to right or left).
// There is more information about macro tools at
//   http://imagej.nih.gov/ij/developer/macro/macros.html#tools

var LeftToRight = true; // assume Left to Right first

macro "Auto500 Tool - Cf20505T0913AT99135" {
   getCursorLoc(x, y, z, flags);
   run("Set Scale...", "distance=51 known=200 unit=um"); // assuming scale is consistent
   len = 500; //scaled version (not in pixels)
   toUnscaled(len); // convert to pixels
   if(LeftToRight){
   makeLine(x,y,x+len,y);
   setTool("line");
   
   }
   else{
   makeLine(x,y,x-len,y);
   setTool("line");
   }
   
}

macro "Auto500 Tool Options" {
   run("Set Scale...", "distance=51 known=200 unit=um");
   LeftToRight = getBoolean("Choose Direction", "Left to Right", "Right to Left");
   
}

macro "Set Tool to Auto500 [q]" { // shortcut to reselect Auto500 Tool and repeat cycle
	setTool("Auto500 Tool");	
}

macro "Measure Current Line [b]"{ // keyboard shortcut to log length 
	run("Measure");
}
