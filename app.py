from __future__ import annotations

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from agents import build_runner
from models import PlanRequest, PlanResponse
from report import render_markdown

load_dotenv()

app = FastAPI(title="Multi-Agent Requirement Planner", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return """
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <title>Multi-Agent Requirement Planner</title>
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, sans-serif; margin: 32px; max-width: 1000px; }
    textarea { width: 100%; height: 220px; font-size: 14px; padding: 12px; }
    button { padding: 10px 16px; margin-top: 12px; cursor: pointer; }
    pre { white-space: pre-wrap; background: #f6f6f6; padding: 16px; border-radius: 8px; }
    label { display: block; margin-top: 12px; }
  </style>
</head>
<body>
  <h1>Multi-Agent Requirement Planner</h1>
  <p>输入一段需求，生成技术评审材料。默认使用 mock 模式，不需要 API Key。</p>
  <textarea id="requirement">我们希望做一个内部研发提效工具，用于把产品经理的需求描述自动转成技术评审材料。输出需要包含需求澄清问题、接口设计草案、实现拆分、风险点、测试建议和评审摘要。系统需要支持人工审核，不允许 AI 直接合入代码或修改线上配置。</textarea>
  <label><input id="mock" type="checkbox" checked /> 使用 mock 模式</label>
  <button onclick="run()">生成</button>
  <h2>输出</h2>
  <pre id="output">等待生成...</pre>
<script>
async function run() {
  const output = document.getElementById('output');
  output.textContent = '生成中...';
  const res = await fetch('/plan', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      requirement: document.getElementById('requirement').value,
      mock: document.getElementById('mock').checked
    })
  });
  const data = await res.json();
  if (!res.ok) {
    output.textContent = data.detail || JSON.stringify(data, null, 2);
    return;
  }
  output.textContent = data.markdown;
}
</script>
</body>
</html>
"""


@app.post("/plan", response_model=PlanResponse)
def plan(req: PlanRequest) -> PlanResponse:
    try:
        runner = build_runner(mock=req.mock)
        document = runner.run(req.requirement)
        markdown = render_markdown(document)
        return PlanResponse(markdown=markdown, document=document)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
