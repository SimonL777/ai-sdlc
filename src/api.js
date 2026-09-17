export async function request(path,token,{method='GET',body,key,raw=false,signal}={}){
 const response=await fetch(path,{method,signal,headers:{Authorization:`Bearer ${token}`,...(body?{'Content-Type':'application/json'}:{}),...(key?{'Idempotency-Key':key}:{})},body:body?JSON.stringify(body):undefined});
 if(!response.ok){let detail;try{detail=await response.json();}catch{}throw new Error(detail?.error||`HTTP_${response.status}`);}
 return raw?response.blob():response.json();
}
export function terminal(status){return ['SUCCEEDED','FAILED','CANCELLED','TIMED_OUT','LOST'].includes(status);}
export function short(id){return id?id.slice(0,8):'—';}
