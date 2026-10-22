import re, json, sys
def chunks(path, span=20):
    out=[]; cur=None
    for line in open(path, encoding='utf-8'):
        m=re.match(r'\[(\d+):(\d{2})(?::(\d{2}))?\]\s*(.*)', line.strip())
        if not m: continue
        a,b,c,txt=m.groups()
        s=int(a)*60+int(b) if c is None else int(a)*3600+int(b)*60+int(c)
        if not txt.strip(): continue
        if cur is None or s-cur[0]>=span: cur=[s,txt.strip()]; out.append(cur)
        else: cur[1]+=' '+txt.strip()
    return out
if __name__=='__main__':
    print(json.dumps(chunks(sys.argv[1]),ensure_ascii=False))
