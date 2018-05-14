#!/bin/sh
### usage:
### 
### this_script asset_catelog_folder
### 
/Applications/Xcode.app/Contents/Developer/usr/bin/actool --platform macosx --minimum-deployment-target 10.10 --target-device mac --compile ./ $1
