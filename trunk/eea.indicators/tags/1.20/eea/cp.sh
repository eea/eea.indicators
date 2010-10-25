# ./archgenxml -c archgenxml.cfg ims-ng.zuml 
# 
# #rename Products.indicators to eea.indicators
# find indicators/* -type f -print | xargs sed -i 's/Products\.indicators/eea\.indicators/g'
# 
# #in the xml type profiles, replace indicators by eea.indicators
# find indicators/* -type f -print | xargs sed -i 's/>indicators</>eea\.indicators</g'
# 
# #in the profiles.zcml, rename the profile to eea.indicators
# find indicators/* -type f -print | xargs sed -i 's/title=\"indicators\"/title=\"eea\.indicators\"/g'
# 
cp -rf ./ ~/svn/eea.indicators/eea/ 
