#!/usr/bin/env python
import os.path
import pygame as pg


def main():
    """
        Show drop zone.
            box, text
        Mouse cursor in rect
            draw drop zone differently
        if mouse in drop zone, and DROPFILE
    """
    going = True
    pg.display.init()
    size = (640, 480)
    screen = pg.display.set_mode(size)
    pg.display.set_caption('Drag an image file onto the drop zone.')


    smaller = 200
    drop_zone = pg.Rect(smaller // 2, smaller //2, 640 - (smaller), 480 - (smaller))
    clock = pg.time.Clock()
    image = None
    in_drop_zone = False

    while going:
        for e in pg.event.get():
            print(e)
            if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                going = False
            elif e.type == pg.MOUSEMOTION:
                if drop_zone.collidepoint(e.pos[0], e.pos[1]) and pg.mouse.get_pressed()[0]:
                    in_drop_zone = True
                else:
                    in_drop_zone = False
            elif e.type == pg.DROPFILE:
                file_extension = os.path.splitext(e.file)[1]
                if file_extension in [".bmp", ".jpg", ".png"]:
                    image = pg.image.load(e.file)
                    pg.display.set_caption(e.file)


        # screen.blit(image, (0, 0))
        if in_drop_zone:
            screen.fill('green', drop_zone)
        else:
            screen.fill('lightgreen', drop_zone)
        pg.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()

