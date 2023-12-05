#! /bin/bash
cd test_runner/systems/verifypn
mkdir build
cd  build
cmake .. -DVERIFYPN_Static=OFF -DVERIFYPN_MC_Simplification=ON 
make
