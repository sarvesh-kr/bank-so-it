"""Verify DSA traces from displayed inputs rather than the selected answer."""
import bisect,collections,heapq,json,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
COVERAGE={'Complexity & algorithm basics':12,'Arrays & strings':12,'Linked lists':12,'Stacks':10,'Queues':10,'Searching':12,'Sorting':26,'Binary trees & traversals':14,'Binary search trees':12,'Heaps & priority queues':10,'Hashing':8,'Graphs & algorithm approaches':12}
WORKED={11,12,24,36,45,46,55,56,67,68,91,92,93,94,106,107,108,119,120,129,130,137,138,149,150}
def arrays(stem):return [json.loads(s) for s in re.findall(r'\[[\d,]+\]',stem)]
def array_text(values):return json.dumps(values,separators=(',',':'))
def inorder(node):return inorder(node[1])+[node[0]]+inorder(node[2]) if node else []
def insert(node,key):
    if node is None:return [key,None,None]
    side=1 if key<node[0] else 2;assert key!=node[0];node[side]=insert(node[side],key);return node
def delete(node,key):
    if key<node[0]:node[1]=delete(node[1],key)
    elif key>node[0]:node[2]=delete(node[2],key)
    elif node[1] is None:return node[2]
    elif node[2] is None:return node[1]
    else:
        successor=node[2]
        while successor[1]:successor=successor[1]
        node[0]=successor[0];node[2]=delete(node[2],successor[0])
    return node

