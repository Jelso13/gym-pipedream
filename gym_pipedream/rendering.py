import pygame
import numpy as np
import random

class Renderer:
    metadata = {"render_modes": ["human", "rgb_array", "ascii", "descriptive"], "render_fps": 4}
    def __init__(self, window_size):
        self.window_size = 512
        pygame.init()
        pygame.display.init()
        self.window = pygame.display.set_mode((self.window_size, self.window_size))
        self.clock = pygame.time.Clock()
        self.board = None
        self.render_mode = "human"

    def render(self, board):
        if self.window is None:
            pygame.init()
            pygame.display.init()
            pygame.display.set_caption("Pipe Dream")
            if self.render_mode == "human":
                self.window = pygame.display.set_mode(self.window_size)
            elif self.render_mode == "rgb_array":
                self.window = pygame.Surface(self.window_size)
        if self.clock is None:
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((512, 512))
        
        canvas.fill((255, 255, 255))
        pix_square_size = (
            512 // board.width
        )  # The size of a single grid square in pixels

        for y in range(0, board.height):
            for x in range(0, board.width):
                cell = (x*pix_square_size, y * pix_square_size)
                pygame.draw.rect(
                    canvas,
                    #(255, 0, 0),
                    (random.randrange(255), 0, 0),
                    pygame.Rect(
                        (pix_square_size * x, pix_square_size * y),
                        (pix_square_size, pix_square_size)
                    ),
                )

        self._target_location = [3,3]
        self._agent_location = [3,3]

        # First we draw the target
        pygame.draw.rect(
            canvas,
            (255, 0, 0),
            pygame.Rect(
                #pix_square_size * self._target_location,
                (3,3),
                (pix_square_size, pix_square_size),
            ),
        )
        # Now we draw the agent
        #pygame.draw.circle(
        #    canvas,
        #    (0, 0, 255),
        #    (self._agent_location) * pix_square_size,
        #    pix_square_size / 3,
        #)

        if self.render_mode == "human":
            # The following line copies our drawings from `canvas` to the visible window
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )
    