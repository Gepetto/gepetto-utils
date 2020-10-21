#!/bin/bash

tigervncserver -SecurityTypes None
sed -i 's/$(hostname)/localhost/g' /usr/share/novnc/utils/launch.sh
/usr/share/novnc/utils/launch.sh --vnc localhost:5901
