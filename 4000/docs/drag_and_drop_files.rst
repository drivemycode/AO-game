Drag and drop of files with python and pygame
=============================================

pygame 2 has very basic support for dragging and dropping files.

It receives events "DROPFILE" events with a "file" attribute containing the
path to the file dropped. If you drop multiple files on the app it gets multiple
"DROPFILE" events.


If you are familiar with pygame events it's just like this.
::

	if e.type == pg.DROPFILE:
	    print (e.file) # filename


Here's a very basic example that allows you to drop images and sounds on it.

- draws images dropped on it
- plays sounds dropped on it


.. code-block:: python

	#!/usr/bin/env python
	import os.path
	import pygame as pg


	def main():
	    """ Very simple example of using the DROPFILE event type
	        to handle dragging and dropping of files.

	        If an image file is dropped from the file manager we load it,
	        and display it in the window.
	    """
	    going = True
	    pg.init()
	    screen = pg.display.set_mode((640, 480))
	    pg.display.set_caption('Drag an image file onto the window.')
	    clock = pg.time.Clock()
	    image = None

	    while going:
	        for e in pg.event.get():
	            if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
	                going = False
	            elif e.type == pg.DROPFILE:
	                file_extension = os.path.splitext(e.file)[1]
	                if file_extension in [".bmp", ".jpg", ".png"]:
	                    try:
	                        image = pg.image.load(e.file)  # load the image given the file name.
	                        pg.display.set_caption(e.file) # show file name in title bar.
	                        screen.blit(image, (0, 0))
	                        pg.display.flip()
	                    except:
	                        pass
	                if file_extension in [".mp3", ".ogg", ".wav"]:
	                    try:
	                        pygame.mixer.music.load(e.file) # load the music in the file name.
	                        pygame.mixer.music.play()
	                    except:
	                        pass


	        clock.tick(30)

	if __name__ == "__main__":
	    main()



