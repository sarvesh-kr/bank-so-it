#!/usr/bin/env python3
"""Independent answer checks for the shipped, trusted bank (never run on uploads)."""
import ast, collections, hashlib, ipaddress, itertools, json, math, pathlib, re, sqlite3, subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]

def number(pattern,text):return int(re.search(pattern,text).group(1).replace(',',''))
def array(text):return ast.literal_eval(re.search(r'\[[^\]]*\]',text).group())
def ipv4(text):
    address,prefix=re.search(r'(\d+\.\d+\.\d+\.\d+)/(\d+)',text).groups()
    value=int.from_bytes(bytes(map(int,address.split('.'))),'big');p=int(prefix)
    mask=((1<<32)-1)^((1<<(32-p))-1)
    first=value&mask;last=first+((1<<(32-p))-1)
    return first,last,p
def dotted(value):return '.'.join(map(str,value.to_bytes(4,'big')))

def numerical(q):
    t,f=q['question'],q['family']
    if f=='usable-hosts':return str(len(range(1,(1<<(32-number(r'/(\d+)',t)))-1)))
    if f=='prefix-mask':return dotted(((1<<32)-1)^((1<<(32-number(r'/(\d+)',t)))-1))
    if f=='network-address':return dotted(ipv4(t)[0])
    if f=='broadcast-address':return dotted(ipv4(t)[1])
    if f=='last-host':return dotted(ipv4(t)[1]-1)
    if f=='host-range':return dotted(ipv4(t)[0]+1)+' through '+dotted(ipv4(t)[1]-1)
    if f=='subnet-count':
        child,parent=map(int,re.findall(r'/(\d+)',t));return str(1<<(child-parent))
    if f=='minimum-host-capacity':
        needed=number(r'at least (\d+)',t)
        return '/'+str(max(p for p in range(1,31) if (1<<(32-p))-2>=needed))
    if f=='ipv6-compression':return ipaddress.IPv6Address(re.search(r'of (\S+)\?',t).group(1)).compressed
    if f=='ipv6-subnets':return str(1<<(64-number(r'inside a /(\d+)',t)))
    if f=='ttl':return str(number(r'TTL (\d+)',t)-number(r'after (\d+) routers',t))
    if f=='serialization':return f"{number(r'serializing (\d+) bytes',t)*8/number(r'(\d+) Mbps',t)/1000:g} ms"
    if f=='propagation':
        km=number(r'travels ([\d,]+) km',t);speed=number(r'at ([\d,]+) km/s',t)
        return f'{km/speed*1000:g} ms'
    if f=='bandwidth-delay':return str(number(r'(\d+) Mbps',t)*1000000*number(r'(\d+) ms',t)//1000//8)
    if f=='window-segments':return str(number(r'a (\d+)-byte',t)//number(r'sends (\d+)-byte',t))
    if f=='stop-wait':
        tx=number(r'takes (\d+) ms',t);rtt=number(r'propagation is (\d+) ms',t)
        return f'{100*tx/(tx+rtt):.2f}%'
    if f=='hamming':
        data=number(r'of (\d+) data bits',t);bits=0
        while (1<<bits)<data+bits+1:bits+=1
        return str(bits)
    if f=='nyquist':return str(2*number(r'(\d+) Hz',t)*int(math.log2(number(r'using (\d+) signal levels',t))))
    if f=='fragment-count':
        payload=number(r'has (\d+) bytes of payload',t);header=number(r'a (\d+)-byte header',t);mtu=number(r'MTU (\d+)',t);count=1
        while payload>mtu-header:payload-=((mtu-header)//8)*8;count+=1
        return str(count)
    if f=='service-ports':
        service=re.search(r'for (.*)\?',t).group(1)
        return str({'SSH':22,'SMTP server-to-server':25,'DNS':53,'HTTP':80,'HTTPS over TCP':443}[service])
    if f=='crc-degree':return str(number(r'degree (\d+)',t))
    if f=='parity':return str(re.search(r'to ([01]+) to',t).group(1).count('1')%2)
    if f=='tcp-ack':return str(number(r'number (\d+)',t)+number(r'carries (\d+)',t))
    if f=='recovery-point':return str(number(r'every (\d+) minutes',t))
    if f=='recovery-time':return str(sum(map(int,re.findall(r'(\d+) minutes',t))))
    if f=='availability':return str(round(number(r'for ([\d,]+) minutes',t)*(100-float(re.search(r'with ([\d.]+)%',t).group(1)))/100))
    if f=='triangular-loop':return str(sum(1 for i in range(1,number(r'i = 1 to (\d+)',t)+1) for j in range(1,i+1)))
    if f=='doubling-loop':
        limit=number(r'i < (\d+)',t);i=1;count=0
        while i<limit:i*=2;count+=1
        return str(count)
    if f=='perfect-tree':return str(sum(len(list(itertools.product([0,1],repeat=depth))) for depth in range(number(r'height (\d+)',t)+1)))
    if f=='complete-graph':return str(len(list(itertools.combinations(range(number(r'with (\d+) vertices',t)),2))))
    if f=='stack-trace':
        stack=[]
        for op,val in re.findall(r'(push|pop)\((\d*)\)',t.split('What does')[0]):
            if op=='push':stack.append(int(val))
            else:stack.pop()
        return str(stack.pop())
    if f=='queue-trace':
        queue=collections.deque()
        for op,val in re.findall(r'(enqueue|dequeue)\((\d*)\)',t.split('What does')[0]):
            if op=='enqueue':queue.append(int(val))
            else:queue.popleft()
        return str(queue.popleft())
    if f=='range-sum':
        low,high=map(int,re.search(r'indices (\d+) through (\d+)',t).groups());return str(sum(array(t)[low:high+1]))
    if f=='maximum-subarray':
        a=array(t);return str(max(sum(a[i:j]) for i in range(len(a)) for j in range(i+1,len(a)+1)))
    if f=='bst-inorder':return ', '.join(map(str,sorted(array(t))))
    if f=='selection-pass':
        a=array(t);j=min(range(len(a)),key=a.__getitem__);a[0],a[j]=a[j],a[0];return str(a)
    if f=='linear-probing':
        slots={};size=number(r'(\d+)-slot',t)
        for value in array(t):
            p=value%size
            while p in slots:p=(p+1)%size
            slots[p]=value
        return str(p)
    if f=='heap-child':return str(2*number(r'node at index (\d+)',t)+1)
    if f=='binary-search-depth':
        size=number(r'has (\d+) distinct',t);maximum=0
        for target in range(size):
            low,high,count=0,size-1,0
            while low<=high:
                count+=1;mid=(low+high)//2
                if target==mid:break
                if target<mid:high=mid-1
                else:low=mid+1
            maximum=max(maximum,count)
        return str(maximum)
    if f=='shortest-path':
        edges=collections.defaultdict(list)
        for a,b,w in re.findall(r'([A-Z])→([A-Z]):(\d+)',t):edges[a].append((b,int(w)))
        def paths(node,visited):
            if node=='D':return [0]
            return [weight+tail for other,weight in edges[node] if other not in visited for tail in paths(other,visited|{other})]
        return str(min(paths('A',{'A'})))
    if f=='recursive-calls':
        n=number(r'for f\((\d+)\)',t)
        def calls(x):return 1 if x==0 else 1+calls(x-1)
        return str(calls(n))
    if f=='fcfs-wait':
        now=0;wait=[]
        for burst in array(t):wait.append(now);now+=burst
        return f'{sum(wait)/len(wait):.2f} ms'
    if f in ['page-number','page-offset']:
        page=number(r'page size (\d+) bytes',t);address=number(r'address (\d+)',t)
        return str(address//page if f=='page-number' else address%page)
    if f=='fifo-faults':
        capacity=number(r'with (\d+) initially',t);frames=collections.deque();faults=0
        for value in array(t):
            if value not in frames:
                faults+=1
                if len(frames)==capacity:frames.popleft()
                frames.append(value)
        return str(faults)
    if f=='banker-need':return str(number(r'claim (\d+)',t)-number(r'holds (\d+)',t))
    if f=='page-table-entries':return str((1<<32)//number(r'uses (\d+)-byte pages',t))
    raise AssertionError('No independent numerical checker: '+f)

def sql_answer(text):
    rows=[(int(i),branch,None if value=='NULL' else int(value)) for i,branch,value in re.findall(r'^\((\d+), (\w+), (NULL|-?\d+)\)$',text,re.M)]
    assert rows
    db=sqlite3.connect(':memory:')
    db.executescript('CREATE TABLE accounts(id INTEGER PRIMARY KEY, branch TEXT, balance INTEGER);CREATE TABLE branches(code TEXT PRIMARY KEY);')
    db.executemany('INSERT INTO accounts VALUES(?,?,?)',rows)
    db.executemany('INSERT INTO branches VALUES(?)',[(s,) for s in 'ABCD'])
    sql=re.search(r'(SELECT\b.*;)\s*$',text,re.S).group(1)
    result=db.execute(sql).fetchall();db.close()
    return '; '.join(', '.join('NULL' if value is None else str(value) for value in row) for row in result) if result else '(no rows)'

def fingerprint(q):
    fields={k:q[k] for k in ['id','subject','topic','difficulty','question','options','answer','explanation','kind','family','references']}
    return hashlib.sha256(json.dumps(fields,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def check():
    bank=json.loads((ROOT/'app/src/main/assets/bank.json').read_text())
    from check_network import check_network
    check_network(bank)
    from check_dbms import check_dbms
    dbms_proofs=check_dbms(bank)
    from check_os import check_os
    os_proofs=check_os(bank)
    decisions=json.loads((ROOT/'content/review/retirements.json').read_text())
    baseline=json.loads((ROOT/'content/review/baseline-manifest.json').read_text())
    current={q['id'] for q in bank['questions']}
    assert set(baseline)==(current&set(baseline))|(set(decisions)&set(baseline))
    extra=json.loads((ROOT/'content/review/retired-after-baseline.json').read_text())
    assert set(decisions)<=set(baseline)|set(extra)
    assert not current&set(decisions)
    assert len(current)==len(bank['questions'])
    proofs={**dbms_proofs,**os_proofs};lint=[]
    for q in bank['questions']:
        assert len(q['options'])==len(set(q['options']))==5,q['id']
        assert q['references'] and all(r['url'].startswith('https://') and r['title'] for r in q['references'])
        answer=q['options'][q['answer']];expected=None
        if q['kind']=='worked-drill':expected=numerical(q)
        elif q['kind']=='executed-SQL':expected=sql_answer(q['question'])
        elif q['kind']=='executed-shell':
            script=q['question'].split('\n',1)[1]
            expected=subprocess.check_output(['bash','--noprofile','--norc','-c',script],text=True,env={'PATH':'/usr/bin:/bin','LC_ALL':'C'},timeout=5).rstrip('\n') or '(empty output)'
        elif q['kind']=='executed-python':
            script=q['question'].split('\n',1)[1]
            expected=subprocess.check_output(['python3','-I','-c',script],text=True,timeout=5).rstrip('\n')
        if expected is not None:
            assert answer==expected,(q['id'],answer,expected)
            assert q['options'].count(expected)==1
            proofs[q['id']]={'method':q['kind'],'independent_result':expected}
        if len(q['question'].split())>85:lint.append(q['id']+': long stem')
        wrong=[len(v) for i,v in enumerate(q['options']) if i!=q['answer']]
        if len(answer)>150 and len(answer)>2*max(wrong):lint.append(q['id']+': answer-length cue')
        assert q['explanation'].strip() and len(q['explanation'].split())<=90,q['id']
    assert not lint,lint
    # Numerical facts in otherwise conceptual items are also checked explicitly.
    by_id={q['id']:q for q in bank['questions']}
    facts={'architecture-004':str(int('1010',2)),'architecture-005':format(13,'b'),'architecture-022':str(2**16),'architecture-023':str(64//8),'dw_dm-033':str(4*3*2),'dw_dm-064':f'{30/40*100:g}%','cloud_ai_ml-032':f'{30/(30+10)*100:g}%'}
    for id,value in facts.items():
        q=by_id[id];assert q['options'][q['answer']]==value,(id,value)
        proofs[id]={'method':'independent conceptual calculation','independent_result':value}
    report={'passed':True,'questions':len(bank['questions']),'retired':len(decisions),'independent_answer_checks':len(proofs),'proofs':proofs,'lint':lint}
    (ROOT/'docs/quality-checks.json').write_text(json.dumps(report,indent=2)+'\n')
    return bank,report

if __name__=='__main__':
    b,r=check();print(json.dumps({k:v for k,v in r.items() if k!='proofs'}))
