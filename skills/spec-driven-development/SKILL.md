---
name: spec-driven-development
description: 规格驱动开发 — 先写规格再写代码。适用于：开始新项目/功能、需求不明确、涉及多文件改动、架构决策、需要 30 分钟以上实现的任务。不适用于：单行修复、明确的改动。
---

# Spec-Driven Development（规格驱动开发）

## Overview

**先写结构化规格，再写任何代码。** 规格是 AI 与人类的共同真相来源——定义我们在构建什么、为什么、以及如何判断完成。没有规格的代码是在猜测。

## When to Use

- 开始新项目或功能
- 需求模糊或不完整
- 改动涉及多个文件或模块
- 需要做架构决策
- 任务需要 30 分钟以上实现

**When NOT to use:** 单行修复、拼写错误修正、需求明确且自包含的改动。

## The Gated Workflow（四阶段门控）

```
SPECIFY ──→ PLAN ──→ TASKS ──→ IMPLEMENT
   │          │        │          │
   ▼          ▼        ▼          ▼
 Human      Human    Human      Human
 reviews    reviews  reviews    reviews
```

### Phase 1: Specify（规格化）

从高层愿景开始。提出澄清问题，直到需求具体化。

**立即暴露假设。** 在写规格内容之前，列出你的假设：

```
我正在做的假设：
1. 这是一个 Web 应用（不是原生移动端）
2. 使用 session-based cookies 认证（不是 JWT）
3. 数据库是 PostgreSQL（基于现有 Prisma schema）
4. 只针对现代浏览器（不支持 IE11）
→ 如果有误请立即纠正。
```

**规格文档覆盖六个核心区域：**

1. **Objective** — 我们在构建什么，为什么？用户是谁？成功是什么样？

2. **Commands** — 完整可执行命令（含参数），不只是工具名
   ```
   Build: npm run build
   Test: npm test -- --coverage
   Lint: npm run lint --fix
   Dev: npm run dev
   ```

3. **Project Structure** — 源码位置、测试位置、文档位置
   ```
   src/           → 应用源码
   src/components → React 组件
   src/lib        → 共享工具
   tests/         → 单元和集成测试
   e2e/           → 端到端测试
   docs/          → 文档
   ```

4. **Code Style** — 一个真实的代码片段胜过三段描述。包含命名规范、格式化规则、良好输出示例。

5. **Testing Strategy** — 测试框架、测试位置、覆盖率期望、测试级别。

6. **Boundaries** — 三层系统：
   - **Always do:** 运行测试前提交、遵循命名规范、验证输入
   - **Ask first:** 数据库 schema 变更、添加依赖、修改 CI 配置
   - **Never do:** 提交 secrets、编辑 vendor 目录、移除失败测试

**规格模板：**

```markdown
# Spec: [项目/功能名称]

## Objective
[我们在构建什么，为什么。用户故事或验收标准。]

## Tech Stack
[框架、语言、带版本的关键依赖]

## Commands
[Build, test, lint, dev — 完整命令]

## Project Structure
[带描述的目录布局]

## Code Style
[示例片段 + 关键规范]

## Testing Strategy
[框架、测试位置、覆盖率要求、测试级别]

## Boundaries
- Always: [...]
- Ask first: [...]
- Never: [...]

## Success Criteria
[如何判断完成 — 具体、可测试的条件]

## Open Questions
[需要人工输入的任何未解决问题]
```

**将需求重新框定为成功标准：**

```
需求："让仪表盘更快"

重新框定的成功标准：
- 仪表盘 LCP < 2.5s（4G 连接）
- 初始数据加载 < 500ms
- 加载期间无布局偏移（CLS < 0.1）
→ 这些是正确目标吗？
```

### Phase 2: Plan（计划）

使用验证后的规格，生成技术实现计划：

1. 识别主要组件及其依赖关系
2. 确定实现顺序（什么必须先构建）
3. 记录风险和缓解策略
4. 识别可并行 vs 必须顺序的部分
5. 定义阶段间的验证检查点

### Phase 3: Tasks（任务）

将计划分解为离散、可实现的任务：

- 每个任务应在单次聚焦会话中完成
- 每个任务有明确的验收标准
- 每个任务包含验证步骤（测试、构建、手动检查）
- 任务按依赖排序，非按感知重要性
- 无任务应涉及超过 ~5 个文件

**任务模板：**
```markdown
- [ ] Task: [描述]
  - Acceptance: [完成时必须为真]
  - Verify: [如何确认 — 测试命令、构建、手动检查]
  - Files: [将修改的文件]
```

### Phase 4: Implement（实现）

按照 `incremental-implementation` 和 `test-driven-development` 技能一次执行一个任务。使用 `context-engineering` 在每个步骤加载正确的规格部分和源文件，而非向 AI 灌输整个规格。

## Keeping the Spec Alive

规格是活文档，不是一次性产物：

- **变更决策时更新** — 如果发现数据模型需要变更，先更新规格，再实现。
- **范围变更时更新** — 增加或删除的功能应反映在规格中。
- **提交规格** — 规格与代码一起属于版本控制。
- **PR 中引用规格** — 链接回每个 PR 实现的部分规格。

## Common Rationalizations

| Rationalization | Reality |
|-----------------|---------|
| "这很简单，不需要规格" | 简单任务不需要*长*规格，但仍然需要验收标准。两行规格就够了。 |
| "我代码写完再写规格" | 那是文档，不是规格。规格的价值在于*之前*强制澄清。 |
| "规格会拖慢我们" | 15 分钟规格防止数小时返工。15 分钟瀑布流优于 15 小时调试。 |
| "需求反正会变" | 这就是规格是活文档的原因。过时的规格仍然好过没有规格。 |
| "用户知道他们想要什么" | 即使是清晰的请求也有隐含假设。规格暴露这些假设。 |

## Red Flags

- 在没有任何书面需求的情况下开始写代码
- 在澄清"完成"意味着什么之前问"我可以开始构建吗"
- 实现未在任何规格或任务列表中提到的功能
- 不记录文档就做架构决策
- 因为"很明显要构建什么"而跳过规格

## Verification

在进入实现之前，确认：

- [ ] 规格覆盖所有六个核心区域
- [ ] 人类已审查并批准规格
- [ ] 成功标准具体且可测试
- [ ] Boundaries（Always/Ask First/Never）已定义
- [ ] 规格已保存到仓库中的文件

---

**来源**: [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) - spec-driven-development
