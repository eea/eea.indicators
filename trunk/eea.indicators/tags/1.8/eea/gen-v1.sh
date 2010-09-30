./archgenxml -c archgenxml.cfg ims-v1-ng.zuml --pdb-on-exception=YES

#rename Products.indicators to eea.indicators
find indicators/* -type f -print | xargs sed -i 's/Products\.indicators/eea\.indicators/g'

#in the xml type profiles, replace indicators by eea.indicators
find indicators/* -type f -print | xargs sed -i 's/>indicators</>eea\.indicators</g'

#in the profiles.zcml, rename the profile to eea.indicators
find indicators/* -type f -print | xargs sed -i 's/title=\"indicators\"/title=\"eea\.indicators\"/g'

#in the profiles.zcml, rename the profile to eea.indicators
find indicators/* -type f -print | xargs sed -i 's/profile-Products\.%s:default/profile-eea\.%s:default/g'

./gen.sh
cp -rf ./ ~/svn/eea.indicators/eea/ 

