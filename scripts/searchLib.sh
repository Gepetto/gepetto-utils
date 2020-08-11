#!/bin/bash

# This script searches all the .so files in the current directory.
# The first arg is a string contained in the dependencies of the library you are looking for.
# The second arg is a string contained in the dependencies that you want to reject. 
# The script will display the names of the .so files which meet these criteria.
# Ex: searchLib.sh my_lib version_to_avoid

set +e
w=`find . -name "*.so" -print`

for v in $w
do
    #echo $v
    out_v=`basename $v`.txt
    #echo $out_v
    ldd $v  > /tmp/$out_v
    grep -nH $1 /tmp/$out_v | grep -v $2 &> /tmp/test
    if [ -s /tmp/test ]
    then
	echo $v
    fi
done

