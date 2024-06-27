import groovy.io.FileType
import java.awt.image.BufferedImage
import qupath.lib.images.servers.ImageServerProvider
import qupath.lib.gui.commands.ProjectCommands

def path = 'C:\\Users\\13107\\Downloads\\test3'
//C:\Users\13107\Downloads\test3
def project = getProject()
def files = new File(path).listFiles()

for (file in files) {
    def imagePath = file.getCanonicalPath()
   def support = ImageServerProvider.getPreferredUriImageSupport(BufferedImage.class, imagePath)
  //println(new File(imagePath).exists())
  def builder = support.builders.get(0)
    //project.addImage(builder)
    entry = project.addImage(builder)
    
    // Set a particular image type
    def imageData = entry.readImageData()
    //imageData.setImageType(ImageData.ImageType.BRIGHTFIELD_H_DAB)
    entry.saveImageData(imageData)
    
    // Write a thumbnail if we can
    var img = ProjectCommands.getThumbnailRGB(imageData.getServer());
    entry.setThumbnail(img)
    
    // Add an entry name (the filename)
    entry.setImageName(file.getName())
    }
print("done")
 

    


//project.addImage(builder)

project.syncChanges()

getQuPath().refreshProject()
