export const routes={automation:'/api/automation',sandbox:'/api/sandbox',model:'/api/model',modelConsole:'/api/model-console'};
export async function request(path,token,{method='GET',body,key,raw=false,signal}={}){
 const r=await fetch(path,{method,signal,headers:{Authorization:`Bearer ${token}`,...(body?{'Content-Type':'application/json'}:{}),...(key?{'Idempotency-Key':key}:{})},body:body?JSON.stringify(body):undefined});
 if(!r.ok){let d;try{d=await r.json();}catch{}throw new Error(d?.error||`HTTP_${r.status}`);}return raw?r.blob():r.json();
}
export function newId(cryptoApi=globalThis.crypto){if(typeof cryptoApi.randomUUID==='function')return cryptoApi.randomUUID();const b=cryptoApi.getRandomValues(new Uint8Array(16));b[6]=(b[6]&15)|64;b[8]=(b[8]&63)|128;const h=[...b].map(x=>x.toString(16).padStart(2,'0')).join('');return `${h.slice(0,8)}-${h.slice(8,12)}-${h.slice(12,16)}-${h.slice(16,20)}-${h.slice(20)}`;}
export const terminal=s=>['SUCCEEDED','FAILED','CANCELLED','TIMED_OUT','LOST'].includes(s);
export const short=id=>id?id.slice(0,8):'—';
export const formatTime=v=>v?new Date(v).toLocaleString('zh-CN',{month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit'}):'—';
export const formatSize=n=>n>1048576?`${(n/1048576).toFixed(1)} MB`:n>1024?`${(n/1024).toFixed(1)} KB`:`${n||0} B`;
export async function download(path,token,name){const blob=await request(path,token,{raw:true});const url=URL.createObjectURL(blob);const link=document.createElement('a');link.href=url;link.download=name;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
