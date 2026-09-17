#!/usr/bin/env python3
from pathlib import Path
import sys
p=Path(__file__).resolve().parent/'.env'
if not p.exists():raise SystemExit('Missing .env; run setup_env.py')
d={k:v for line in p.read_text().splitlines() if line and not line.startswith('#') and '=' in line for k,v in [line.split('=',1)]}
errors=[]
for k in ['API_TOKEN','SANDBOX_SERVICE_TOKEN','MODEL_SERVICE_TOKEN','AUTOMATION_SERVICE_TOKEN']:
 if len(d.get(k,''))<24:errors.append(k+' must be set to a strong random value')
if len({d.get(k) for k in ['SANDBOX_SERVICE_TOKEN','MODEL_SERVICE_TOKEN','AUTOMATION_SERVICE_TOKEN']})<3:errors.append('Service credentials must be distinct')
if not d.get('DOCKER_GID','').isdigit():errors.append('Set DOCKER_GID from the Docker socket group on the deployment host')
if d.get('SPRING_PROFILES_ACTIVE')!='local':
 for k in ['DATABASE_URL','DATABASE_USER','DATABASE_PASSWORD','SUPABASE_URL','SUPABASE_SERVICE_ROLE_KEY']:
  if not d.get(k) or 'YOUR_' in d[k]:errors.append(k+' must be configured')
 if d.get('ARTIFACT_MODE')!='supabase':errors.append('NAS production mode requires Supabase artifact storage')
if d.get('MODEL_MODE')=='upstream':
 for k in ['MODEL_BASE_URL','MODEL_API_KEY','MODEL_NAME']:
  if not d.get(k):errors.append(k+' required in upstream mode')
 if not d.get('MODEL_BASE_URL','').startswith('https://'):errors.append('MODEL_BASE_URL must use HTTPS')
if errors:print('\n'.join(errors));sys.exit(1)
print('Configuration structure valid; connectivity and runtime are not yet verified.')
