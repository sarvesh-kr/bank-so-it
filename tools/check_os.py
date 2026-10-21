"""Independently simulate worked OS cases using inputs parsed from displayed stems."""
import collections,itertools,json,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
COVERAGE={'OS roles & architecture':10,'Processes & states':14,'Threads & IPC':8,'CPU scheduling':14,'Synchronization':12,'Deadlocks':12,'Memory allocation & addressing':10,'Virtual memory & replacement':10,'Files, storage & I/O':10}
WORKED={43,44,45,46,69,79,80,89,90,100}

def schedule(jobs,policy,quantum=1):
    """Tick-based CPU model; return observed start/completion times and execution trace."""
    remaining={name:burst for name,arrival,burst in jobs};arrival={name:a for name,a,b in jobs}
    starts={};finished={};queue=collections.deque();trace=[];time=0;current=None;used=0
    order={name:n for n,(name,a,b) in enumerate(jobs)}
    while len(finished)<len(jobs):
        for name,a,b in jobs:
            if a==time:queue.append(name)
        if policy=='SRTF':
            ready=[name for name,a,b in jobs if a<=time and remaining[name]>0]
            current=min(ready,key=lambda n:(remaining[n],order[n])) if ready else None
        elif current is None:
            if policy=='SJF' and queue:
                current=min(queue,key=lambda n:(remaining[n],order[n]));queue.remove(current)
            elif queue:current=queue.popleft()
            used=0
        if current is None:trace.append(None);time+=1;continue
        starts.setdefault(current,time);trace.append(current);remaining[current]-=1;used+=1;time+=1
        if not remaining[current]:finished[current]=time;current=None
        elif policy=='RR' and used==quantum:
            # These RR cases have all arrivals at zero, so there is no boundary tie.
            assert all(a==0 for n,a,b in jobs)
            queue.append(current);current=None
    return starts,finished,trace

def replacement(refs,capacity,policy):
    frames=[];faults=0;trace=[]
    for page in refs:
        hit=page in frames
        if hit and policy=='LRU':frames.remove(page);frames.append(page)
        elif not hit:
            faults+=1
            if len(frames)==capacity:frames.pop(0)
            frames.append(page)
        trace.append({'page':page,'fault':not hit,'ordered_frames':list(frames)})
    return faults,trace

def computed(number,q):
    stem=q['question'];detail={}
    if number in {43,44}:
        assert 'all arrive at time 0' in stem and 'zero overhead' in stem
        bursts=list(map(int,re.search(r'bursts (?:are|of) (\d+), (\d+) and (\d+)',stem).groups()))
        jobs=[('P'+str(i+1),0,b) for i,b in enumerate(bursts)]
        policy='FCFS' if number==43 else 'SJF';assert policy in stem
        starts,ends,trace=schedule(jobs,policy);values=list(starts.values()) if number==43 else list(ends.values())
        answer=f'{sum(values)/len(values):g} time units';detail={'CPU_ticks':trace,'first_start':starts,'completion':ends}
    elif number==45:
        quantum=int(re.search(r'quantum (\d+)',stem).group(1));b1,b2=map(int,re.search(r'bursts of (\d+) and (\d+)',stem).groups())
        assert 'Round Robin' in stem and 'arrive at time 0 in queue order P1, P2' in stem and 'zero overhead' in stem
        starts,ends,trace=schedule([('P1',0,b1),('P2',0,b2)],'RR',quantum)
        answer=str(ends['P2']);detail={'CPU_ticks':trace,'completion':ends}
    elif number==46:
        assert 'preemptive SJF/SRTF' in stem and 'zero overhead' in stem
        jobs=[(name,int(a),int(b)) for name,a,b in re.findall(r'(P\d)\((\d+),(\d+)\)',stem)];assert len(jobs)==3
        starts,ends,trace=schedule(jobs,'SRTF');answer=str(ends['P2']);detail={'CPU_ticks':trace,'completion':ends}
    elif number==69:
        available=int(re.search(r'Available = (\d+)',stem).group(1));allocated=list(map(int,re.search(r'Allocation = \(([^)]+)\)',stem).group(1).split(',')));maximum=list(map(int,re.search(r'Maximum = \(([^)]+)\)',stem).group(1).split(',')))
        assert len(allocated)==len(maximum)==3
        need=[m-a for m,a in zip(maximum,allocated)];assert min(need)>=0
        safe=[]
        for sequence in itertools.permutations(range(3)):
            work=available
            for i in sequence:
                if need[i]>work:break
                work+=allocated[i]
            else:safe.append(', '.join('P'+str(i+1) for i in sequence))
        choices=set(safe)&set(q['options']);assert len(choices)==1
        answer=choices.pop();detail={'Need':need,'all_safe_sequences':safe}
    elif number==79:
        page_size=int(re.search(r'([\d,]+)-byte pages',stem).group(1).replace(',',''));frame=int(re.search(r'physical frame (\d+)',stem).group(1));offset=int(re.search(r'offset (\d+)',stem).group(1));assert 0<=offset<page_size
        answer=str(frame*page_size+offset);detail={'frame':frame,'page_bytes':page_size,'offset':offset}
    elif number==80:
        size=int(re.search(r'needs exactly (\d+) KiB',stem).group(1));page=int(re.search(r'whole (\d+) KiB pages',stem).group(1));pages=(size+page-1)//page
        answer=str(pages*page-size)+' KiB';detail={'allocated_pages':pages,'required_KiB':size,'allocated_KiB':pages*page}
    elif number in {89,90}:
        assert 'Three page frames are initially empty' in stem
        refs=list(map(int,re.search(r'reference string ([\d, ]+), how',stem).group(1).split(',')));policy='FIFO' if number==89 else 'LRU';assert 'under '+policy in stem
        faults,trace=replacement(refs,3,policy);answer=str(faults);detail={'reference_trace':trace}
    elif number==100:
        assert 'SSTF' in stem and 'no new arrivals' in stem
        head=int(re.search(r'starts at track (\d+)',stem).group(1));pending=list(map(int,re.search(r'requests are tracks (\d+), (\d+) and (\d+)',stem).groups()));movement=0;path=[head]
        while pending:
            distance=min(abs(x-head) for x in pending);nearest=[x for x in pending if abs(x-head)==distance];assert len(nearest)==1,'Unstated SSTF tie'
            movement+=distance;head=nearest[0];path.append(head);pending.remove(head)
        answer=str(movement)+' tracks';detail={'head_path':path}
    else:raise AssertionError(number)
    return answer,detail

def check_os(bank):
    qs=[q for q in bank['questions'] if q['subject']=='os'];assert {q['id'] for q in qs}=={f'os-r2-{i:03}' for i in range(1,101)}
    assert dict(collections.Counter(q['topic'] for q in qs))==COVERAGE
    proofs={}
    for q in qs:
        number=int(q['id'].rsplit('-',1)[1]);assert q['kind']==('worked-os' if number in WORKED else 'concept')
        if number in WORKED:
            expected,detail=computed(number,q);assert expected==q['options'][q['answer']],(q['id'],expected)
            proofs[q['id']]={'method':'independent OS simulation/calculation','independent_result':expected,'details':detail}
    assert len(proofs)==10
    report={'questions':100,'coverage':COVERAGE,'concepts_and_applications':90,'worked_checks':10,'proofs':proofs}
    (ROOT/'docs/os-quality-summary.json').write_text(json.dumps(report,indent=2)+'\n')
    return proofs
