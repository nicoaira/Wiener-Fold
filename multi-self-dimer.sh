#!/bin/sh
# This is a comment!


nscripts=4
nsequences=50
nbatches=2000


python3 restore_df.py

for i in $(seq 1 $nscripts)
do
  python3 self-dimer.py $i $nsequences $nbatches &

done
