./archgenxml -c archgenxml.cfg ims-ng.zuml 

find indicators/* -type f -print | xargs sed -i 's/Products\.indicators/eea\.indicators/g'

# -name “*.cpp” 
