#!/usr/bin/env python3
"""Explicit runtime check. Prints IDs and proof, never tokens."""
from pathlib import Path
import argparse,json,time,urllib.request,uuid
p=argparse.ArgumentParser();p.add_argument('--base-url',default='http://127.0.0.1:8098');p.add_argument('--negative',action='store_true');args=p.parse_args()
env=Path(__file__).resolve().parent/'.env';d={k:v for line in env.read_text().splitlines() if line and not line.startswith('#') and '=' in line for k,v in [line.split('=',1)]}
token=d['API_TOKEN'];base=args.base_url.rstrip('/')
def call(path,body=None,key=None):
 headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'}
 if key:headers['Idempotency-Key']=key
 req=urllib.request.Request(base+path,data=json.dumps(body).encode() if body is not None else None,headers=headers)
 with urllib.request.urlopen(req,timeout=20) as r:return json.load(r)
body={'requirement':'Add a task called Prepare interview to the synthetic task list and assert that it is visible.'}
if args.negative:body={'workflow':{'version':1,'target':'todo-demo','steps':[{'op':'fill','target':'title','value':'Actual task'},{'op':'click','target':'add','value':None},{'op':'assertText','target':'items','value':'This text must not exist'}]}}
key=str(uuid.uuid4());created=call('/api/automation/runs',body,key);run_id=created['id']
assert call('/api/automation/runs',body,key)['id']==run_id,'Idempotency replay created a second run'
end=time.monotonic()+240
while time.monotonic()<end:
 run=call('/api/automation/runs/'+run_id)
 if run['status'] not in ['QUEUED','RUNNING']:break
 time.sleep(2)
else:raise SystemExit('Smoke timed out; runId='+run_id)
expected='FAILED' if args.negative else 'SUCCEEDED'
assert run['status']==expected,json.dumps({'runId':run_id,'status':run['status'],'error':run.get('error')})
execution_id=run['remoteId'];execution=call('/api/sandbox/executions/'+execution_id)
for _ in range(15):
 if execution['cleanupStatus']=='DESTROYED':break
 time.sleep(1);execution=call('/api/sandbox/executions/'+execution_id)
assert execution['cleanupStatus']=='DESTROYED','Container cleanup not verified'
result=run['result'];assert result['report']['passed'] is (not args.negative)
assert result['report']['specHash']==result['specHash'],'Compiler/runner artifact hash mismatch'
print(json.dumps({'runId':run_id,'executionId':execution_id,'status':run['status'],'providerMode':result['providerMode'],'reportPassed':result['report']['passed'],'cleanup':execution['cleanupStatus'],'idempotentReplay':True,'specHashVerified':True},indent=2))
