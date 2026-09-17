const base=Deno.env.get('SUPABASE_URL')!;
const anon=Deno.env.get('SUPABASE_ANON_KEY')!;
const serviceKey=Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const cors={'Access-Control-Allow-Origin':Deno.env.get('APP_ORIGIN')||'*','Access-Control-Allow-Headers':'authorization,apikey,content-type','Access-Control-Allow-Methods':'POST,OPTIONS'};
function reply(value:unknown,status=200){return new Response(JSON.stringify(value),{status,headers:{...cors,'content-type':'application/json'}});}
Deno.serve(async(req:Request)=>{
 if(req.method==='OPTIONS')return new Response(null,{status:204,headers:cors});
 if(req.method!=='POST')return reply({error:'METHOD_NOT_ALLOWED'},405);
 const authorization=req.headers.get('authorization')||'';
 if(!authorization.startsWith('Bearer '))return reply({error:'AUTH_REQUIRED'},401);
 try {
  const identity=await fetch(base+'/auth/v1/user',{headers:{authorization,apikey:anon},signal:AbortSignal.timeout(10000)});
  if(!identity.ok)return reply({error:'AUTH_REQUIRED'},401);const user=await identity.json();
  const text=await req.text();if(text.length>20000)return reply({error:'BODY_TOO_LARGE'},413);const data=JSON.parse(text);
  const headers={authorization,apikey:anon,'content-type':'application/json',Prefer:'return=representation'};
  let response:Response;
  if(data.action==='create'){
   if(typeof data.title!=='string'||!data.title.trim()||data.title.length>80||typeof data.requirement!=='string'||!data.requirement.trim()||data.requirement.length>8000)return reply({error:'INVALID_MATERIAL'},422);
   const digest=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(data.requirement));const source_hash=[...new Uint8Array(digest)].map(v=>v.toString(16).padStart(2,'0')).join('');
   response=await fetch(base+'/rest/v1/sdlc_workspaces',{method:'POST',headers:{...headers,authorization:'Bearer '+serviceKey,apikey:serviceKey},body:JSON.stringify({owner_id:user.id,title:data.title,requirement:data.requirement,source_hash}),signal:AbortSignal.timeout(10000)});
  } else if(data.action==='attach'){
   const uuid=/^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/i;if(!uuid.test(data.id)||!uuid.test(data.runId))return reply({error:'INVALID_REFERENCE'},422);
   response=await fetch(base+'/rest/v1/sdlc_workspaces?id=eq.'+data.id,{method:'PATCH',headers,body:JSON.stringify({automation_run_id:data.runId}),signal:AbortSignal.timeout(10000)});
  } else if(data.action==='list')response=await fetch(base+'/rest/v1/sdlc_workspaces?select=*&order=created_at.desc&limit=50',{headers,signal:AbortSignal.timeout(10000)});
  else return reply({error:'UNKNOWN_ACTION'},422);
  if(!response.ok)return reply({error:'WORKSPACE_STORAGE_FAILED'},502);const rows=await response.json();
  if(data.action==='list')return reply(rows);if(!rows.length)return reply({error:'NOT_FOUND'},404);return reply(rows[0],data.action==='create'?201:200);
 }catch{return reply({error:'WORKSPACE_REQUEST_FAILED'},400);}
});
