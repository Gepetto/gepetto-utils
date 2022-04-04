#!/usr/bin/env python

import sys

import crocoddyl
import curves
import eigenpy
import example_robot_data
import hppfcl
import multicontact_api
import numpy as np
import pinocchio
import tsid

with open("/dist") as f:
    dist = f.read()

if "20.04" in dist:
    print("*" * 74)
print("{: <6s}".format(sys.version.split()[0]))
print(eigenpy.Quaternion(1, 2, 3, 4).norm())
print(hppfcl.Capsule(2, 3).computeVolume())
print(pinocchio.SE3.Identity().inverse())
print(example_robot_data.load("talos").model.nq)
URDF = "/talos_data/robots/talos_left_arm.urdf"
PATH = example_robot_data.robots_loader.getModelPath(URDF)
print(tsid.RobotWrapper(PATH + URDF, [PATH], False).na)
print(crocoddyl.ActionModelUnicycle().nr)
print(
    curves.bezier(
        np.array([[1, 2, 3], [4, 5, 6], [4, 5, 6], [4, 5, 6], [4, 5, 6]]), 0.2, 1.5
    ).dim()
)
print(multicontact_api.ContactModel().mu)
