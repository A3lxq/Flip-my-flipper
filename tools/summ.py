import sys, glob, re, collections
import xml.etree.ElementTree as ET
ns = {'m': 'http://dummy.com'}
for f in sorted(glob.glob(sys.argv[1] + '/*.xml')):
    r = ET.parse(f).getroot()
    ips = collections.Counter()
    for ip in r.findall('m:IP', ns):
        n = ip.get('InstanceName'); nm = ip.get('Name')
        ips[re.sub(r'\d+$', '', n)] += 1
    keys = ['SPI','I2C','USART','UART','LPUART','SDMMC','USB_OTG_FS','USB_OTG_HS','USB','LTDC','FMC','ADC','DAC','OCTOSPI','QUADSPI','FDCAN','DCMI','COMP','OPAMP']
    print(r.get('RefName'), r.get('Package'), 'IO', r.find('m:IONb', ns).text, 'RAM', r.find('m:Ram', ns).text, 'Flash', r.find('m:Flash', ns).text, {k: ips[k] for k in keys if ips[k]})
