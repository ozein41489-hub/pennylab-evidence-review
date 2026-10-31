"""PennyLab evidence verification exercise: offline, structured, auditable claims.
Input is synthetic JSON. No web claims or real-world facts are verified.
"""
from datetime import datetime,timezone
from collections import defaultdict

def _date(s):
    try:
        d=datetime.fromisoformat(s.replace("Z","+00:00"))
        if d.tzinfo is None:raise ValueError("timezone required")
        return d.astimezone(timezone.utc)
    except (ValueError,AttributeError,TypeError):
        raise ValueError("invalid publication date")

def verify(claims,sources,as_of):
    cutoff=_date(as_of)
    ids=set()
    for s in sources:
        if not isinstance(s.get('id'),str) or not s['id'] or s['id'] in ids:raise ValueError('duplicate/invalid source id')
        ids.add(s['id'])
    source_map={s['id']:s for s in sources}
    outcome=[]
    for c in claims:
        cid=c.get('id')
        if not isinstance(cid,str) or not cid:raise ValueError('invalid claim id')
        support=[];refute=[];excluded=[]
        for cite in c.get('evidence',[]):
            sid=cite.get('source_id');s=source_map.get(sid)
            if s is None:excluded.append({'source_id':sid,'reason':'missing source'});continue
            if _date(s['published_at'])>cutoff:
                excluded.append({'source_id':sid,'reason':'future source'});continue
            quote=cite.get('quote')
            if not isinstance(quote,str) or not quote or quote not in s.get('text',''):
                excluded.append({'source_id':sid,'reason':'quote not found'});continue
            stance=cite.get('stance')
            if stance not in ('supports','refutes'):
                excluded.append({'source_id':sid,'reason':'invalid stance'});continue
            record={'source_id':sid,'quote':quote}
            (support if stance=='supports' else refute).append(record)
        if support and refute:status='CONFLICTED'
        elif support:status='SUPPORTED'
        elif refute:status='REFUTED'
        else:status='UNVERIFIED'
        outcome.append({'claim_id':cid,'status':status,'supporting_evidence':support,'refuting_evidence':refute,'excluded_evidence':excluded})
    return outcome
