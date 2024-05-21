#! /bin/bash
cd ./test_runner/systems/tapaal-gui
./gradlew assemble # If this takes longer than a minute, try just calling "gradle assemble" manually from local system without any virtualization

cd ./build/distributions
unzip TAPAAL-4.0-SNAPSHOT.zip

echo Tapaal Executable located at: "./test_runner/systems/tapaal-gui/build/distributions/TAPAAL-4.0-SNAPSHOT/bin/TAPAAL"
