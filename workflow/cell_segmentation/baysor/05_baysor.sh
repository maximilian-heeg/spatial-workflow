#!/bin/bash
#PBS -q home-yeo
#PBS -N baysor
#PBS -l nodes=1:ppn=8
#PBS -l walltime=48:00:00
#PBS -l pmem=120gb
#PBS -o baysor.log
#PBS -e baysor.err
#PBS -m abe
#PBS -M mheeg@ucsd.edu

# use with qsub -v mol=30

cd /home/mheeg/projects/Merscope/Slide_01/202206_Duodenum_day_7/cell_segmentation/


mkdir -p baysor_30_mol_per_cell

/home/mheeg/bin/Baysor_old/bin/Baysor run -g gene -x global_x -y global_y \
    -z global_z -o baysor_30_mol_per_cell -p \
    -m 30 \
    --n-clusters 8 \
    --save-polygons=geojson \
    -s 5.0 --scale-std=50% \
    --prior-segmentation-confidence 0.7 \
    cellpose_segmentation/transcripts.csv :mask



