#!/usr/bin/env python

import sys

import eigenpy
import hppfcl
import pinocchio

print(sys.version.split()[0])
print(eigenpy.Quaternion(1, 2, 3, 4).norm())
print(hppfcl.Capsule(2, 3).computeVolume())
print(pinocchio.SE3.Identity().inverse())
