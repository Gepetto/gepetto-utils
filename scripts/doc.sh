#!/bin/bash

# Removes useless folders, and set permissions

set -e

cd /net/cubitus/projects/Partage_GEPETTO/Doc

find . -type d -exec chmod 0775 {} \;
find . -type f -exec chmod 0664 {} \;
