#! /bin/bash
echo Building Downward
bash build_downward.sh

echo Building Planning via Unfolding
bash build_planning-via-unfolding.sh

echo Building VerifyPN
bash build_verifypn.sh

echo Building Val
bash build_val.sh

echo Building ENHSP
bash build_enhsp.sh

echo Building Tapaal GUI
bash build_tapaal_gui.sh
