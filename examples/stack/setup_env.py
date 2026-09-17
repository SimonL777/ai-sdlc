#!/usr/bin/env python3
"""Create private configuration; never print generated credentials."""
from pathlib import Path
import argparse,os,secrets
p=argparse.ArgumentParser();p.add_argument('--local',action='store_true',help='Explicit H2/local-artifact development mode');args=p.parse_args()
root=Path(__file__).resolve().parent;target=root/'.env'
if target.exists():raise SystemExit('.env already exists; preserve it and edit explicitly.')
values={name:secrets.token_urlsafe(36) for name in ['API_TOKEN','SANDBOX_SERVICE_TOKEN','MODEL_SERVICE_TOKEN','AUTOMATION_SERVICE_TOKEN']}
socket=Path('/var/run/docker.sock');values['DOCKER_GID']=str(socket.stat().st_gid) if socket.exists() else 'SET_ON_DOCKER_HOST'
if args.local:values.update(SPRING_PROFILES_ACTIVE='local',ARTIFACT_MODE='local',DATABASE_URL='',DATABASE_USER='',DATABASE_PASSWORD='',SUPABASE_URL='',SUPABASE_SERVICE_ROLE_KEY='')
lines=[]
for line in (root/'.env.example').read_text().splitlines():
 if '=' in line and not line.startswith('#'):
  key=line.split('=',1)[0]
  if key in values:line=key+'='+values[key]
 lines.append(line)
fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
with os.fdopen(fd,'w') as f:f.write('\n'.join(lines)+'\n')
print('Created private .env. Fill Supabase/provider settings and verify DOCKER_GID. Credentials were not printed.')
