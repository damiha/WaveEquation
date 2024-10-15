import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wave Equation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def draw_scalar_grid(screen, grid, draw_lines=False):
    N_cells = grid.shape[0]
    cell_size = WIDTH // N_cells

    for i in range(N_cells):
        for j in range(N_cells):
            value = grid[i, j]
            # Map value from -1,1 to 0,255
            color_value = int((value + 1) * 127.5)
            color = (color_value, color_value, color_value)

            pygame.draw.rect(screen, color, (j * cell_size, i * cell_size, cell_size, cell_size))

    # Draw grid lines
    if draw_lines:
        for i in range(N_cells + 1):
            pygame.draw.line(screen, WHITE, (0, i * cell_size), (WIDTH, i * cell_size))
            pygame.draw.line(screen, WHITE, (i * cell_size, 0), (i * cell_size, HEIGHT))

# returns grid_n as grid_nm
# returns grid_np as grid
def advance(c, grid_n, grid_nm, h, dt):

    # calculate laplacian
    grid_xp = np.zeros_like(grid_n)
    grid_xp[:, :-1] = grid_n[:, 1:]

    grid_xm = np.zeros_like(grid_n)
    grid_xm[:, 1:] = grid_n[:, :-1]

    grid_yp = np.zeros_like(grid_n)
    grid_yp[:-1, :] = grid_n[1:, :]

    grid_ym = np.zeros_like(grid_n)
    grid_ym[1:, :] = grid_n[:-1, :]

    laplacian = (grid_xp + grid_xm + grid_yp + grid_ym - 4 * grid_n) / (h**2)

    # advance in time
    grid_np = (c**2 * laplacian * dt**2) + 2 * grid_n - grid_nm

    return grid_np, grid_n

def main():
    N_cells = 100

    drop_size = 2
    drop_init_h = 1.0
    drop_h_after_step = 0.9

    drop_start_idx = N_cells // 2 - drop_size // 2

    grid_nm = np.zeros((N_cells, N_cells))
    grid_nm[drop_start_idx:(drop_start_idx + drop_size), drop_start_idx:(drop_start_idx + drop_size)] = drop_init_h

    grid_n = np.zeros((N_cells, N_cells))
    grid_n[drop_start_idx:(drop_start_idx + drop_size), drop_start_idx:(drop_start_idx + drop_size)] = drop_h_after_step

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        grid_n, grid_nm = advance(0.25, grid_n, grid_nm, h = 1 / N_cells, dt = 1 / 60)

        draw_scalar_grid(screen, grid_n)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()