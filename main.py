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

font = pygame.font.Font(None, 24)

def draw_text_overlay(screen, font):
    texts = [
        "[Space] to start the simulation",
        "[1] for scene 1",
        "[2] for scene 2"
    ]

    for i, text in enumerate(texts):
        text_surface = font.render(text, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect()
        text_rect.topright = (screen.get_width() - 10, 10 + i * 30)  # Positioning
        screen.blit(text_surface, text_rect)

def draw_scalar_grid(screen, grid, obstacles, N_cells, draw_lines=False):

    cell_size = WIDTH // N_cells

    for i in range(N_cells):
        for j in range(N_cells):

            value = grid[i + N_cells, j + N_cells]
            # Map value from -1,1 to 0,255
            color_value = int((value + 1) * 127.5)
            color = (color_value, color_value, color_value) if obstacles[i + N_cells, j + N_cells] == 1 else 0

            pygame.draw.rect(screen, color, (j * cell_size, i * cell_size, cell_size, cell_size))

    # Draw grid lines
    if draw_lines:
        for i in range(N_cells + 1):
            pygame.draw.line(screen, WHITE, (0, i * cell_size), (WIDTH, i * cell_size))
            pygame.draw.line(screen, WHITE, (i * cell_size, 0), (i * cell_size, HEIGHT))

# returns grid_n as grid_nm
# returns grid_np as grid
def advance(c, grid_n, grid_nm, h, dt, dissipation_center, dissipation_outside, obstacles):

    N_cells = len(grid_n) // 3

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

    velocity = (grid_n - grid_nm) / dt

    dissipation_mat = np.ones_like(grid_n) * dissipation_outside
    dissipation_mat[N_cells:2 * N_cells, N_cells : 2 * N_cells] = dissipation_center

    # advance in time
    grid_np = (c**2 * laplacian * dt**2) + 2 * grid_n - grid_nm - (dissipation_mat * velocity * dt)

    grid_np *= obstacles

    return grid_np, grid_n

# "linear waves"
def get_grids_scene_1(N_cells):

    drop_init_h = 1.0
    drop_h_after_step = 0.9

    grid_nm = np.zeros((3 * N_cells, 3 * N_cells))
    grid_nm[:, 1 + N_cells] = drop_init_h

    grid_n = np.zeros((3 * N_cells, 3 * N_cells))
    grid_n[:, 1 + N_cells] = drop_h_after_step

    # 1 where free, 0 where obstacle
    obstacles = np.ones_like(grid_n)

    gap_width = 10
    half = N_cells // 2

    obstacle_width = 5
    obstacle_x_pos = 30

    obstacles[0 : N_cells + half - gap_width // 2, N_cells + obstacle_x_pos : N_cells + obstacle_x_pos + obstacle_width] = 0
    obstacles[N_cells + half + gap_width // 2:, N_cells + obstacle_x_pos: N_cells + obstacle_x_pos + obstacle_width] = 0

    return grid_n, grid_nm, obstacles

# "circular waves"
def get_grids_scene_2(N_cells):

    drop_size = 2
    drop_init_h = 1.0
    drop_h_after_step = 0.9

    drop_start_idx = (3 * N_cells) // 2 - (3 * drop_size) // 2

    offset = 20

    grid_nm = np.zeros((3 * N_cells, 3 * N_cells))
    grid_nm[drop_start_idx:(drop_start_idx + drop_size), drop_start_idx - offset:(drop_start_idx + drop_size) - offset] = drop_init_h
    grid_nm[drop_start_idx:(drop_start_idx + drop_size), drop_start_idx + offset:(drop_start_idx + drop_size) + offset] = drop_init_h


    grid_n = np.zeros((3 * N_cells, 3 * N_cells))
    grid_n[drop_start_idx:(drop_start_idx + drop_size), drop_start_idx - offset:(drop_start_idx + drop_size) - offset] = drop_h_after_step
    grid_n[drop_start_idx:(drop_start_idx + drop_size), drop_start_idx + offset:(drop_start_idx + drop_size) + offset] = drop_h_after_step

    obstacles = np.ones_like(grid_n)

    return grid_n, grid_nm, obstacles

def main():

    N_cells = 100

    grid_n, grid_nm, obstacles = get_grids_scene_1(N_cells)

    running = True
    clock = pygame.time.Clock()

    simulation_started = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    simulation_started = True

                if event.key == pygame.K_1:
                    simulation_started = False
                    grid_n, grid_nm, obstacles = get_grids_scene_1(N_cells)

                if event.key == pygame.K_2:
                    simulation_started = False
                    grid_n, grid_nm, obstacles = get_grids_scene_2(N_cells)

        screen.fill(BLACK)

        if simulation_started:
            grid_n, grid_nm = (
                advance(0.25, grid_n, grid_nm, h = 1 / N_cells, dt = 1 / 120, dissipation_center = 0, dissipation_outside=0.01, obstacles=obstacles))

            draw_scalar_grid(screen, grid_n, obstacles, N_cells)
        else:
            draw_scalar_grid(screen, np.zeros_like(grid_n), obstacles, N_cells)


        draw_text_overlay(screen, font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()