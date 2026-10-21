"""Render reviewed fixtures and independently execute their SQL/set operations."""
import json,pathlib,sqlite3,itertools
ROOT=pathlib.Path(__file__).resolve().parents[1]

def fixtures():return json.loads((ROOT/'content/curated/dbms-r2-cases.json').read_text())
def value(v):return 'NULL' if v is None else str(v)
def tuple_text(row):return '('+', '.join(map(value,row))+')'
def render(number,intro):
    data=fixtures();case=data['cases'][str(number)]
    if case['type']=='sql':
        pieces=['Using SQLite, foreign_keys = ON. '+intro]
        for name in case['tables']:
            t=data['tables'][name];pieces.append(t['heading']+':\n'+'\n'.join(tuple_text(row) for row in t['rows']))
        pieces.extend(['Rows in options are separated by semicolons; NULL is shown explicitly.','\n'+case['sql']])
        return '\n'.join(pieces)
    pieces=['Classical set-based relational algebra. '+intro]
    for name,t in case['relations'].items():pieces.append(name+'('+','.join(t['columns'])+') = {'+', '.join(tuple_text(row) for row in t['rows'])+'}')
    pieces.extend(['Expression: '+case['expression'],'List tuples in lexicographic order for comparison; a relation itself has no row order.'])
    return '\n'.join(pieces)

def sql_result(case,data):
    db=sqlite3.connect(':memory:');db.execute('PRAGMA foreign_keys = ON')
    for name in case['tables']:
        t=data['tables'][name];db.execute(t['schema']);db.executemany('INSERT INTO '+name+' VALUES('+','.join('?' for _ in t['rows'][0])+')',t['rows'])
    db.commit();rows=[]
    try:
        for sql in case['sql'].split(';'):
            if not sql.strip():continue
            cursor=db.execute(sql)
            if cursor.description:rows=cursor.fetchall()
    except sqlite3.IntegrityError as error:
        result={'SQLITE_CONSTRAINT_PRIMARYKEY':'PRIMARY KEY constraint violation','SQLITE_CONSTRAINT_CHECK':'CHECK constraint violation','SQLITE_CONSTRAINT_FOREIGNKEY':'FOREIGN KEY constraint violation'}.get(error.sqlite_errorname)
        if result is None:raise
        return result
    finally:db.close()
    return '; '.join(', '.join(map(value,row)) for row in rows) if rows else '(no rows)'

def algebra_result(case):
    relations=case['relations'];r=relations['R'];rows={tuple(row) for row in r['rows']};op=case['operation'];parentheses=False
    if op=='select':
        column=r['columns'].index(case['column']);out={row for row in rows if row[column]>=case['value']};parentheses=True
    elif op=='project':
        positions=[r['columns'].index(c) for c in case['columns']];out={tuple(row[i] for i in positions) for row in rows}
    elif op=='product-count':return str(sum(1 for _ in itertools.product(rows,{tuple(row) for row in relations['S']['rows']})))
    elif op in ['union','difference']:
        other={tuple(row) for row in relations['S']['rows']};out=rows|other if op=='union' else rows-other
    elif op=='natural-join':
        s=relations['S'];shared=set(r['columns'])&set(s['columns']);extra=[i for i,c in enumerate(s['columns']) if c not in shared]
        out={a+tuple(b[i] for i in extra) for a in rows for b in map(tuple,s['rows']) if all(a[r['columns'].index(c)]==b[s['columns'].index(c)] for c in shared)};parentheses=True
    else:raise AssertionError(op)
    return '; '.join(tuple_text(row) if parentheses else ', '.join(map(value,row)) for row in sorted(out)) if out else '(no tuples)'
def result(number):
    data=fixtures();case=data['cases'][str(number)]
    return sql_result(case,data) if case['type']=='sql' else algebra_result(case)
