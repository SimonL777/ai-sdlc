# API-001 · 查询商品目录

- 前置条件：内置 Northstar 环境已启动。
- 操作：GET /api/products。
- 预期：状态 200，total 为 3，第一个商品为 Mechanical Keyboard。

```json
{"version":2,"target":"api:todo-demo","steps":[{"op":"request","target":"GET","value":"{\"path\":\"/api/products\"}"},{"op":"assertStatus","target":"response","value":"200"},{"op":"assertJson","target":"$.total","value":"3"}]}
```
