# The idea of this file is to use the generate avl file and feed it to AVL in order to steer the parameter generation.
#!/bin/bash
CUSTOM_MODEL=$1
DIR_PATH='/home/fremarkus/Documents/avl_automation'

cd 
cd avl3.36/Avl/runs
../bin/avl $CUSTOM_MODEL.avl < $DIR_PATH/avl_steps.txt
echo -e "\n"

##CHECK IF IT ALREADY EXISTS AND DECIDE WHAT YOU WANT TO DO 