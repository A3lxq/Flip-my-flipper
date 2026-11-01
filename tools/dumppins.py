import sys
import xml.etree.ElementTree as ET
ns = {'m': 'http://dummy.com'}
r = ET.parse(sys.argv[1]).getroot()
for p in r.findall('m:Pin', ns):
    sigs = [s.get('Name') for s in p.findall('m:Signal', ns)]
    print(p.get('Position'), p.get('Name').split()[0].split('-')[0].split('/')[0], p.get('Type'), ' '.join(sigs))
