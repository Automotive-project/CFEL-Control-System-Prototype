#!/usr/bin/python
"""Display image obtained from Point Grey Camera"""

import numpy as np
import sys
from matplotlib import pyplot as plt

# pylint: disable=C0103

with open(sys.argv[1], "rb") as f:
    image_file = np.fromfile(f, dtype=np.uint8, count=1280*1024)
    image = image_file.reshape((1024, 1280))
# print(image)
plt.imshow(image, cmap='gray')
plt.show()
