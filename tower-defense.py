"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] tower defense game
[E] ender.prime@gmail.com
[F] tower-defense.py
[V] 01.28.17
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

if __name__ == '__main__': main()
