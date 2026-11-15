from agents import MockAgentRunner
from report import render_markdown


def test_mock_runner_generates_document():
    runner = MockAgentRunner()
    doc = runner.run("请把需求转换为技术评审材料，必须支持人工审核。")
    assert doc.title
    assert doc.requirement_analysis.core_goal
    assert doc.architecture_plan.major_components
    assert doc.risk_assessment.mitigations
    assert doc.test_plan.manual_review_checks


def test_markdown_contains_sections():
    runner = MockAgentRunner()
    doc = runner.run("做一个多 Agent 需求评审工具。")
    md = render_markdown(doc)
    assert "## 1. 需求分析" in md
    assert "## 2. 技术方案" in md
    assert "## 3. 风险评估" in md
    assert "## 4. 测试计划" in md
    assert "## 5. 评审结论" in md
