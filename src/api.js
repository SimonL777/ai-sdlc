export async function request(path,token,{method='GET',body,key,raw=false,signal}={}){
 const response=await fetch(path,{method,signal,headers:{Authorization:`Bearer ${token}`,...(body?{'Content-Type':'application/json'}:{}),...(key?{'Idempotency-Key':key}:{})},body:body?JSON.stringify(body):undefined});
 if(!response.ok){let detail;try{detail=await response.json();}catch{}throw new Error(detail?.error||`HTTP_${response.status}`);}
 return raw?response.blob():response.json();
}
export function terminal(status){return ['SUCCEEDED','FAILED','CANCELLED','TIMED_OUT','LOST'].includes(status);}
export function short(id){return id?id.slice(0,8):'—';}

// crypto.randomUUID requires a secure context; NAS LAN HTTP still supports getRandomValues.
export function newId(cryptoApi=globalThis.crypto){
 if(typeof cryptoApi.randomUUID==='function')return cryptoApi.randomUUID();
 const bytes=cryptoApi.getRandomValues(new Uint8Array(16));bytes[6]=(bytes[6]&15)|64;bytes[8]=(bytes[8]&63)|128;
 const hex=[...bytes].map(b=>b.toString(16).padStart(2,'0')).join('');
 return `${hex.slice(0,8)}-${hex.slice(8,12)}-${hex.slice(12,16)}-${hex.slice(16,20)}-${hex.slice(20)}`;
}
