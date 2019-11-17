#!/bin/bash

# Downloads HapMap data, removes non-founders, converts to text format
mkdir -p scratch
cd scratch
wget http://zzz.bwh.harvard.edu/plink/dist/hapmap_r23a.zip
wget -o hapmap.pop http://zzz.bwh.harvard.edu/plink/dist/hapmap.pop
unzip hapmap_r23a.zip
rm hapmap_r23a.zip
plink --bfile hapmap_r23a --out clean_hapmap --make-bed --filter-founders
plink --bfile clean_hapmap --recode transpose --out my_hapmap
rm hapmap_* clean_hapmap.*
