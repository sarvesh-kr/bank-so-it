"""Regression checks for the user-scoped network set; no network access in CI."""
import collections,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]

def check_network(bank):
    qs=[q for q in bank['questions'] if q['subject']=='network'];by_id={q['id']:q for q in qs}
    assert set(by_id)=={f'network-r2-{i:03}' for i in range(1,232)}
    counts=collections.Counter(q['topic'] for q in qs)
    expected={'OSI & TCP/IP models':16,'Network devices & media':14,'Frames, packets & headers':13,'IP addressing & NAT':20,'Subnetting':12,'TCP, UDP & communication':10,'Services & ports':34,'Bandwidth & network fundamentals':8,'TLS, cryptography & encoding':23,'Firewalls & protective controls':14,'Common attacks':20,'Malware & virus types':16,'CIA & general security':14,'Web APIs & HTTP basics':9,'Blockchain fundamentals':6,'CDN & web delivery':2}
    assert dict(counts)==expected,(counts,expected)
    drills=[q for q in qs if q['kind']=='worked-drill']
    assert len(drills)==10 and all(q['topic']=='Subnetting' for q in drills)
    assert all(q['difficulty'] in ['Easy','Moderate'] and q['references'] for q in qs)
    # Expected service associations are checked against the retrieved IANA rows,
    # separately from the generator's chosen answer index.
    snapshot=json.loads((ROOT/'content/review/network-r2-port-registry.json').read_text())
    entries={(r['Service Name'],int(r['Port Number']),r['Transport Protocol']) for r in snapshot['rows']}
    facts={85:('21',[('ftp',21,'tcp')]),86:('SSH',[('ssh',22,'tcp')]),87:('Telnet',[('telnet',23,'tcp')]),88:('TCP 25',[('smtp',25,'tcp')]),89:('Port 53 with UDP and TCP',[('domain',53,'udp'),('domain',53,'tcp')]),90:('67 and 68',[('bootps',67,'udp'),('bootpc',68,'udp')]),91:('80',[('http',80,'tcp')]),92:('443',[('https',443,'tcp')]),93:('110',[('pop3',110,'tcp')]),94:('143',[('imap',143,'tcp')]),95:('123',[('ntp',123,'udp')]),96:('161',[('snmp',161,'udp')]),101:('3389',[('ms-wbt-server',3389,'tcp')]),104:('69',[('tftp',69,'udp')]),105:('389',[('ldap',389,'tcp')]),106:('445',[('microsoft-ds',445,'tcp')])}
    facts[211]=('IMAP: 993; POP3: 995',[('imaps',993,'tcp'),('pop3s',995,'tcp')])
    for number,(answer,associations) in facts.items():
        q=by_id[f'network-r2-{number:03}'];assert q['options'][q['answer']]==answer,q['id']
        assert set(associations)<=entries,q['id']
        for service,port,transport in associations:
            assert str(port) in q['question'] or str(port) in answer,q['id']
    report={'questions':231,'coverage':dict(counts),'subnet_calculations':10,'port_questions_verified':len(facts),'registry_rows':len(entries),'review_scope':'User-provided bank SO IT topics; no exact previous-paper frequencies asserted.'}
    (ROOT/'docs/network-quality-summary.json').write_text(json.dumps(report,indent=2)+'\n')
    return report
