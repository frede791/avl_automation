# The idea of this file is to use the generate avl file and feed it to AVL in order to steer the parameter generation.
#!/bin/bash
CUSTOM_MODEL=$1
DIR_PATH='/home/fremarkus/avl_automation'
cp $DIR_PATH/$CUSTOM_MODEL.avl /home/fremarkus/avl3.36/Avl/runs/

cd 
cd avl3.36/Avl/runs
../bin/avl $CUSTOM_MODEL.avl < $DIR_PATH/avl_steps.txt
echo "\n"

#After completion move the plot to avl_automation directory 
mv /home/fremarkus/avl3.36/Avl/runs/plot.ps $DIR_PATH/
mv $DIR_PATH/plot.ps $DIR_PATH/$CUSTOM_MODEL.ps

##CHECK IF IT ALREADY EXISTS AND DECIDE WHAT YOU WANT TO DO 