def computed(number,q):
    stem=q['question'];detail={}
    if number==11:
        n=int(re.search(r'n = (\d+)',stem).group(1));count=0
        for i in range(1,n+1):
            for j in range(i):count+=1
        answer=str(count);detail={'inner_iteration_counts':list(range(1,n+1))}
    elif number==12:
        n=int(re.search(r'n = (\d+)',stem).group(1));values=[]
        while n>1:assert n%2==0;n//=2;values.append(n)
        answer=str(len(values));detail={'successive_values':values}
    elif number==24:
        base=int(re.search(r'byte address (\d+)',stem).group(1));size=int(re.search(r'occupies (\d+) bytes',stem).group(1));index=int(re.search(r'A\[(\d+)\]',stem).group(1));assert 'zero-based' in stem
        answer=str(base+index*size);detail={'base':base,'element_bytes':size,'index':index}
    elif number==36:
        values=list(map(int,re.search(r'initially contains ([\d →]+)\.',stem).group(1).split(' → ')));new,after=map(int,re.search(r'Insert (\d+) immediately after node (\d+)',stem).groups());removed=int(re.search(r'delete the node containing (\d+)',stem).group(1));values.insert(values.index(after)+1,new);values.remove(removed)
        answer=' → '.join(map(str,values));detail={'final_list':values}
    elif number==45:
        tokens=re.search(r'postfix expression (.+?) using',stem).group(1).split();stack=[]
        for token in tokens:
            if token.isdigit():stack.append(int(token));continue
            b,a=stack.pop(),stack.pop();assert token in ['+','*'];stack.append(a+b if token=='+' else a*b)
        assert len(stack)==1;answer=str(stack[0]);detail={'tokens':tokens}
    elif number==46:
        stack=[];returned=[]
        for op,value in re.findall(r'(push|pop)\((\d*)\)',stem):
            if op=='push':stack.append(int(value))
            else:returned.append(stack.pop())
        answer=', '.join(map(str,returned));detail={'returned':returned,'remaining':stack}
    elif number==55:
        queue=collections.deque();returned=[]
        for op,value in re.findall(r'(enqueue|dequeue)\(([A-Z]?)\)',stem):
            if op=='enqueue':queue.append(value)
            else:returned.append(queue.popleft())
        answer=', '.join(returned);detail={'returned':returned,'remaining':list(queue)}
    elif number==56:
        capacity=int(re.search(r'capacity (\d+)',stem).group(1));count=int(re.search(r'count of (\d+)',stem).group(1));front=int(re.search(r'front index (\d+)',stem).group(1));assert 0<=count<capacity and 0<=front<capacity
        occupied=[(front+i)%capacity for i in range(count)];answer=str((occupied[-1]+1)%capacity);detail={'occupied_indices':occupied}
    elif number==67:
        values=arrays(stem)[0];target=int(re.search(r'target (\d+)',stem).group(1));lo,hi=0,len(values)-1;probes=[]
        while lo<=hi:
            mid=(lo+hi)//2;probes.append({'index':mid,'value':values[mid]})
            if values[mid]==target:break
            if values[mid]<target:lo=mid+1
            else:hi=mid-1
        else:raise AssertionError('Expected target present')
        answer=str(len(probes));detail={'probes':probes}
    elif number==68:
        values=arrays(stem)[0];target=int(re.search(r'target (\d+)',stem).group(1));answer=str(bisect.bisect_left(values,target));detail={'values':values,'target':target}
    elif number in {91,92,93}:
        values=arrays(stem)[0];trace=[list(values)]
        if number==91:
            assert 'left-to-right pass' in stem
            for i in range(len(values)-1):
                if values[i]>values[i+1]:values[i],values[i+1]=values[i+1],values[i]
                trace.append(list(values))
        elif number==92:
            smallest=min(range(len(values)),key=values.__getitem__);values[0],values[smallest]=values[smallest],values[0];trace.append(list(values))
        else:
            assert 'original second element and then the original third element' in stem
            for i in range(1,3):
                x=values[i];j=i
                while j>0 and values[j-1]>x:values[j]=values[j-1];j-=1
                values[j]=x;trace.append(list(values))
        answer=array_text(values);detail={'array_trace':trace}
    elif number==94:
        left,right=arrays(stem);assert left==sorted(left) and right==sorted(right)
        merged=list(heapq.merge(left,right));answer=array_text(merged);detail={'merged':merged}
    elif number==106:
        root,left,right=re.search(r'root ([A-Z]), children ([A-Z]) on the left and ([A-Z]) on the right',stem).groups();parent,l,r=re.search(r'([A-Z]) has left child ([A-Z]) and right child ([A-Z])',stem).groups();assert parent==left
        children={root:(left,right),parent:(l,r)}
        def walk(n):return walk(children[n][0])+[n]+walk(children[n][1]) if n in children else [n]
        visited=walk(root);answer=', '.join(visited);detail={'inorder':visited}
    elif number==107:
        root,left,right=re.search(r'root ([A-Z]), children ([A-Z]) and ([A-Z])',stem).groups();children={root:(left,right)}
        for parent,l,r in re.findall(r"([A-Z])'s children ([A-Z]) and ([A-Z])",stem):children[parent]=(l,r)
        def height(n):return 1+max(map(height,children[n])) if n in children else 0
        answer=str(height(root));detail={'child_edges':children,'height_convention':'edges'}
    elif number==108:
        leaves=int(re.search(r'has (\d+) leaves',stem).group(1));possible=[i for i in range(2*leaves) if 2*i==i+leaves-1];assert len(possible)==1;internal=possible[0]
        answer=str(internal+leaves);detail={'leaves':leaves,'internal':internal,'edges':2*internal}
    elif number in {119,120}:
        keys=arrays(stem)[0];tree=None
        for key in keys:tree=insert(tree,key)
        if number==119:
            key=int(re.search(r'searching for (\d+)',stem).group(1));path=[];node=tree
            while node:
                path.append(node[0])
                if node[0]==key:break
                node=node[1 if key<node[0] else 2]
            else:raise AssertionError('Search target absent')
            answer=', '.join(map(str,path));detail={'comparison_path':path}
        else:
            key=int(re.search(r'Delete root key (\d+)',stem).group(1));assert tree[0]==key and 'inorder successor' in stem;tree=delete(tree,key);assert inorder(tree)==sorted(set(keys)-{key})
            answer=str(tree[0]);detail={'inorder_after_deletion':inorder(tree)}
    elif number in {129,130}:
        values=arrays(stem)[0];assert all(values[(i-1)//2]<=values[i] for i in range(1,len(values)))
        if number==129:heapq.heappush(values,int(re.search(r'Append key (\d+)',stem).group(1)))
        else:removed=heapq.heappop(values);assert removed==int(re.search(r'Extract (\d+)',stem).group(1))
        assert all(values[(i-1)//2]<=values[i] for i in range(1,len(values)));answer=array_text(values);detail={'resulting_heap':values}
    elif number in {137,138}:
        modulus=int(re.search(r'h\(k\) = k mod (\d+)',stem).group(1))
        if number==137:
            keys=list(map(int,re.search(r'Insert keys (\d+), (\d+) and (\d+)',stem).groups()));slots=[None]*modulus
            for key in keys:
                slot=key%modulus
                while slots[slot] is not None:slot=(slot+1)%modulus
                slots[slot]=key
            target=int(re.search(r'Which slot stores (\d+)',stem).group(1));answer=str(slots.index(target));detail={'slots':slots}
        else:
            keys=list(map(int,re.search(r'Insert keys (\d+), (\d+), (\d+) and (\d+)',stem).groups()));bucket=int(re.search(r'keys are in bucket (\d+)',stem).group(1));buckets=[[] for _ in range(modulus)]
            for key in keys:buckets[key%modulus].append(key)
            answer=str(len(buckets[bucket]));detail={'buckets':buckets}
    elif number==149:
        edges=re.findall(r'([A-Z])-([A-Z])',stem);adj=collections.defaultdict(set)
        for a,b in edges:adj[a].add(b);adj[b].add(a)
        start=re.search(r'Starting at ([A-Z])',stem).group(1);queue=collections.deque([start]);seen={start};order=[]
        while queue:
            current=queue.popleft();order.append(current)
            for other in sorted(adj[current]):
                if other not in seen:seen.add(other);queue.append(other)
        answer=', '.join(order);detail={'dequeue_order':order}
    elif number==150:
        edges=[(a,b,int(w)) for a,b,w in re.findall(r'([A-Z])→([A-Z])\((\d+)\)',stem)];assert len(edges)==5 and all(w>=0 for a,b,w in edges)
        start,target=re.search(r'from ([A-Z]) to ([A-Z])',stem).groups();adj=collections.defaultdict(list)
        for a,b,w in edges:adj[a].append((b,w))
        distance={start:0};previous={};queue=[(0,start)]
        while queue:
            cost,node=heapq.heappop(queue)
            if cost!=distance[node]:continue
            for other,weight in adj[node]:
                candidate=cost+weight
                if candidate<distance.get(other,float('inf')):distance[other]=candidate;previous[other]=node;heapq.heappush(queue,(candidate,other))
        path=[target]
        while path[-1]!=start:path.append(previous[path[-1]])
        answer=str(distance[target]);detail={'distances':distance,'shortest_path':path[::-1]}
    else:raise AssertionError(number)
    return answer,detail

def check_dsa(bank):
    qs=[q for q in bank['questions'] if q['subject']=='dsa'];assert {q['id'] for q in qs}=={f'dsa-r2-{i:03}' for i in range(1,151)}
    assert dict(collections.Counter(q['topic'] for q in qs))==COVERAGE
    proofs={}
    for q in qs:
        number=int(q['id'].rsplit('-',1)[1]);assert q['kind']==('worked-dsa' if number in WORKED else 'concept')
        if number in WORKED:
            expected,detail=computed(number,q);assert expected==q['options'][q['answer']],(q['id'],expected,q['options'][q['answer']])
            proofs[q['id']]={'method':'independent DSA simulation/calculation','independent_result':expected,'details':detail}
    assert len(proofs)==25
    report={'questions':150,'coverage':COVERAGE,'concepts_and_applications':125,'worked_checks':25,'proofs':proofs}
    (ROOT/'docs/dsa-quality-summary.json').write_text(json.dumps(report,indent=2)+'\n')
    return proofs
