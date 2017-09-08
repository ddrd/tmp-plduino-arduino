VERSION=1.1.2
rm dist/PLDuino???-$VERSION.*
cd plduino-arduinoide-package
tar -zcvf ../dist/PLDuinoAVR-$VERSION.tar.gz PLDuinoAVR
tar -zcvf ../dist/PLDuinoESP-$VERSION.tar.gz PLDuinoESP
