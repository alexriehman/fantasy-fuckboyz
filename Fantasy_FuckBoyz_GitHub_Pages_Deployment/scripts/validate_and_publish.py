#!/usr/bin/env python3
"""Validate a full replacement dashboard JSON, then publish a matching dashboard.js. Only finalized weeks accepted."""
import json, sys, pathlib, collections, math
p=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else 'data/dashboard.json')
d=json.loads(p.read_text())
assert isinstance(d.get('league'),list) and len(d['league'])==12, 'Expected 12 teams'
assert isinstance(d.get('weekly'),list), 'Missing weekly records'
assert len(set(r['manager'] for r in d['league']))==12,'Duplicate managers'
byweek=collections.defaultdict(list)
for r in d['weekly']:
 if r.get('year')==2026:
  byweek[int(r['week'])].append(r)
  assert math.isfinite(float(r['pf'])) and math.isfinite(float(r['pa'])),'Invalid score'
for week,rows in sorted(byweek.items()):
 assert len(rows)==12, f'Week {week} has {len(rows)} teams (expected 12)'
 assert len({r['manager'] for r in rows})==12,f'Week {week} has duplicate team'
 for r in rows:
  peer=next((x for x in rows if x['manager']==r['opponent']),None)
  assert peer and abs(float(peer['pf'])-float(r['pa']))<.011,f'Week {week} opponent score mismatch: {r["manager"]}'
for r in d['league']:
 rows=[x for x in d['weekly'] if x.get('year')==2026 and x['manager']==r['manager']]
 assert len(rows)==int(r['wins'])+int(r['losses']),f'Incomplete 2026 history: {r["manager"]}'
 assert abs(sum(float(x['pf']) for x in rows)-float(r['pf']))<.011,f'PF mismatch: {r["manager"]}'
 assert abs(sum(float(x['pa']) for x in rows)-float(r['pa']))<.011,f'PA mismatch: {r["manager"]}'
js=p.parent/'dashboard.js'
js.write_text('window.FFB_DB='+json.dumps(d,ensure_ascii=False,separators=(',',':'))+';\n')
print('Validated:',len(byweek),'completed weeks,',len(d['league']),'teams,',len(d['weekly']),'weekly entries')
