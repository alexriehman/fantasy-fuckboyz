#!/usr/bin/env python3
"""Fetch full authoritative dashboard JSON from a separately deployed authenticated endpoint.
This is an integration adapter, NOT a direct Flaim API client.
If no endpoint configured, leave published data unchanged.
"""
import os,sys,json,urllib.request,pathlib
url=os.environ.get('FFB_DATA_ENDPOINT','').strip()
if not url:
 print('No FFB_DATA_ENDPOINT configured; retaining last validated dashboard. See README.md.')
 sys.exit(0)
if not url.startswith('https://'):
 raise SystemExit('FFB_DATA_ENDPOINT must be HTTPS')
headers={'Accept':'application/json','User-Agent':'fantasy-fuckboyz-pages/1.0'}
if os.environ.get('FFB_DATA_TOKEN'):
 headers['Authorization']='Bearer '+os.environ['FFB_DATA_TOKEN']
with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=40) as response:
 payload=response.read(5_000_000)
data=json.loads(payload)
assert isinstance(data,dict) and 'league' in data and 'weekly' in data
pathlib.Path('data/dashboard.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':')))
print('Downloaded candidate snapshot; validation follows')
