# Don't use libphidgets22 since it's stupid and resets the state of all outputs
# on open and close.
wget https://www.phidgets.com/downloads/phidget21/libraries/linux/libphidget/libphidget_2.1.8.20170607.tar.gz
tar xf libphidget_2.1.8.20170607.tar.gz
cd libphidget-2.1.8.20170607
./configure --prefix="${HOME}/phidgets"
make
make install
cd ..
./build.sh
mkdir "${HOME}/phidgets/bin"
cp phidgets-relay "${HOME}/phidgets/bin"
LD_LIBRARY_PATH="${HOME}/phidgets/lib" "${HOME}/phidgets/bin/phidgets-relay" 109237 2 1
