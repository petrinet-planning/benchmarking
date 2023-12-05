#! /bin/bash
echo Building Downward
bash build_downward.sh

echo Building Planning via Unfolding
bash build_planning-via-unfolding.sh

echo Building VerifyPN
bash build_verifypn.sh
