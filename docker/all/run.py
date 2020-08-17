#!/usr/bin/env python

import eigenpy
import hppfcl

print(eigenpy.Quaternion(1, 2, 3, 4).norm())
print(hppfcl.Capsule(2, 3).computeVolume())
