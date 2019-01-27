"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense game
[E] ender.prime@gmail.com
[F] tower-defense.py
[V] 02.17.17
"""

from game import *
import pygame

# --------------------------------------------------------------------------------------------------------------------

def main():

    pygame.init()
    game = Game()
    game.new()
    pygame.quit()

# --------------------------------------------------------------------------------------------------------------------
