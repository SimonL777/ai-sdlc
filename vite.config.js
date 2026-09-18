import {defineConfig} from 'vite';
export default defineConfig({base:'./',server:{port:5173,proxy:{
 '/api/automation':{target:'http://127.0.0.1:8083',rewrite:p=>p.replace('/api/automation','/api')},
 '/api/sandbox':{target:'http://127.0.0.1:8081',rewrite:p=>p.replace('/api/sandbox','/api')},
 '/api/model-console':{target:'http://127.0.0.1:8082',rewrite:p=>p.replace('/api/model-console','/api')},
 '/api/model':{target:'http://127.0.0.1:8082',rewrite:p=>p.replace('/api/model','/v1')}
}}});
