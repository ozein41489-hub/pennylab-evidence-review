"""PennyLab independent-of-implementation test harness, synthetic evidence only."""
import json,pathlib
from evidence import verify

DAY="2026-10-30T00:00:00Z"
sources=[
 {'id':'official','published_at':'2026-10-01T00:00:00Z','text':'Bluecrate opened 4 offices. Revenue reached 120 units.'},
 {'id':'audit','published_at':'2026-10-02T00:00:00Z','text':'Bluecrate opened 3 offices. The reported total was revised.'},
 {'id':'future','published_at':'2026-11-02T00:00:00Z','text':'Bluecrate opened 6 offices.'},
 {'id':'news','published_at':'2026-10-03T00:00:00Z','text':'The audit says there were 3 offices.'}
]
def ev(s,q,stance='supports'):return {'source_id':s,'quote':q,'stance':stance}
def cl(i,*e):return {'id':i,'evidence':list(e)}
tests=[]
def test(name,fn):
 try:fn();tests.append({'name':name,'pass':True,'points':10})
 except Exception as x:tests.append({'name':name,'pass':False,'points':0,'error':repr(x)})
def result(c,src=sources,day=DAY):return verify([c],src,day)[0]
def t_supported():
 r=result(cl('a',ev('official','Revenue reached 120 units.')))
 assert r['status']=='SUPPORTED' and r['supporting_evidence'][0]['source_id']=='official'
def t_refuted():
 assert result(cl('b',ev('audit','Bluecrate opened 3 offices.','refutes')))['status']=='REFUTED'
def t_conflict():
 r=result(cl('c',ev('official','Bluecrate opened 4 offices.'),ev('audit','Bluecrate opened 3 offices.','refutes')))
 assert r['status']=='CONFLICTED' and len(r['refuting_evidence'])==1
def t_missing_source():
 r=result(cl('d',ev('ghost','missing quote')))
 assert r['status']=='UNVERIFIED' and r['excluded_evidence'][0]['reason']=='missing source'
def t_bad_quote():
 r=result(cl('e',ev('official','Revenue reached 999 units.')))
 assert r['status']=='UNVERIFIED' and r['excluded_evidence'][0]['reason']=='quote not found'
def t_future():
 r=result(cl('f',ev('future','Bluecrate opened 6 offices.')))
 assert r['status']=='UNVERIFIED' and r['excluded_evidence'][0]['reason']=='future source'
def t_asof_boundary():
 assert result(cl('g',ev('future','Bluecrate opened 6 offices.')),day='2026-11-02T00:00:00Z')['status']=='SUPPORTED'
def t_duplicate_source():
 try:result(cl('h'),sources+[sources[0]])
 except ValueError:return
 raise AssertionError('duplicate ID accepted')
def t_invalid_date():
 try:result(cl('i',ev('official','Bluecrate opened 4 offices.')),day='not-a-date')
 except ValueError:return
 raise AssertionError('bad date accepted')
def t_mixed():
 claims=[cl('1',ev('official','Bluecrate opened 4 offices.')),cl('2',ev('audit','Bluecrate opened 3 offices.','refutes')),cl('3',ev('news','The audit says there were 3 offices.'),ev('future','Bluecrate opened 6 offices.','refutes'))]
 out=verify(claims,sources,DAY)
 assert [x['status'] for x in out]==['SUPPORTED','REFUTED','SUPPORTED']
for name,fn in [('verbatim supporting evidence',t_supported),('explicit refutation',t_refuted),('conflicting evidence retained',t_conflict),('missing source exclusion',t_missing_source),('fabricated quote exclusion',t_bad_quote),('future-dated source exclusion',t_future),('as-of boundary inclusion',t_asof_boundary),('duplicate source rejection',t_duplicate_source),('invalid date rejection',t_invalid_date),('multi-claim provenance',t_mixed)]:test(name,fn)
report={'assessment':'PennyLab Research & Evidence Verification v1','classification':'Internal assistant-authored synthetic test, not official pact0 or third-party certification','score':sum(x['points'] for x in tests),'possible':100,'tests':tests}
pathlib.Path(__file__).with_name('report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
