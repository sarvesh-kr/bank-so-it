"""Stable primary documentation and authored textbook references for item review."""
SOURCES={
 'serverless':('AWS: Lambda execution model','https://docs.aws.amazon.com/lambda/latest/dg/welcome.html'),
 'iac':('HashiCorp: infrastructure as code','https://developer.hashicorp.com/terraform/intro'),
 'nat':('AWS: NAT gateways','https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html'),
 'bluegreen':('AWS: blue/green deployments','https://docs.aws.amazon.com/whitepapers/latest/overview-deployment-options/bluegreen-deployments.html'),
 'cdn':('AWS: CloudFront content delivery','https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html'),
 'autoscale':('AWS: EC2 Auto Scaling','https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html'),
 'containers':('Docker: container fundamentals','https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/'),
 'circuit':('Microsoft: circuit-breaker pattern','https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker'),
 'tokenization':('Hugging Face: tokenizers','https://huggingface.co/learn/llm-course/chapter2/4'),
 'parquet':('Apache: Parquet format','https://parquet.apache.org/docs/'),
 'zero_trust':('NIST: zero trust architecture, SP 800-207','https://csrc.nist.gov/pubs/sp/800/207/final'),
 'aes':('NIST: AES standard, FIPS 197','https://csrc.nist.gov/pubs/fips/197/final'),
 'sha':('NIST: Secure Hash Standard, FIPS 180-4','https://csrc.nist.gov/pubs/fips/180-4/upd1/final'),
 'hmac':('IETF: keyed hashing for message authentication','https://www.rfc-editor.org/rfc/rfc2104.html'),
 'imps':('NPCI: Immediate Payment Service','https://www.npci.org.in/what-we-do/imps/product-overview'),
 'journal':('systemd: journalctl manual','https://www.freedesktop.org/software/systemd/man/latest/journalctl.html'),
 'ss':('Linux manual: ss socket inspection','https://man7.org/linux/man-pages/man8/ss.8.html'),
 'dig':('ISC BIND: dig utility','https://bind9.readthedocs.io/en/latest/manpages.html#dig-dns-lookup-utility'),
 'networks_text':('Kurose and Ross: networking lectures by the authors','https://gaia.cs.umass.edu/kurose_ross/online_lectures.htm'),
 'mining':('Data Mining and Machine Learning, by Zaki and Meira','https://dataminingbook.info/'),
 'pca':('scikit-learn: principal component analysis','https://scikit-learn.org/stable/modules/decomposition.html#pca'),
 'osi':('ITU-T X.200: OSI reference model','https://www.itu.int/rec/T-REC-X.200-199407-I/en'),
 'ip':('IETF: Internet host requirements','https://www.rfc-editor.org/rfc/rfc1122.html'),
 'ipv6':('IETF: IPv6 specification','https://www.rfc-editor.org/rfc/rfc8200.html'),
 'tcp':('IETF: TCP specification','https://www.rfc-editor.org/rfc/rfc9293.html'),
 'udp':('IETF: UDP specification','https://www.rfc-editor.org/rfc/rfc768.html'),
 'dns':('IETF: DNS implementation and specification','https://www.rfc-editor.org/rfc/rfc1035.html'),
 'ports':('IANA: service names and port numbers','https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml'),
 'ethernet':('Cisco: LAN switching and VLAN configuration','https://www.cisco.com/c/en/us/support/docs/lan-switching/virtual-lans-vlan-vtp/10023-3.html'),
 'security':('NIST: security and privacy controls, SP 800-53','https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final'),
 'web_security':('OWASP: application security verification standard','https://owasp.org/www-project-application-security-verification-standard/'),
 'passwords':('OWASP: password storage guidance','https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html'),
 'tls':('IETF: TLS 1.3 specification','https://www.rfc-editor.org/rfc/rfc8446.html'),
 'zero':('NIST glossary: zero-day attack','https://csrc.nist.gov/glossary/term/zero_day_attack'),
 'db_design':('Database Design, 2nd edition: relational design and normalization','https://opentextbc.ca/dbdesign2/'),
 'sql':('PostgreSQL: SQL language reference','https://www.postgresql.org/docs/current/sql.html'),
 'isolation':('PostgreSQL: transaction isolation','https://www.postgresql.org/docs/current/transaction-iso.html'),
 'sqlite':('SQLite: SELECT statement','https://www.sqlite.org/lang_select.html'),
 'ostep':('Operating Systems: Three Easy Pieces, by its authors','https://pages.cs.wisc.edu/~remzi/OSTEP/'),
 'ods':('Open Data Structures, by Pat Morin','https://opendatastructures.org/'),
 'algorithms':('MIT: Introduction to Algorithms','https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/'),
 'bash':('GNU Bash reference manual','https://www.gnu.org/software/bash/manual/bash.html'),
 'coreutils':('GNU Coreutils reference manual','https://www.gnu.org/software/coreutils/manual/coreutils.html'),
 'systemd':('systemd: systemctl manual','https://www.freedesktop.org/software/systemd/man/latest/systemctl.html'),
 'linux_net':('Linux manual: ip networking command','https://man7.org/linux/man-pages/man8/ip.8.html'),
 'warehouse':('Kimball Group: dimensional modelling techniques','https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/'),
 'ml':('scikit-learn: supervised learning','https://scikit-learn.org/stable/supervised_learning.html'),
 'metrics':('scikit-learn: evaluation metrics','https://scikit-learn.org/stable/modules/model_evaluation.html'),
 'preprocess':('scikit-learn: preprocessing and leakage pitfalls','https://scikit-learn.org/stable/common_pitfalls.html'),
 'cluster':('scikit-learn: clustering','https://scikit-learn.org/stable/modules/clustering.html'),
 'cloud':('NIST: definition of cloud computing, SP 800-145','https://csrc.nist.gov/pubs/sp/800/145/final'),
 'cloud_security':('NIST: cloud security guidance, SP 800-144','https://csrc.nist.gov/pubs/sp/800/144/final'),
 'oauth':('IETF: OAuth 2.0 authorization framework','https://www.rfc-editor.org/rfc/rfc6749.html'),
 'oidc':('OpenID Foundation: OpenID Connect Core','https://openid.net/specs/openid-connect-core-1_0.html'),
 'account_aggregator':('RBI: Account Aggregator directions','https://rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=10598'),
 'localization':('RBI: Storage of Payment System Data, 6 April 2018','https://rbi.org.in/Scripts/NotificationUser.aspx?Id=11244'),
 'ai_risk':('NIST: Generative AI risk management profile','https://csrc.nist.gov/pubs/ai/600/1/final'),
 'testing':('ISTQB: official testing glossary','https://glossary.istqb.org/'),
 'swebok':('IEEE Computer Society: Software Engineering Body of Knowledge','https://www.computer.org/education/bodies-of-knowledge/software-engineering'),
 'scrum':('The Scrum Guide, 2020','https://scrumguides.org/scrum-guide.html'),
 'cert':('CERT-In: directions of 28 April 2022','https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf'),
 'npci':('NPCI: payment products and services','https://www.npci.org.in/'),
 'rtgs':('RBI: RTGS and distinction from NEFT','https://www.rbi.org.in/scripts/FS_FAQs.aspx?Id=65'),
 'token':('RBI: card tokenization guidance','https://www.rbi.org.in/scripts/BS_CircularIndexDisplay.aspx?Id=12159'),
 'swift':('SWIFT: financial messaging and its role','https://www.swift.com/about-us/who-we-are'),
 'pci':('PCI Security Standards Council: PCI DSS','https://www.pcisecuritystandards.org/standards/pci-dss/'),
 'c':('WG14: public C11 committee draft, N1570','https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf'),
 'cpp':('C++ working draft','https://eel.is/c++draft/'),
 'java':('Java SE 21 language specification','https://docs.oracle.com/javase/specs/jls/se21/html/index.html'),
 'python':('Python 3 language and library tutorial','https://docs.python.org/3/tutorial/'),
 'architecture':('MIT Computation Structures: instruction-set architectures','https://computationstructures.org/lectures/isa/isa.html'),
 'digital':('MIT: Computation Structures','https://computationstructures.org/'),
 'http':('IETF: HTTP semantics','https://www.rfc-editor.org/rfc/rfc9110.html'),
 'html':('WHATWG: HTML living standard','https://html.spec.whatwg.org/'),
 'web':('MDN: web platform documentation','https://developer.mozilla.org/en-US/docs/Web'),
 'json':('IETF: JSON format','https://www.rfc-editor.org/rfc/rfc8259.html'),
 'xml':('W3C: XML 1.0','https://www.w3.org/TR/xml/'),
}

