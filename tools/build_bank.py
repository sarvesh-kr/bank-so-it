#!/usr/bin/env python3
"""Build original concept questions and executable/numerical practice drills."""
import json, random, math, ipaddress, sqlite3, subprocess, collections, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'app/src/main/assets'
rng=random.Random(20261018)
SUBJECTS=[('network','Computer Networks & Cybersecurity',250),('dbms','DBMS & SQL',250),('os','Operating Systems',100),('dsa','Data Structures & Algorithms',250),('linux','Linux & Shell Basics',100)]
ADDITIONAL_SUBJECTS=[('dw_dm','Data Warehousing & Data Mining',65),('cloud_ai_ml','Cloud, AI & ML Basics',65),('se_bank_it','Software Engineering & Banking IT',70)]
questions=[]

def add(subject,topic,difficulty,stem,answer,wrong,explanation,kind='concept',family=None):
    answer=str(answer)
    choices=list(dict.fromkeys([answer]+[str(x) for x in wrong if str(x)!=answer]))
    assert len(choices)>=5,(stem,choices)
    choices=choices[:5]; rng.shuffle(choices)
    n=sum(q['subject']==subject for q in questions)+1
    questions.append(dict(id=f'{subject}-{n:03}',subject=subject,topic=topic,difficulty=difficulty,question=stem,options=choices,answer=choices.index(answer),explanation=explanation,kind=kind,family=family or topic))

def num(s,t,d,q,a,e,f,wr=None):
    if wr is None:
        wr=[a+1,a-1,a*2,a+2,a+3,a+5,a*4,0]
    add(s,t,d,q,str(a),[str(x) for x in wr],e,'worked-drill',f)

for sid,_,_ in SUBJECTS:
    for line in (ROOT/'content'/f'{sid}.txt').read_text().splitlines():
        if not line or line.startswith('#'):continue
        p=line.split('¦'); assert len(p)==9,(sid,len(p),line)
        topic,diff,stem,ans,*rest=p
        add(sid,topic,diff,stem,ans,rest[:4],rest[4])

