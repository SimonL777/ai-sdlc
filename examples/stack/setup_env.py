#!/usr/bin/env python3
"""Create private configuration; never print generated credentials."""
from pathlib import Path
import argparse,os,secrets
p=argparse.ArgumentParser();p.add_argument('--local',action='store_true',help='Explicit H2/local-artifact development mode');p.add_argument('--layout',choices=['independent','two-project-demo'],default='independent');args=p.parse_args()
root=Path(__file__).resolve().parent;target=root/'.env'
if target.exists():raise SystemExit('.env already exists; preserve it and edit explicitly.')
values={name:secrets.token_urlsafe(36) for name in ['API_TOKEN','SANDBOX_SERVICE_TOKEN','MODEL_SERVICE_TOKEN','AUTOMATION_SERVICE_TOKEN']}
values['SUPABASE_LAYOUT']=args.layout
if args.layout=='two-project-demo':
 for prefix in ['SANDBOX','MODEL']:
  values[prefix+'_DATABASE_URL']='jdbc:postgresql://YOUR_INFRA_DB_HOST:5432/postgres?sslmode=require'
  values[prefix+'_SUPABASE_URL']='https://YOUR_INFRA_PROJECT.supabase.co'
 values['AUTOMATION_DATABASE_URL']='jdbc:postgresql://YOUR_APP_DB_HOST:5432/postgres?sslmode=require'
 values['AUTOMATION_SUPABASE_URL']='https://YOUR_APP_PROJECT.supabase.co'
 values['AI_SDLC_SUPABASE_URL']='https://YOUR_APP_PROJECT.supabase.co'
socket=Path('/var/run/docker.sock');values['DOCKER_GID']=str(socket.stat().st_gid) if socket.exists() else 'SET_ON_DOCKER_HOST'
if args.local:
 values.update(SPRING_PROFILES_ACTIVE='local',ARTIFACT_MODE='local',AI_SDLC_SUPABASE_URL='',AI_SDLC_SUPABASE_ANON_KEY='')
 for prefix in ['SANDBOX','MODEL','AUTOMATION']:
  for suffix in ['DATABASE_URL','DATABASE_USER','DATABASE_PASSWORD','SUPABASE_URL','SUPABASE_SERVICE_ROLE_KEY']:values[prefix+'_'+suffix]=''
lines=[]
for line in (root/'.env.example').read_text().splitlines():
 if '=' in line and not line.startswith('#'):
  key=line.split('=',1)[0]
  if key in values:line=key+'='+values[key]
 lines.append(line)
fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
with os.fdopen(fd,'w') as f:f.write('\n'.join(lines)+'\n')
print('Created private .env. Fill Supabase/provider settings and verify DOCKER_GID. Credentials were not printed.')
