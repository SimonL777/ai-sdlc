import {defineConfig} from 'vite';
export default defineConfig({server:{port:5173,proxy:{
 '/api/automation':{target:'http://127.0.0.1:8083',rewrite:p=>p.replace('/api/automation','/api')},
 '/api/sandbox':{target:'http://127.0.0.1:8081',rewrite:p=>p.replace('/api/sandbox','/api')},
 '/api/model':{target:'http://127.0.0.1:8082',rewrite:p=>p.replace('/api/model','/v1')},
 '/health/automation':{target:'http://127.0.0.1:8083',rewrite:()=>'/actuator/health'},
 '/health/sandbox':{target:'http://127.0.0.1:8081',rewrite:()=>'/actuator/health'},
 '/health/model':{target:'http://127.0.0.1:8082',rewrite:()=>'/actuator/health'}
}}});
