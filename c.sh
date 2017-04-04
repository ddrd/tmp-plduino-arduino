#!/bin/bash

rm -rf ./dist
mkdir dist

function checksum() {
	echo "SHA-256:`shasum -a 256 $1 | awk '{print \$1}'`"
}

tar -zcvf dist/esptool-plduino-0.4.6-osx.tar.gz esptool-plduino-osx
tar -zcvf dist/esptool-plduino-0.4.6-linux64.tar.gz esptool-plduino-linux64
tar -zcvf dist/esptool-plduino-0.4.6-win32.tar.gz esptool-plduino-win32
tar -zcvf dist/esptool-plduino-0.4.6-linux32.tar.gz esptool-plduino-linux32
cd plduino-arduinoide-package
tar -zcvf ../dist/PLDuinoAVR-1.0.0.tar.gz PLDuinoAVR
tar -zcvf ../dist/PLDuinoESP-1.0.0.tar.gz PLDuinoESP
cd ..

cd dist

ESPTOOL_URL="https:\/\/raw.githubusercontent.com\/ddrd\/tmp-plduino-arduino\/master\/dist"
ESPTOOL_CHECKSUM_WIN32=`checksum esptool-plduino-0.4.6-win32.tar.gz`
ESPTOOL_SIZE_WIN32=`stat -n -f%z esptool-plduino-0.4.6-win32.tar.gz`
ESPTOOL_CHECKSUM_LINUX32=`checksum esptool-plduino-0.4.6-linux32.tar.gz`
ESPTOOL_SIZE_LINUX32=`stat -n -f%z esptool-plduino-0.4.6-linux32.tar.gz`
ESPTOOL_CHECKSUM_LINUX64=`checksum esptool-plduino-0.4.6-linux64.tar.gz`
ESPTOOL_SIZE_LINUX64=`stat -n -f%z esptool-plduino-0.4.6-linux64.tar.gz`
ESPTOOL_CHECKSUM_OSX=`checksum esptool-plduino-0.4.6-osx.tar.gz`
ESPTOOL_SIZE_OSX=`stat -n -f%z esptool-plduino-0.4.6-osx.tar.gz`

BOARDAVR_URL="https:\/\/raw.githubusercontent.com\/ddrd\/tmp-plduino-arduino\/master\/dist"
BOARDAVR_CHECKSUM=`checksum PLDuinoAVR-1.0.0.tar.gz`
BOARDAVR_SIZE=`stat -n -f%z PLDuinoAVR-1.0.0.tar.gz`

BOARDESP_URL="https:\/\/raw.githubusercontent.com\/ddrd\/tmp-plduino-arduino\/master\/dist"
BOARDESP_CHECKSUM=`checksum PLDuinoESP-1.0.0.tar.gz`
BOARDESP_SIZE=`stat -n -f%z PLDuinoESP-1.0.0.tar.gz`

cp ../package_PLDuino_index.json.template package_PLDuino_index.json

function replace() {
	sed -i bak "s/$1/${!1}/g" package_PLDuino_index.json
}

replace "ESPTOOL_URL"
replace "ESPTOOL_CHECKSUM_WIN32"
replace "ESPTOOL_CHECKSUM_LINUX32"
replace "ESPTOOL_CHECKSUM_LINUX64"
replace "ESPTOOL_CHECKSUM_OSX"
replace "ESPTOOL_SIZE_WIN32"
replace "ESPTOOL_SIZE_LINUX32"
replace "ESPTOOL_SIZE_LINUX64"
replace "ESPTOOL_SIZE_OSX"

replace "BOARDAVR_URL"
replace "BOARDAVR_CHECKSUM"
replace "BOARDAVR_SIZE"

replace "BOARDESP_URL"
replace "BOARDESP_CHECKSUM"
replace "BOARDESP_SIZE"
