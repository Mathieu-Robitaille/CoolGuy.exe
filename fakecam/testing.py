import cv2
import os
import sys
import pathlib

from itertools import cycle

class A:
    def __init__(self, a):
        self.a = a

    def print(self):
        print(self.a)

class B:
    def __init__(self, a):
        self.a = a

    def print(self):
        super()

print()