def references_for(q):
    s,t,n=q['subject'],q['topic'],int(q['id'].rsplit('-',1)[1])
    if s=='network':
        ids=['osi'] if t=='Models' else ['ethernet'] if t in ['Ethernet','Wireless'] else ['ipv6','ip'] if t in ['IP addressing','Subnetting','IPv6','IP forwarding','IP fragmentation'] else ['tcp'] if t in ['Transport','TCP sequence numbers','Transport calculations'] else ['ports','ip'] if t in ['Protocols','Service ports'] else ['web_security'] if t=='Web security' else ['tls','security'] if t=='Cryptography' else ['security','ip']
        if n in [37,38,39,40,120,121,252]:ids=['dns']
        if n==66:ids=['passwords']
        if n==79:ids=['zero']
        if n==255:ids=['udp']
        if t in ['Transmission','Routing','Error control','Recovery planning','Availability']:ids=['networks_text','security'] if t in ['Recovery planning','Availability'] else ['networks_text']
    elif s=='dbms':ids=['sqlite'] if q['kind']=='executed-SQL' else ['isolation','sql'] if t in ['Transactions','Concurrency'] else ['db_design','sql']
    elif s=='os':ids=['ostep']
    elif s=='dsa':ids=['ods','algorithms']
    elif s=='linux':ids=['systemd'] if t=='Services' else ['linux_net','coreutils'] if t=='Networking' else ['bash','coreutils']
    elif s=='dw_dm':ids=['cluster'] if t=='Clustering' else ['preprocess'] if t=='Data preparation' else ['ml'] if t in ['Data mining foundations','Association rules'] else ['warehouse','db_design']
    elif s=='cloud_ai_ml':
        ids=['cloud','cloud_security'] if n<=20 or 47<=n<=55 else ['metrics'] if t=='Model evaluation' else ['preprocess'] if t=='Model training' else ['ml']
        if n==12:ids=['localization']
        if n==17:ids=['oauth']
        if n==19:ids=['oidc','oauth']
        if n==20:ids=['account_aggregator']
        if n in [21,44]:ids=['ai_risk']
    elif s=='se_bank_it':
        ids=['testing','swebok'] if t in ['Testing foundations','Test techniques','Reliability'] else ['scrum'] if n in [6,7] else ['swebok']
        if t in ['Banking systems','Payment systems','Payment controls','Banking channel security','Banking data quality']:ids=['npci','security']
        if t in ['Banking security operations','Banking resilience']:ids=['security']
        if n==38:ids=['cert']
        if n in [28,71,72]:ids=['rtgs']
        if n==74:ids=['swift']
        if n==75:ids=['token']
        if n==76:ids=['pci']
        if n==70:ids=['http']
    elif s=='programming':ids=['c'] if t=='C basics' else ['cpp'] if t=='C++ basics' else ['python'] if t.startswith('Python') else ['java']
    elif s=='architecture':ids=['architecture','digital']
    elif s=='web':ids=['http'] if t in ['HTTP','URLs'] else ['html','web']
    else:raise ValueError(s)
    if s=='web' and n==13:ids=['json']
    if s=='web' and n==14:ids=['xml']
    if s=='dw_dm' and t in ['Data mining foundations','Association rules']:ids=['mining']
    if s=='cloud_ai_ml' and n==40:ids=['pca']
    if s=='cloud_ai_ml' and n in {7:'serverless',15:'iac',47:'nat',48:'bluegreen',49:'cdn',52:'autoscale',53:'containers',55:'circuit',60:'tokenization'}:
        ids=[{7:'serverless',15:'iac',47:'nat',48:'bluegreen',49:'cdn',52:'autoscale',53:'containers',55:'circuit',60:'tokenization'}[n]]
    if s=='dw_dm' and n==59:ids=['parquet']
    if s=='linux' and n in {42:'journal',45:'ss',46:'dig'}:ids=[{42:'journal',45:'ss',46:'dig'}[n]]
    if s=='se_bank_it' and n==73:ids=['imps']
    if s=='network' and t=='Wireless':ids=['networks_text','security']
    if s=='network' and n in {60:'zero_trust',62:'aes',63:'sha',69:'hmac'}:ids=[{60:'zero_trust',62:'aes',63:'sha',69:'hmac'}[n]]
    return [{'title':SOURCES[i][0],'url':SOURCES[i][1]} for i in ids]
