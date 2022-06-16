import pygame
import numpy as np
import random
import os

#base_path = os.path.dirname(__file__)
base_path = os.path.join(os.path.dirname(__file__), "../images/pieces/")

PIPE_IMG = {
    "floor":            pygame.image.load(os.path.join(base_path, "floor.png")),
    "vertical":         pygame.image.load(os.path.join(base_path, "vert.png")),
    "horizontal":       pygame.image.load(os.path.join(base_path, "horiz.png")),
    "cross":            pygame.image.load(os.path.join(base_path, "cross.png")),
    "leftup":           pygame.image.load(os.path.join(base_path, "leftup.png")),
    "leftdown":         pygame.image.load(os.path.join(base_path, "leftdown.png")),
    "rightup":          pygame.image.load(os.path.join(base_path, "rightup.png")),
    "rightdown":        pygame.image.load(os.path.join(base_path, "rightdown.png")),
    "wall":             pygame.image.load(os.path.join(base_path, "wall.png")),
    "startdown":        pygame.image.load(os.path.join(base_path, "startdown.png")),
    "startup":          pygame.image.load(os.path.join(base_path, "startup.png")),
    "startleft":        pygame.image.load(os.path.join(base_path, "startleft.png")),
    "startright":       pygame.image.load(os.path.join(base_path, "startright.png"))
}

class Renderer:
    metadata = {"render_modes": ["human", "rgb_array", "ascii", "descriptive"], "render_fps": 4}
    def __init__(self, window_size=512):
        self.window_size = window_size
        pygame.init()
        pygame.display.init()
        self.window = None
        self.clock = pygame.time.Clock()
        self.board = None
        self.render_mode = "human"
        self.width = None
        self.height = None

    def render(self, board):
        if self.window is None:
            self.height = int((board.height / board.width)*self.window_size)
            self.width = self.window_size
            pygame.init()
            pygame.display.init()
            pygame.display.set_caption("Pipe Dream")
            if self.render_mode == "human":
                self.window = pygame.display.set_mode((self.width, self.height))
            elif self.render_mode == "rgb_array":
                self.window = pygame.Surface(self.window_size)
        if self.clock is None:
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.width, self.height))
        
        canvas.fill((255, 255, 255))
        pix_square_size = (
            self.width // board.width
        )  # The size of a single grid square in pixels
        #pix_square_size = 49

        for y in range(0, board.height):
            for x in range(0, board.width):
                cell = (x*pix_square_size, y * pix_square_size)
                print("cell = ", cell)
                if y == 3 and x == 4:
                    tile_type = "leftup"
                if y == 5 and x == 7:
                    tile_type = "cross"
                if y == 3 and x == 3:
                    tile_type = "startup"
                else:
                    tile_type = "floor"
                self.window.blit(
                    pygame.transform.scale(PIPE_IMG[tile_type], (pix_square_size, pix_square_size)), 
                    cell
                    #(pix_square_size, pix_square_size)
                )
                #pygame.draw.rect(
                #    canvas,
                #    #(255, 0, 0),
                #    (random.randrange(255), 0, 0),
                #    pygame.Rect(
                #        (pix_square_size * x, pix_square_size * y),
                #        (pix_square_size, pix_square_size)
                #    ),
                #)

        if self.render_mode == "human":
            # copy canvas to window
            #self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # handle framerate
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )

    def _render_pipe(self, pipe_type):
        
        raise NotImplementedError
    