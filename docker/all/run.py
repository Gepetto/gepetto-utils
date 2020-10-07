#!/usr/bin/env python

import sys

import eigenpy
import hppfcl
import pinocchio

with open('/dist') as f:
    dist = f.read()


if '20.04' in dist:
    print('*' * 74)
print(sys.version.split()[0])
print(eigenpy.Quaternion(1, 2, 3, 4).norm())
print(hppfcl.Capsule(2, 3).computeVolume())
print(pinocchio.SE3.Identity().inverse())
