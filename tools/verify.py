import re, sys
dump, md = sys.argv[1], sys.argv[2]
pins = {}
for l in open(dump):
    p = l.split()
    pins[p[1]] = (p[2], set(p[3:]))
seen, exti, bad = {}, {}, []
exti_names = {'INT_B','PWR_INT','ESP_HS','SD_CD','LINUX_WAKE','LINUX_PRSNT'} | {f'IRQ_P{i}' for i in range(1,9)}
n = 0
for l in open(md):
    m = re.match(r'\| (\d+) \| (\S+) \| (\S+) \| (.+) \|$', l)
    if not m or m.group(3) == 'Function': continue
    pos, port, fn, sg = m.groups()
    if fn == 'RESERVED': continue
    n += 1
    if port in seen: bad.append(f'duplicate pin {port}')
    seen[port] = fn
    if port not in pins or pins[port][0] != 'I/O': bad.append(f'{port} not I/O')
    elif sg != 'GPIO' and sg not in pins[port][1]: bad.append(f'{port} lacks {sg}')
    elif sg == 'GPIO' and 'GPIO' not in pins[port][1]: bad.append(f'{port} no GPIO')
    if fn in exti_names:
        i = int(re.sub(r'\D', '', port[2:]))
        if i in exti: bad.append(f'EXTI{i} used by {exti[i]} and {fn}')
        exti[i] = fn
print(md.split('/')[-1], n, 'assignments;', 'EXTI lines used:', len(exti), ';', 'PROBLEMS: ' + '; '.join(bad) if bad else 'no problems')