# Network: 25 distinct calculation/interpretation families, five drills per family.
for k in range(5):
    p=24+k; hosts=2**(32-p)-2
    num('network','Subnetting','Moderate',f'For an ordinary IPv4 /{p} LAN subnet, excluding network and broadcast addresses, how many usable host addresses exist?',hosts,f'Host bits = 32−{p} = {32-p}. Usable hosts = 2^{32-p}−2 = {hosts}. /31 and /32 special cases are not involved.','usable-hosts',[2**(32-p),hosts+1,hosts//2,hosts*2,1])
    net=ipaddress.ip_network(f'192.168.{20+k}.0/{p}')
    mask=str(net.netmask)
    add('network','Subnetting','Moderate',f'Which dotted-decimal mask corresponds to /{p}?',mask,[str(ipaddress.ip_network(f'0.0.0.0/{x}').netmask) for x in range(22,31) if x!=p],f'A /{p} mask has {p} leading one bits; its dotted form is {mask}.','worked-drill','prefix-mask')
    address=f'10.{k+1}.3.{141+k*3}'; pr=25+k%4
    n=ipaddress.ip_interface(f'{address}/{pr}').network
    other=[str(ipaddress.ip_address(int(n.network_address)+v)) for v in [1,2,8,16,32,64]]
    add('network','Subnetting','Moderate',f'What is the network address of {address}/{pr}?',str(n.network_address),other,f'Apply the /{pr} mask to {address}. The containing subnet is {n}, beginning at {n.network_address}.','worked-drill','network-address')
    n=ipaddress.ip_network(f'192.168.{30+k}.64/27')
    add('network','Subnetting','Moderate',f'What is the broadcast address of {n}?',str(n.broadcast_address),[f'192.168.{30+k}.{v}' for v in [64,65,94,96,127]],f'The /27 block contains 32 addresses: .64 through .95. Its last address, {n.broadcast_address}, is broadcast.','worked-drill','broadcast-address')
    n=ipaddress.ip_network(f'172.16.{k+2}.128/{26+k%3}')
    a=str(n.broadcast_address-1)
    add('network','Subnetting','Moderate',f'What is the last usable host address in the ordinary IPv4 subnet {n}?',a,[str(n.broadcast_address),str(n.network_address),str(n.network_address+1),str(n.broadcast_address+1)],f'The broadcast address is {n.broadcast_address}; the immediately preceding address {a} is the last usable host.','worked-drill','last-host')
    new=25+k
    num('network','Subnetting','Moderate',f'How many /{new} subnets fit into a /24 IPv4 network?',2**(new-24),f'{new-24} additional prefix bits create 2^{new-24} = {2**(new-24)} subnets.','subnet-count')
    needed=[25,50,100,200,500][k]; bits=math.ceil(math.log2(needed+2)); ans=32-bits
    add('network','Subnetting','Moderate',f'What is the longest IPv4 prefix that provides at least {needed} usable host addresses in an ordinary LAN subnet?',f'/{ans}',[f'/{x}' for x in range(ans-2,ans+4) if x!=ans],f'Need 2^h−2 ≥ {needed}. The smallest h is {bits}, giving {2**bits-2} hosts and /{ans}.','worked-drill','minimum-host-capacity')
    full=f'2001:0db8:000{k+1}:0000:0000:0000:0000:00a{k}'
    compressed=ipaddress.ip_address(full).compressed
    add('network','IPv6','Moderate',f'Which is the correctly compressed form of {full}?',compressed,[f'2001:db8:{k+1}::a{k}:0',f'2001:db8::{k+1}:a{k}',f'2001:db8:{k+1}:a{k}::',f'2001:db8:{k+2}::a{k}'],f'Remove leading zeroes in hextets and compress the consecutive zero run once: {compressed}.','worked-drill','ipv6-compression')
    parent=[48,52,56,60,62][k]
    num('network','IPv6','Moderate',f'How many /64 IPv6 subnets fit inside a /{parent} allocation?',2**(64-parent),f'There are 64−{parent} = {64-parent} subnet bits, giving 2^{64-parent} = {2**(64-parent)} subnets.','ipv6-subnets')
    ttl=32+k*8; hops=k+3
    num('network','IP forwarding','Easy',f'An IPv4 packet starts with TTL {ttl}. What TTL remains after {hops} routers each decrement it once, with no encapsulation?',ttl-hops,f'TTL decreases once at each forwarding router: {ttl}−{hops} = {ttl-hops}.','ttl')
    size=[500,1000,1500,2000,2500][k]; rate=10
    ans=size*8/rate/1000
    add('network','Transmission','Moderate',f'Ignoring headers and other delays, how long does serializing {size} bytes onto a {rate} Mbps link take?',f'{ans:g} ms',[f'{ans/8:g} ms',f'{ans*8:g} ms',f'{ans*10:g} ms',f'{ans/10:g} ms'],f'Time = bits/rate = {size}×8 / 10,000,000 seconds = {ans:g} ms.','worked-drill','serialization')
    km=100*(k+1); ms=km/200
    add('network','Transmission','Moderate',f'A signal travels {km} km at 200,000 km/s. What is its one-way propagation delay?',f'{ms:g} ms',[f'{ms*2:g} ms',f'{ms/2:g} ms',f'{ms*10:g} ms',f'{ms/10:g} ms'],f'Delay = distance/speed = {km}/200,000 seconds = {ms:g} ms.','worked-drill','propagation')
    mbps=10*(k+1); rtt=20
    num('network','Transport calculations','Moderate',f'Using bandwidth × RTT for TCP window sizing, what is the product in bytes for a {mbps} Mbps link and {rtt} ms round-trip time? Use decimal units.',mbps*1000000*rtt//1000//8,f'{mbps}×1,000,000×0.020 bits ÷ 8 = {mbps*2500} bytes. This is the bandwidth multiplied by RTT.','bandwidth-delay')
    tx=k+1; rt=2*tx*(k+1); util=100*tx/(tx+rt)
    add('network','Transport calculations','Hard',f'A stop-and-wait sender takes {tx} ms to transmit a data frame. Round-trip propagation is {rt} ms; ACK transmission and processing are negligible. What is sender utilization?',f'{util:.2f}%',[f'{util/2:.2f}%',f'{min(100,util*2):.2f}%',f'{100-util:.2f}%','100.00%','5.00%'],f'One cycle takes transmission plus round-trip propagation: {tx}+{rt} ms. Utilization = {tx}/({tx}+{rt})×100 = {util:.2f}%.','worked-drill','stop-wait')
    window=8000*(k+2); payload=1000
    num('network','Transport calculations','Moderate',f'A sender has a {window}-byte usable send window and sends {payload}-byte payload segments. Ignoring other limits, how many full segments may be outstanding?',window//payload,f'Window divided by payload = {window}/{payload} = {window//payload} full segments.','window-segments')
    degree=k+3
    num('network','Error control','Moderate',f'A CRC generator polynomial has degree {degree}. How many CRC remainder bits are appended to a dataword?',degree,f'A generator of degree r uses r remainder/check bits. Here r = {degree}.','crc-degree')
    bitstrings=['1011001','1110000','1010101','1111001','1101001']; b=bitstrings[k]; parity=b.count('1')%2
    add('network','Error control','Easy',f'What bit must be appended to {b} to make the total number of 1 bits even?',str(parity),['0' if parity else '1','Two bits are always required','Parity cannot be computed','The dataword must be inverted'],f'The data contains {b.count("1")} one bits. Add {parity} so the resulting count is even.','worked-drill','parity')
    m=[4,8,16,32,64][k]; r=0
    while 2**r<m+r+1:r+=1
    num('network','Error control','Hard',f'For single-bit-error-correcting Hamming coding of {m} data bits, what is the minimum parity-bit count r satisfying 2^r ≥ m+r+1?',r,f'The smallest r satisfying 2^r ≥ {m}+r+1 is {r}: 2^{r} = {2**r} ≥ {m+r+1}.','hamming')
    band=1000*(k+1); snr=15; capacity=band*4
    band=2000; levels=2**(k+1); capacity=2*band*(k+1)
    num('network','Channel capacity','Hard',f'For an ideal noiseless {band} Hz channel using {levels} signal levels, what is the Nyquist maximum bit rate in bits/s?',capacity,f'Rate = 2B log2(M) = 2×{band}×{k+1} = {capacity} bits/s.','nyquist')
    payload=2000+k*500; mtu=1000; maxpayload=976; count=math.ceil(payload/maxpayload)
    num('network','IP fragmentation','Hard',f'An IPv4 datagram has {payload} bytes of payload and a 20-byte header. It crosses a link with MTU 1000; fragmentation is allowed, with no options. How many fragments are needed?',count,f'Nonfinal fragment payload must be a multiple of 8: floor((1000−20)/8)×8 = 976 bytes. ceil({payload}/976) = {count} fragments.','fragment-count')
    seq=1000+k*1000; data=200+k*100
    num('network','TCP sequence numbers','Moderate',f'A TCP segment starts at sequence number {seq} and carries {data} data bytes, with no SYN or FIN. If all bytes through this segment arrive in order, which ACK number is expected?',seq+data,f'TCP acknowledges the next expected byte: {seq}+{data} = {seq+data}.','tcp-ack')
    protocols=[('SSH',22),('SMTP server-to-server',25),('DNS',53),('HTTP',80),('HTTPS over TCP',443)]; name,port=protocols[k]
    num('network','Service ports','Easy',f'Which is the conventional destination port for {name}?',port,f'The conventional service port for {name} is {port}; servers may be configured to use different ports.','service-ports',[20,21,23,110,143,3389])
    interval=[5,10,15,30,60][k]
    num('network','Recovery planning','Moderate',f'Successful recoverable snapshots are taken every {interval} minutes. If a failure occurs just before the next snapshot and no later logs exist, what is the worst-case lost-work interval in minutes, approximately?',interval,f'The latest recoverable point may be almost one snapshot interval old, so potential loss is approximately {interval} minutes.','recovery-point')
    minutes=10+5*k; verify=5+k; switch=2
    num('network','Recovery planning','Moderate',f'A recovery plan needs {minutes} minutes to restore, then {verify} minutes to validate, then {switch} minutes to switch traffic. With no overlap, what is total restoration time in minutes?',minutes+verify+switch,f'Add the sequential stages: {minutes}+{verify}+{switch} = {minutes+verify+switch} minutes.','recovery-time')
    available=99+k*0.2; total=10000; down=round(total*(100-available)/100)
    num('network','Availability','Moderate',f'A service is observed for 10,000 minutes with {available:g}% availability. How many minutes was it unavailable?',down,f'Unavailable fraction = (100−{available:g})/100. Multiply by 10,000 to obtain {down} minutes.','availability')

# SQL questions: concrete datasets, executed with SQLite; standard SQL where possible.
for variant in range(10):
    rows=[]
    for i in range(5+variant%6):
        branch=['A','A','B','B','C','C','A','C','B','A'][i]
        if i==4+variant%6 and variant%3==1: branch='D'
        balance=None if i==2 or (i>3 and (i+variant)%5==0) else [100,200,150,300,200,50,400,75,125,250][i]+variant*(5+(i%3)*5)
        rows.append((i+1,branch,balance))
    a_values=[v for _,b,v in rows if b=='A' and v is not None]
    null_ids=[i for i,b,v in rows if v is None]
    missing_branches=[b for b in 'ABCD' if not any(r[1]==b for r in rows)]
    db=sqlite3.connect(':memory:')
    db.execute('CREATE TABLE accounts(id INTEGER PRIMARY KEY, branch TEXT, balance INTEGER)')
    db.executemany('INSERT INTO accounts VALUES(?,?,?)',rows)
    db.execute('CREATE TABLE branches(code TEXT PRIMARY KEY)');db.executemany('INSERT INTO branches VALUES(?)',[(x,) for x in 'ABCD'])
    table='accounts(id, branch, balance):\n'+'\n'.join(f'({i}, {b}, {v if v is not None else "NULL"})' for i,b,v in rows)
    threshold=180+variant*20
    group_threshold=[200,310,300,320,430,350,480,450,560,650][variant]
    templates=[
      ('Aggregate COUNT', 'SELECT COUNT(*) FROM accounts;', f'COUNT(*) includes all {len(rows)} rows, including rows with NULL balances.'),
      ('Non-NULL COUNT','SELECT COUNT(balance) FROM accounts;', f'COUNT(balance) excludes {len(null_ids)} NULL balances, leaving {len(rows)-len(null_ids)} values.'),
      ('Filtered SUM',"SELECT SUM(balance) FROM accounts WHERE branch='A';",f'Branch A has non-NULL balances {a_values}; SUM adds these values.'),
      ('NULL filtering','SELECT id FROM accounts WHERE balance IS NULL ORDER BY id;',f'IS NULL selects rows with missing balances: ids {null_ids}.'),
      ('DISTINCT','SELECT COUNT(DISTINCT balance) FROM accounts;','COUNT(DISTINCT balance) ignores NULL and counts each different non-NULL balance once.'),
      ('HAVING',f'SELECT branch FROM accounts GROUP BY branch HAVING SUM(balance) > {group_threshold} ORDER BY branch;','Compute SUM(balance) within each branch, ignoring NULL, then keep only groups above the stated threshold.'),
      ('Range filtering',f'SELECT id FROM accounts WHERE balance >= {threshold} ORDER BY id;','Compare each non-NULL balance with the threshold. NULL comparisons are UNKNOWN and do not pass WHERE.'),
      ('COALESCE','SELECT SUM(COALESCE(balance, 25)) FROM accounts;',f'Replace each of the {len(null_ids)} NULL balances by 25, then add all {len(rows)} resulting values.'),
      ('LEFT JOIN',"SELECT COUNT(*) FROM branches b LEFT JOIN accounts a ON b.code=a.branch;",f'All {len(rows)} account rows match a branch. Each branch with no account contributes one NULL-extended row. Missing branches: {missing_branches}.'),
      ('Unmatched rows',"SELECT b.code FROM branches b LEFT JOIN accounts a ON b.code=a.branch WHERE a.id IS NULL ORDER BY b.code;",f'Only branches with no matching account have NULL-extended account ids. Such branches are: {missing_branches}.'),
      ('Correlated EXISTS',f'SELECT b.code FROM branches b WHERE EXISTS (SELECT 1 FROM accounts a WHERE a.branch=b.code AND a.balance > {threshold}) ORDER BY b.code;', 'For each branch, EXISTS checks whether at least one account has a balance above the threshold.'),
      ('Ranking',"SELECT id, DENSE_RANK() OVER (ORDER BY balance DESC) AS r FROM accounts WHERE balance IS NOT NULL ORDER BY id;",'Sort non-NULL balances descending for ranks. Equal balances share a rank, and DENSE_RANK leaves no rank gaps.'),
      ('CASE',f"SELECT SUM(CASE WHEN balance >= {threshold} THEN 1 ELSE 0 END) FROM accounts;",'The CASE contributes 1 for each qualifying balance and 0 otherwise, including NULL; SUM counts the qualifying rows.'),
      ('Scalar subquery','SELECT id FROM accounts WHERE balance = (SELECT MAX(balance) FROM accounts) ORDER BY id;','The scalar subquery finds the maximum non-NULL balance; the outer query selects all matching ids.'),
      ('NOT IN and NULL','SELECT id FROM accounts WHERE balance NOT IN (100, NULL) ORDER BY id;','For values other than 100, comparison with the NULL makes NOT IN UNKNOWN; 100 fails directly. No row passes.')
    ]
    def fmt(result):
        if not result:return '(no rows)'
        return '; '.join(', '.join('NULL' if v is None else str(v) for v in row) for row in result)
    for topic,sql,reason in templates:
        result=db.execute(sql).fetchall(); ans=fmt(result)
        extras=['(no rows)','NULL','0','1','2','3','4','5','6','7','A; B; C','A; C','B; C','D','1; 2; 4; 5; 6','1; 2; 3; 4; 5; 6']
        if len(result)==1 and len(result[0])==1 and isinstance(result[0][0],(int,float)):
            n=result[0][0]; extras=[str(n+1),str(n-1),str(n+25),str(n*2),'NULL','0']
        elif topic=='Ranking':
            extras=['1, 1; 2, 2; 4, 3; 5, 4; 6, 5','1, 3; 2, 2; 4, 1; 5, 2; 6, 5','1, 2; 2, 1; 4, 3; 5, 1; 6, 4','1, 4; 2, 3; 4, 1; 5, 2; 6, 5']+extras
        else:
            rng.shuffle(extras)
        stem='Using SQLite and the following data:\n'+table+'\n'+('branches(code) contains A, B, C, D.\n' if 'branches' in sql else '')+'What is the result? Rows are separated by semicolons.\n'+sql
        add('dbms',topic,'Hard' if topic in ['Ranking','NOT IN and NULL','Correlated EXISTS'] else 'Moderate',stem,ans,extras,reason+' Result: '+ans+'.','executed-SQL',topic)
    db.close()

# DSA: 15 trace/count families, ten data variants each.
for k in range(10):
    n=k+4
    num('dsa','Loop analysis','Moderate',f'How many times does work() run?\nfor i = 1 to {n}:\n  for j = 1 to i:\n    work()',n*(n+1)//2,f'Calls = 1+2+...+{n} = {n}×{n+1}/2 = {n*(n+1)//2}.','triangular-loop')
    limit=2**(k+3)
    num('dsa','Loop analysis','Moderate',f'How many iterations execute?\ni = 1\nwhile i < {limit}:\n  i = i * 2',k+3,f'After t iterations i=2^t. Reaching {limit}=2^{k+3} ends the loop, so there are {k+3} iterations.','doubling-loop')
    num('dsa','Tree counts','Moderate',f'A perfect binary tree has height {k+2}, measured in edges from root to leaf. How many nodes does it contain?',2**(k+3)-1,f'Levels 0 through h contain 1+2+...+2^h = 2^(h+1)−1 = {2**(k+3)-1} nodes.','perfect-tree')
    vertices=k+5
    num('dsa','Graph counts','Moderate',f'How many edges are in a simple complete undirected graph with {vertices} vertices?',vertices*(vertices-1)//2,f'Each unordered pair forms one edge: V(V−1)/2 = {vertices}×{vertices-1}/2 = {vertices*(vertices-1)//2}.','complete-graph')
    vals=[k+2,k+5,k+1,k+8]; stack=[]
    stack.append(vals[0]);stack.append(vals[1]);stack.pop();stack.append(vals[2]);stack.append(vals[3]);a=stack.pop()
    num('dsa','Stack traces','Easy',f'An empty stack receives push({vals[0]}), push({vals[1]}), pop(), push({vals[2]}), push({vals[3]}). What does the next pop() return?',a,f'After the first pop the bottom item is {vals[0]}; pushing {vals[2]} then {vals[3]} leaves {vals[3]} on top.','stack-trace',vals+[0,-1])
    q=collections.deque(vals[:3]);q.popleft();q.append(vals[3]);a=q.popleft()
    num('dsa','Queue traces','Easy',f'An empty FIFO queue receives enqueue({vals[0]}), enqueue({vals[1]}), enqueue({vals[2]}), dequeue(), enqueue({vals[3]}). What does the next dequeue() return?',a,f'The first dequeue removes {vals[0]}; the oldest remaining item is {vals[1]}.','queue-trace',vals+[0,-1])
    arr=[4+k,1+k,7+k,3+k,9+k,2+k]; left=k%3;right=left+2;ans=sum(arr[left:right+1])
    num('dsa','Prefix sums','Moderate',f'For zero-based array {arr}, what is the sum of indices {left} through {right}, inclusive?',ans,f'The selected values are {arr[left:right+1]}; their sum is {ans}. A prefix-sum solution subtracts prefix[{left}] from prefix[{right+1}].','range-sum')
    arr=[-2-k,3+k,-1,4,-5,2];best=arr[0];ending=0
    for x in arr:ending=max(x,ending+x);best=max(best,ending)
    num('dsa','Dynamic programming','Moderate',f'What is the maximum sum of a nonempty contiguous subarray of {arr}?',best,f'Kadane tracks max(current value, previous ending sum + value). The best segment is [{3+k}, -1, 4], whose sum is {best}.','maximum-subarray')
    keys=[k+10,k+5,k+15,k+2,k+7];ordered=sorted(keys)
    add('dsa','BST traces','Moderate',f'Insert {keys} in that order into an initially empty BST with distinct keys. What is the inorder traversal?',', '.join(map(str,ordered)),[', '.join(map(str,a)) for a in [keys,list(reversed(keys)),list(reversed(ordered)),ordered[1:]+ordered[:1]]],f'Inorder visits keys in sorted order: {ordered}.','worked-drill','bst-inorder')
    arr=[k+5,k+1,k+4,k+2,k+3];res=arr.copy();j=res.index(min(res));res[0],res[j]=res[j],res[0]
    add('dsa','Sorting traces','Moderate',f'After one outer pass of ascending selection sort (swap the minimum into index 0), what is {arr}?',str(res),[str(sorted(arr)),str(arr),str(arr[::-1]),str(arr[1:]+arr[:1])],f'The minimum is {k+1} at index 1; swap it with {k+5} at index 0. Result: {res}.','worked-drill','selection-pass')
    size=11;keys=[k+1,k+12,k+23];table=[None]*size;positions=[]
    for key in keys:
        pos=key%size
        while table[pos] is not None:pos=(pos+1)%size
        table[pos]=key;positions.append(pos)
    num('dsa','Hashing traces','Moderate',f'Insert keys {keys} into an empty 11-slot table using h(x)=x mod 11 and linear probing with wraparound. At which zero-based slot is the last key stored?',positions[-1],f'Initial hashes collide at {keys[0]%11}. Successive occupied slots are {positions}; the final key goes to {positions[-1]}.','linear-probing',list(range(11)))
    i=k+1
    num('dsa','Heap indexing','Moderate',f'In a zero-based array representation of a binary heap, what is the left-child index of a node at index {i}, assuming that child exists?',2*i+1,f'For zero-based indexing, left child = 2i+1 = 2×{i}+1 = {2*i+1}.','heap-child')
    n=2**(k+2)-1;comparisons=k+2
    num('dsa','Search counts','Moderate',f'A sorted array has {n} distinct items. Using ordinary binary search that checks the midpoint each iteration, what is the maximum number of iterations for a successful search?',comparisons,f'{n}=2^{k+2}−1 forms a full binary search decision tree with {k+2} levels, so at most {k+2} midpoint checks.','binary-search-depth')
    edges=[('A','B',k+2),('A','C',k+7),('B','C',3),('B','D',k+6),('C','D',2)]
    dist={'A':0,'B':math.inf,'C':math.inf,'D':math.inf}
    for _ in range(3):
        for u,v,w in edges:dist[v]=min(dist[v],dist[u]+w)
    a=dist['D']
    num('dsa','Shortest paths','Moderate',f'A directed graph has edges A→B:{k+2}, A→C:{k+7}, B→C:3, B→D:{k+6}, C→D:2. What is the shortest distance from A to D?',a,f'The path A→B→C→D costs {k+2}+3+2 = {a}. Direct alternatives A→C→D and A→B→D are no smaller.','shortest-path')
    n=k+3
    num('dsa','Recursion counts','Moderate',f'For f(n): if n=0 return 0; else return 1+f(n−1), how many total function invocations occur for f({n}), including the initial and base calls?',n+1,f'The calls have arguments {n}, {n-1}, ..., 0: {n+1} invocations.','recursive-calls')

# OS: six families, five variants each.
for k in range(5):
    bursts=[k+3,k+5,k+2];waits=[0,bursts[0],sum(bursts[:2])];avg=sum(waits)/3
    add('os','Scheduling calculations','Moderate',f'Three processes arrive at time 0 with CPU bursts {bursts} ms and run in that FCFS order, with no overhead. What is average waiting time?',f'{avg:.2f} ms',[f'{avg+1:.2f} ms',f'{avg+2:.2f} ms',f'{sum(bursts)/3:.2f} ms','0.00 ms'],f'Waiting times are {waits} ms. Average = {sum(waits)}/3 = {avg:.2f} ms.','worked-drill','fcfs-wait')
    page=2**(10+k);address=page*(k+2)+125+k
    num('os','Paging calculations','Moderate',f'With page size {page} bytes, what is the page number for byte-addressed virtual address {address}? Assume page numbers start at zero.',address//page,f'Page number = floor(address/page size) = floor({address}/{page}) = {address//page}; offset = {address%page}.','page-number')
    num('os','Paging calculations','Moderate',f'With page size {page} bytes, what is the offset of virtual byte address {address}?',address%page,f'Offset = address mod page size = {address} mod {page} = {address%page}.','page-offset')
    refs=[1,2,3,1,4,2,5,1,k+6];frames=[];faults=0
    for r in refs:
        if r not in frames:
            faults+=1
            if len(frames)==3:frames.pop(0)
            frames.append(r)
    num('os','Page replacement traces','Hard',f'Using FIFO with 3 initially empty frames, how many page faults occur for reference string {refs}? Hits do not change FIFO order.',faults,f'Simulating arrivals and evicting the oldest loaded page gives {faults} faults. The fourth reference (1) and sixth reference (2) are hits; hits do not refresh FIFO age.','fifo-faults')
    logical=32;off=10+k;entries=2**(logical-off)
    num('os','Page-table sizing','Hard',f'A 32-bit byte-addressed virtual space uses {2**off}-byte pages and a flat page table. How many page-table entries cover the entire space?',entries,f'Offset requires {off} bits. Page-number bits = 32−{off} = {32-off}; entries = 2^{32-off} = {entries}.','page-table-entries')
    avail=3+k;maximum=10+k;allocated=4+k;need=maximum-allocated
    num('os','Banker calculations','Moderate',f'For one resource type, a process declares maximum claim {maximum} units and currently holds {allocated}. What is its remaining Need value?',need,f'Need = Maximum − Allocation = {maximum}−{allocated} = {need}. Available resources are a separate quantity.','banker-need')

# Linux: executable Bash output questions; safe, deterministic builtins/text tools.
scripts=[
('x=7; printf "%s" "$x"','Variable expansion prints the stored value.'),
("x=7; printf '%s' '$x'",'Single quotes preserve the literal dollar sign and variable name.'),
('printf "%s" "$((7 + 3 * 2))"','Multiplication has higher precedence than addition: 7+6=13.'),
('printf "%s" "$((17 / 5))"','Bash integer division truncates toward zero.'),
('printf "%s" "$((17 % 5))"','The remainder after dividing 17 by 5 is 2.'),
('false; printf "%s" "$?"','false returns exit status 1.'),
('true; printf "%s" "$?"','true returns exit status 0.'),
('set -- red "blue green" yellow; printf "%s" "$#"','There are three positional arguments; the quoted space stays inside one argument.'),
('set -- red "blue green" yellow; printf "%s" "$2"','The second positional parameter is the two-word string passed as one argument.'),
('x=; printf "%s" "${x:-fallback}"','The :- form uses the fallback when the variable is unset or empty.'),
('x=; printf "%s" "${x-fallback}"','The - form without a colon substitutes only for an unset variable, not an empty one.'),
('unset x; printf "%s" "${x-fallback}"','Here x is unset, so the fallback is substituted.'),
('x=banking; printf "%s" "${#x}"','${#x} reports the length of the expanded string.'),
('for n in 2 4 6; do printf "%s\\n" "$n"; done','The for loop visits the three supplied words in order.'),
('n=0; while [ "$n" -lt 3 ]; do n=$((n+1)); done; printf "%s" "$n"','The counter reaches 3, making the loop condition false.'),
('false && printf yes; printf done','The AND-list skips yes because false fails; the next independent command prints done.'),
('false || printf recovered','The OR-list runs its second command because false fails.'),
('true || printf skipped; printf done','The OR-list skips its second command when true succeeds.'),
('printf "3\\n12\\n2\\n" | sort -n','Numeric sort orders 2 before 3 before 12.'),
('printf "a\\na\\nb\\na\\n" | uniq','uniq collapses only adjacent duplicate lines; the final a is retained.'),
('printf "a\\na\\nb\\na\\n" | sort -u','Sorting with -u produces each distinct line once.'),
('printf "alpha\\nbeta\\nalpine\\n" | grep "^al"','The ^ anchor requires al at the start of the line.'),
('printf "ERROR\\nerror\\nOK\\n" | grep -ic error','Case-insensitive counting matches both ERROR and error.'),
('printf "A:10:x\\nB:20:y\\n" | cut -d: -f2','The second colon-delimited fields are 10 and 20.'),
("printf 'one two three\\n' | awk '{print $2}'",'awk selects the second whitespace-separated field.'),
("printf '2 3\\n4 5\\n' | awk '{s += $1} END {print s}'",'The first fields sum to 2+4=6.'),
("printf 'foo foo\\n' | sed 's/foo/bar/'",'Without g, sed replaces only the first match in each line.'),
("printf 'foo foo\\n' | sed 's/foo/bar/g'",'The g flag replaces all matching occurrences within the line.'),
('set -- "a b" c; for x in "$@"; do printf "[%s]" "$x"; done','Quoted "$@" preserves the two argument boundaries.'),
('printf "x\\ny\\nz\\n" | head -n 2','head selects the first two lines.')
]
for i,(script,why) in enumerate(scripts):
    result=subprocess.run(['bash','--noprofile','--norc','-c',script],capture_output=True,text=True,check=True,env={'PATH':'/usr/bin:/bin','LC_ALL':'C'})
    out=result.stdout.rstrip('\n')
    ans=out if out else '(empty output)'
    candidates=['(empty output)','Syntax error','0','1','2','3','7','13','$x','fallback','done','yesdone','a; b','[a][b][c]']
    if '\n' in out:candidates=[out.replace('\n',' '),out.split('\n')[0],out.split('\n')[-1],out[::-1]]+candidates
    rng.shuffle(candidates)
    add('linux','Shell output','Moderate','In Bash, what is the standard output of this script? Ignore the final newline; line breaks inside an option are significant.\n'+script,ans,candidates,why+' Output: '+repr(out)+'.','executed-shell',f'shell-output-{i+1}')

# Append additions after the original generation so existing IDs, option orders
# and random-number consumption remain stable for saved progress and imports.
for sid,_,_ in ADDITIONAL_SUBJECTS:
    for line in (ROOT/'content'/f'{sid}.txt').read_text().splitlines():
        if not line or line.startswith('#'):continue
        p=line.split('¦'); assert len(p)==9,(sid,len(p),line)
        topic,diff,stem,ans,*rest=p
        add(sid,topic,diff,stem,ans,rest[:4],rest[4])
SUBJECTS += ADDITIONAL_SUBJECTS

# Quality-first release: retired items never enter any practice or revision pool.
legacy_counts=collections.Counter(q['subject'] for q in questions)
for sid,_,target in SUBJECTS:assert legacy_counts[sid]==target
baseline=json.loads((ROOT/'content/review/baseline-manifest.json').read_text())
assert set(baseline)=={q['id'] for q in questions}
retired=json.loads((ROOT/'content/review/retirements.json').read_text())
after_baseline=json.loads((ROOT/'content/review/retired-after-baseline.json').read_text())
assert set(retired)<=set(baseline)|set(after_baseline)
questions[:]=[q for q in questions if q['id'] not in retired]

# Preserve source IDs and append new IDs after the previous subject maximum.
# The add() helper normally counts rows, so use a stable sequence override here.
new_subjects=[('programming','Programming & OOP'),('architecture','Computer Fundamentals & Architecture'),('web','Web Technology')]
def append_content(sid,path):
    for line in path.read_text().splitlines():
        if not line or line.startswith('#'):continue
        parts=line.split('¦');assert len(parts)==9,(path,line)
        topic,diff,stem,answer,*rest=parts
        add(sid,topic,diff,stem,answer,rest[:4],rest[4])
        maximum=max([int(qid.rsplit('-',1)[1]) for qid,v in baseline.items() if v['subject']==sid]+[0])
        if maximum:
            additions=sum(q['subject']==sid and q['id'] not in baseline for q in questions[:-1])
            questions[-1]['id']=f'{sid}-{maximum+additions+1:03}'
for sid,_ in new_subjects:append_content(sid,ROOT/'content'/f'{sid}.txt')
for sid in ['network','dbms','os','se_bank_it']:append_content(sid,ROOT/'content'/f'supplement_{sid}.txt')
python_cases=[
 ('print(7 // 2)','3',['3.5','4','2','1'],'Positive integer floor division gives 3, not 3.5.'),
 ('print(7 % 3)','1',['2','3','0','2.3333333333333335'],'The remainder is 1 because 7 = 2×3 + 1.'),
 ('print(2 + 3 * 4)','14',['20','24','9','18'],'Multiplication is evaluated before addition: 2 + 12 = 14.'),
 ('print(list(range(1, 6, 2)))','[1, 3, 5]',['[1, 3, 5, 6]','[1, 2, 3, 4, 5]','[2, 4, 6]','[1, 3]'],'The range starts at 1, steps by 2 and excludes stop value 6.'),
 ('s = "BANK"; print(s[1:3])','AN',['BAN','ANK','BA','NK'],'Indices 1 and 2 are included; stop index 3 is excluded.'),
 ('a = [1, 2]; b = a; b.append(3); print(len(a))','3',['2','1','4','0'],'a and b refer to the same list, so appending through b changes its length to 3.'),
 ('d = {"a": 1, "a": 2}; print(d["a"])','2',['1','[1, 2]','3','None'],'The later value replaces the earlier value for the same dictionary key.'),
 ('print("7" + "3")','73',['10','21','7 3','[7, 3]'],'Both operands are strings, so + concatenates them.'),
 ('print(bool(""))','False',['True','None','0','SyntaxError'],'An empty string has false truth value; print displays the Boolean False.'),
 ('print([x * 2 for x in [1, 2, 3]])','[2, 4, 6]',['[1, 2, 3, 1, 2, 3]','[1, 4, 9]','[2, 3, 4]','[6, 4, 2]'],'The comprehension multiplies each input element by two in input order.'),
]
# Keep the first reviewed Python family IDs stable when another topic is replaced.
for case_number,(script,answer,wrong,explanation) in enumerate(python_cases,start=806):
    output=subprocess.check_output(['python3','-I','-c',script],text=True).rstrip('\n')
    assert output==answer
    add('programming','Python output','Moderate','In Python 3, what is printed?\n'+script,answer,wrong,explanation,'executed-python','python-output-'+str(case_number))

# Versioned topic replacement; legacy generation above keeps other subjects byte-stable.
from build_network import load_network
from build_dbms import load_dbms
from build_os import load_os
questions[:]=load_network()+load_dbms()+load_os()+[q for q in questions if q['subject'] not in {'network','dbms','os'}]
assert not {q['id'] for q in questions}&set(retired)

counts=collections.Counter(q['subject'] for q in questions)
all_subjects=[(sid,name) for sid,name,_ in SUBJECTS]+new_subjects
assert len({q['id'] for q in questions})==len(questions)
assert len({q['question'] for q in questions})==len(questions)
for q in questions:
    assert len(q['options'])==5 and len(set(q['options']))==5
    assert 0<=q['answer']<5 and len(q['explanation'])>20
    q['studyScope']='core'
    q['studyReason']='Curated degree-level foundation or representative exam-style application'
    if q['difficulty']=='Hard':q['difficulty']='Moderate'

# References are selected by subject/topic and may be further narrowed by ID.
from review_sources import references_for
for q in questions:
    q['references']=q.get('references') or references_for(q)
    assert q['references'],q['id']
bank={'schemaVersion':1,'version':'2.3.0','title':'Bank SO IT','subjects':[{'id':sid,'name':name} for sid,name in all_subjects],
      'retiredQuestionIds':sorted(retired),'questions':questions}
OUT.mkdir(parents=True,exist_ok=True)
(ROOT/'dist').mkdir(exist_ok=True)
(ROOT/'docs').mkdir(exist_ok=True)
(OUT/'bank.json').write_text(json.dumps(bank,ensure_ascii=False,separators=(',',':')))
(ROOT/'dist/question-bank.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2))
report={'total':len(questions),'subjects':dict(counts),'retired':len(retired),'kinds':dict(collections.Counter(q['kind'] for q in questions)),
'difficulty':dict(collections.Counter(q['difficulty'] for q in questions)),
'checks':['Unique IDs and stems','Five distinct options per question','Valid answer indices','Explanations and references present','Legacy ID retirement prevents duplicate reintroduction','SQL answers executed in SQLite during generation','Shell answers executed in Bash during generation','Python answers executed in Python 3 during generation']}
(ROOT/'docs/bank-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
