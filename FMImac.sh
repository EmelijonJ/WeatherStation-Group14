##!/bin/bash
x="'${1}'"
stor_loc="'${2}'"
berg="'${3}'"
osl="'${4}'"
trond="'${5}'"
osascript -e "tell application \"Terminal\" to do script \"cd $x; python3 $stor_loc\""
sleep 3
osascript -e "tell application \"Terminal\" to do script \"cd $x; python3 $berg\""
osascript -e "tell application \"Terminal\" to do script \"cd $x; python3 $osl\""
osascript -e "tell application \"Terminal\" to do script \"cd $x; python3 $trond\""
osascript -e "tell application \"Terminal\" to do script \"cd $x; $6; $7\""
