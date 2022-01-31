import numpy as np
import pandas as pd
from ..Map.WallTile import WallTile
from ..Map.FloorTile import FloorTile




def test_joining():
    first = [[0,0,0],
             [0,0,0],
             [0,0,0]]
    second = [[1,1,1],
              [1,1,1],
              [1,1,1]]
    print(first)