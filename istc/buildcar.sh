#!/bin/sh

/Applications/Xcode.app/Contents/Developer/usr/bin/actool --platform macosx --minimum-deployment-target 10.10 --target-device mac --compile ./ $1
