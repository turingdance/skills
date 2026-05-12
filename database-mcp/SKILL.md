---
title: "database-mcp"
summary: "使用 database-mcp 进行数据库操作的专业指南"
agent_created: true
---

# database-mcp 使用指南

## 获取与安装

### 方式一：直接运行（推荐，无需安装）

```bash
# 直接执行，无需安装
npx @turingdance/database-mcp

# 或指定数据库环境变量
DB_TYPE=mysql DB_HOST=localhost DB_USER=root DB_PASSWORD=123456 DB_NAME=test npx @turingdance/database-mcp
```

### 方式二：本地安装

```bash
# 全局安装
npm install -g @turingdance/database-mcp

# 或在项目中安装
npm install @turingdance/database-mcp
```

### 方式三：本地运行源码

```bash
git clone https://github.com/turingdance/database-mcp.git
cd database-mcp
npm install
npm start
```

### WorkBuddy / Claude Desktop 配置

将以下配置写入 `~/.workbuddy/mcp.json` 或 Claude Desktop 的 MCP 配置文件：

```json
{
  "mcpServers": {
    "database-mcp": {
      "command": "npx",
      "args": ["-y", "@turingdance/database-mcp"],
      "env": {
        "DB_TYPE": "mysql",
        "DB_HOST": "127.0.0.1",
        "DB_PORT": "3306",
        "DB_USER": "root",
        "DB_PASSWORD": "your_password",
        "DB_NAME": "your_database"
      }
    }
  }
}
```

---

## 工具列表

database-mcp 提供 5 个 MCP 工具，涵盖数据库查询与操作的全流程：

| 工具 | 用途 | 风险 | 说明 |
|---|---|---|---|
| `connect_db` | 测试连接 | 低 | 验证数据库连通性 |
| `list_tables` | 列出所有表 | 低 | 获取数据库表清单 |
| `describe_table` | 查看表结构 | 低 | 获取字段、类型、约束信息 |
| `query` | SELECT 查询 | 低 | 只读查询，参数化防注入 |
| `execute` | 写操作 | 按语句分级 | INSERT/UPDATE/DELETE/DROP 等，需 confirm |

---

## 工作流程

### 1. 连接测试（必做）

```
"测试数据库连接"
```

先用 `connect_db` 确认连接正常，再进行后续操作。

### 2. 探索数据库

```
"列出所有表"
"查看 users 表的结构"
"查看 orders 表有哪些字段"
```

### 3. 数据查询

```
"查询 users 表的前10条数据"
"统计 orders 表的总记录数"
"查看 product_category='电子产品' 的商品"
```

### 4. 数据操作（需确认）

写操作（INSERT/UPDATE/DELETE）默认被拦截，需要传入 `confirm: true`：

```json
{
  "tool": "execute",
  "arguments": {
    "sql": "INSERT INTO users (name, email) VALUES ('张三', 'zhangsan@example.com')",
    "confirm": true,
    "reason": "添加测试用户数据"
  }
}
```

---

## 风险分级

| 等级 | 关键字 | 行为 |
|---|---|---|
| **高危** | DROP, TRUNCATE, ALTER | 需 `confirm: true`，服务端记录日志 |
| **中危** | INSERT, DELETE, UPDATE, REPLACE, RENAME, GRANT, REVOKE | 需 `confirm: true` |
| **低危** | SELECT, SHOW, DESCRIBE, PRAGMA 等 | 直接执行 |

### 未确认拦截示例

```json
{
  "status": "rejected",
  "risk_level": "medium",
  "message": "检测到中危（数据变更）操作 [INSERT]，必须传入 confirm: true 才能执行。"
}
```

---

## 环境变量配置

| 变量 | 说明 | 默认值 |
|---|---|---|
| `DB_TYPE` | mysql / mariadb / tidb / postgresql / sqlite / oracle / sqlserver | sqlite |
| `DB_HOST` | 主机地址 | localhost |
| `DB_PORT` | 端口 | 数据库默认 |
| `DB_USER` | 用户名 | - |
| `DB_PASSWORD` | 密码 | - |
| `DB_NAME` | 数据库名（SQLite 无需） | mcp-db |
| `DB_FILE` | SQLite 文件路径 | mcp.db |

### MySQL 示例

```bash
DB_TYPE=mysql DB_HOST=localhost DB_USER=root DB_PASSWORD=xxx DB_NAME=test npx @turingdance/database-mcp
```

### PostgreSQL 示例

```bash
DB_TYPE=postgresql DB_HOST=localhost DB_USER=postgres DB_PASSWORD=xxx DB_NAME=test npx @turingdance/database-mcp
```

### SQLite 示例

```bash
DB_TYPE=sqlite DB_FILE=/path/to/database.db npx @turingdance/database-mcp
```

---

## SQL 编写规范

### 1. 参数化查询（防注入）

```sql
-- ✅ 推荐：使用参数
SELECT * FROM users WHERE email = ?
SELECT * FROM orders WHERE status = ? AND created_at > ?

-- ❌ 避免：字符串拼接
SELECT * FROM users WHERE email = '" + email + "'
```

### 2. 只查询需要的字段

```sql
-- ✅ 推荐
SELECT id, name, email FROM users WHERE status = 'active'

-- ❌ 避免
SELECT * FROM users
```

### 3. 写操作前先查询确认

```
"先查看 users 表有哪些字段"
"再查询一条现有数据确认格式"
"最后执行 INSERT"
```

---

## 常见场景

### 场景 1：新增数据

1. 先 `describe_table` 了解表结构
2. 再 `query` 看一条现有数据作为参考
3. 最后 `execute` 插入数据（带 confirm）

### 场景 2：批量更新

1. 先用 `query` 预览影响范围
2. 确认无误后 `execute` 执行 UPDATE

### 场景 3：删除数据

1. 先用 `query` 预览要删除的数据
2. 使用 `WHERE` 条件而非无条件的 DELETE
3. 执行时务必 `confirm: true`

---

## 故障排除

| 问题 | 解决方案 |
|---|---|
| 连接失败 | 检查 DB_HOST、DB_PORT、用户名密码是否正确 |
| 表不存在 | 确认 DB_NAME 是否正确，用 `list_tables` 验证 |
| 参数化失败 | 检查参数类型，确保与字段类型匹配 |
| 写操作被拦截 | 这是安全机制！确认无误后传入 `confirm: true` |

---

## 安全提醒

1. **永远不要**在不确认的情况下执行 `DROP TABLE` 或 `TRUNCATE`
2. **永远不要**在生产环境使用 `confirm: true` 执行未经测试的 SQL
3. **始终先查询预览**，再执行写操作
4. **使用参数化查询**，避免 SQL 注入风险