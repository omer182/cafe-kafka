#!/bin/sh
# Inputs for the VRM sprite pipeline. Both are freely licensed:
#  - pixiv's VRoid sample character, VRM Public License 1.0 with modification,
#    redistribution and commercial use allowed and no credit required
#  - VRM Add-on for Blender (MIT)
set -e
cd "$(dirname "$0")"
curl -fsSL -o pixiv-sample.vrm https://raw.githubusercontent.com/vrm-c/vrm-specification/master/samples/VRM1_Constraint_Twist_Sample/vrm/VRM1_Constraint_Twist_Sample.vrm
curl -fsSL -o ../blender/addon.zip https://github.com/saturday06/VRM-Addon-for-Blender/releases/download/v4.10.5/VRM_Addon_for_Blender-Extension-4_10_5.zip
