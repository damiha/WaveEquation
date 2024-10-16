
# Solving the wave equation

I wanted to practice solving partial differential equations (PDE's)
numerically using the finite difference method. 

**NOTE**: I couldn't really get "Sommerfeld boundary conditions" to work
(I want to avoid reflecting boundaries so that it feels like an infinite water surface)
so I opted for a quick and dirty solution. I just extend the
grid (the grid that is drawn is the centerpiece, and we have 8 surrounding patches).
When the wave travels from the centerpiece to neighboring patches,
the dissipation coefficient increases so the waves die out before they can be reflected
at the boundary. This is not efficient at all but gets the job done. To improve
it, one should choose the grid extension in accordance with the dissipation factor.

# Demo

![Water drops](gifs/water_drops.gif)

![Wave and Obstacles](gifs/linear_wave.gif)

**NOTE**: in order for the finite difference method to work,
the [CFL condition](https://en.wikipedia.org/wiki/Courant%E2%80%93Friedrichs%E2%80%93Lewy_condition) needs to be respected. I underestimated
its importance in the beginning.

