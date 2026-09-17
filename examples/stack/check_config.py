#!/usr/bin/env python3
"""Validate explicit project boundaries without printing private values."""
from pathlib import Path
import sys

def validate(d):
 errors=[]
 layout=d.get('SUPABASE_LAYOUT','independent')
 if layout not in {'independent','two-project-demo'}:errors.append('Unknown SUPABASE_LAYOUT')
 for k in ['API_TOKEN','SANDBOX_SERVICE_TOKEN','MODEL_SERVICE_TOKEN','AUTOMATION_SERVICE_TOKEN']:
  if len(d.get(k,''))<24:errors.append(k+' must be a strong random value')
 if len({d.get(k) for k in ['SANDBOX_SERVICE_TOKEN','MODEL_SERVICE_TOKEN','AUTOMATION_SERVICE_TOKEN']})<3:errors.append('Service credentials must be distinct')
 if not d.get('DOCKER_GID','').isdigit():errors.append('Set DOCKER_GID on the Docker host')
 if d.get('SPRING_PROFILES_ACTIVE')!='local':
  for prefix in ['SANDBOX','MODEL','AUTOMATION']:
   for suffix in ['DATABASE_URL','DATABASE_USER','DATABASE_PASSWORD','SUPABASE_URL']:
    k=prefix+'_'+suffix
    if not d.get(k) or 'YOUR_' in d[k]:errors.append(k+' must be configured')
  for k in ['SANDBOX_SUPABASE_SERVICE_ROLE_KEY','AUTOMATION_SUPABASE_SERVICE_ROLE_KEY','AI_SDLC_SUPABASE_URL']:
   if not d.get(k) or 'YOUR_' in d[k]:errors.append(k+' must be configured')
  projects=[d.get(prefix+'_SUPABASE_URL','').rstrip('/') for prefix in ['SANDBOX','MODEL','AUTOMATION','AI_SDLC']]
  if any(not u.startswith('https://') for u in projects):errors.append('Supabase project URLs must use HTTPS')
  databases=[(d.get(prefix+'_DATABASE_URL'),d.get(prefix+'_DATABASE_USER')) for prefix in ['SANDBOX','MODEL','AUTOMATION']]
  if layout=='independent':
   if len(set(projects))<4:errors.append('Use four distinct Supabase project URLs')
   if len(set(databases))<3:errors.append('Java services must not reuse an identical database connection identity')
  elif layout=='two-project-demo':
   if projects[0]!=projects[1] or projects[2]!=projects[3] or projects[0]==projects[2]:errors.append('Two-project demo requires Sandbox+Model in project A and Automation+AI-SDLC in a distinct project B')
   if databases[2] in databases[:2]:errors.append('Infrastructure and application groups must not share a database connection identity')
  if d.get('ARTIFACT_MODE')!='supabase':errors.append('Production artifacts must use Supabase Storage')
  if d.get('SANDBOX_SUPABASE_SERVICE_ROLE_KEY')==d.get('AUTOMATION_SUPABASE_SERVICE_ROLE_KEY'):errors.append('Do not reuse project service-role keys')
 if d.get('MODEL_MODE')=='upstream':
  for k in ['MODEL_BASE_URL','MODEL_API_KEY','MODEL_NAME']:
   if not d.get(k):errors.append(k+' required for upstream mode')
  if not d.get('MODEL_BASE_URL','').startswith('https://'):errors.append('MODEL_BASE_URL must use HTTPS')
 return errors

def read_env(path):
 return {k:v.strip().strip("\"'") for line in path.read_text().splitlines() if line and not line.startswith('#') and '=' in line for k,v in [line.split('=',1)]}

if __name__=='__main__':
 p=Path(__file__).resolve().parent/'.env'
 if not p.exists():raise SystemExit('Missing .env; run setup_env.py')
 errors=validate(read_env(p))
 if errors:print('\n'.join(errors));sys.exit(1)
 print('Configuration boundaries valid; network and runtime still require verification.')
