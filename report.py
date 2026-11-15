from __future__ import annotations

from models import ReviewDocument


def _bullets(items: list[str]) -> str:
    if not items:
        return "- 暂无"
    return "\n".join(f"- {item}" for item in items)


def render_markdown(doc: ReviewDocument) -> str:
    a = doc.requirement_analysis
    p = doc.architecture_plan
    r = doc.risk_assessment
    t = doc.test_plan

    return f"""# {doc.title}

## 1. 需求分析

**核心目标**  
{a.core_goal}

**目标用户**
{_bullets(a.target_users)}

**核心痛点**
{_bullets(a.pain_points)}

**明确需求**
{_bullets(a.explicit_requirements)}

**隐含需求**
{_bullets(a.implicit_requirements)}

**待澄清问题**
{_bullets(a.open_questions)}

**验收标准**
{_bullets(a.acceptance_criteria)}

## 2. 技术方案

**方案概览**  
{p.overview}

**主要组件**
{_bullets(p.major_components)}

**接口草案**
{_bullets(p.api_draft)}

**数据模型说明**
{_bullets(p.data_model_notes)}

**实现拆分**
{_bullets(p.implementation_steps)}

**系统集成点**
{_bullets(p.integration_points)}

## 3. 风险评估

**技术风险**
{_bullets(r.technical_risks)}

**产品风险**
{_bullets(r.product_risks)}

**安全与隐私风险**
{_bullets(r.security_privacy_risks)}

**运维风险**
{_bullets(r.operational_risks)}

**缓解措施**
{_bullets(r.mitigations)}

## 4. 测试计划

**单元测试**
{_bullets(t.unit_tests)}

**集成测试**
{_bullets(t.integration_tests)}

**边界场景**
{_bullets(t.edge_cases)}

**人工审核检查项**
{_bullets(t.manual_review_checks)}

## 5. 评审结论

{doc.final_summary}
"""
