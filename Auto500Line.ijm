// This macro tool creates a perfect horiontal line of length 500um, starting from the current cursor position (assuming 51 pixels is 200 um).
// Press ctrl-i (Macros>Install Macros) to reinstall after
// making changes. Double click on the tool icon (red # 5)
// to set which direction you want the line to be created from (based on cursor position, extend to right or left).
// There is more information about macro tools at
//   http://imagej.nih.gov/ij/developer/macro/macros.html#tools

var LeftToRight = true; // assume Left to Right first

macro "Auto500 Tool - Cf20505T59135" {
   getCursorLoc(x, y, z, flags);
//   run("Set Scale...", "distance=1 known=25 pixel=1 unit=um");
   run("Set Scale...", "distance=51 known=200 unit=um");
   //run("Set Scale...", "distance = 51 known = 200 pixel = 1 unit = um");
   len = 500; //scaled version (not in pixels)
   toUnscaled(len); // convert to pixels
   if(LeftToRight){
   makeLine(x,y,x+len,y);
   }
   else{
   makeLine(x,y,x-len,y);
   }
   
}

macro "Auto500 Tool Options" {
   run("Set Scale...", "distance=51 known=200 unit=um");
   LeftToRight = getBoolean("Choose Direction", "Left to Right", "Right to Left");
   
}
