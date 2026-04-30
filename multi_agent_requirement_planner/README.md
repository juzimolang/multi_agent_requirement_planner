# Multi-Agent Requirement Planner

一个可直接运行的多 Agent 需求评审材料生成器。它把产品需求文本转成结构化技术评审材料，包含：

- 需求分析
- 架构方案
- 风险评估
- 测试计划
- Markdown 评审文档
- JSON 结构化输出

默认支持 `mock` 模式，不需要 API Key，适合演示、评审和本地测试。也支持 OpenAI live 模式。

## 目录结构

```text
multi_agent_requirement_planner/
├── agents.py                  # Mock Agent 与 OpenAI Agent Runner
├── app.py                     # FastAPI Web/API 服务
├── models.py                  # Pydantic 数据模型
├── report.py                  # Markdown 渲染
├── run_cli.py                 # 命令行入口
├── sample_requirement.txt     # 示例需求
├── requirements.txt           # Python 依赖
├── .env.example               # 环境变量示例
├── tests/                     # 测试用例
└── outputs/                   # 输出目录
```

## 快速开始

```bash
cd multi_agent_requirement_planner
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## CLI 运行：mock 模式

```bash
python run_cli.py --input sample_requirement.txt --mock --out outputs/review.md --json outputs/result.json
```

运行后会生成：

- `outputs/review.md`
- `outputs/result.json`

## Web 运行

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

浏览器打开：

```text
http://localhost:8000
```

API 调用：

```bash
curl -X POST http://localhost:8000/plan \
  -H 'Content-Type: application/json' \
  -d '{"requirement":"做一个把需求转成技术评审材料的多 Agent 工具。","mock":true}'
```

## OpenAI live 模式

复制环境变量文件：

```bash
cp .env.example .env
```

编辑 `.env`：

```text
OPENAI_API_KEY=你的 API Key
OPENAI_MODEL=gpt-4.1-mini
```

运行时去掉 `--mock`：

```bash
python run_cli.py --input sample_requirement.txt --out outputs/review.md --json outputs/result.json
```

Web 页面里取消勾选“使用 mock 模式”即可走 live 模式。

## 测试

```bash
pytest
```

## 核心设计

本项目采用多 Agent 串行工作流：

1. `Requirement Analyzer`：提取目标、用户、痛点、显性需求、隐性需求和验收标准。
2. `Architecture Planner`：生成组件划分、接口草案、数据模型和实现步骤。
3. `Risk Reviewer`：识别技术、产品、安全隐私和运维风险。
4. `Test Planner`：生成测试计划和人工审核检查项。
5. `Report Composer`：把结构化结果渲染为 Markdown 和 JSON。

所有结果默认是评审草稿，不执行自动合入、不修改线上配置、不替代人工决策。
