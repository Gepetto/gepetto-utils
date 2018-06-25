#!/bin/bash

# Removes useless folders, and set permissions

set -e

cd /net/pongo/vol/vol_projects/partage_gepetto/Doc

find . -type d -exec chmod 0775 {} \;
find . -type f -exec chmod 0664 {} \;
