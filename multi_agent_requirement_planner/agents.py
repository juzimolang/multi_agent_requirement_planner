from __future__ import annotations

import json
import os
from typing import Type, TypeVar

from pydantic import BaseModel

from models import (
    ArchitecturePlan,
    RequirementAnalysis,
    RequirementInput,
    ReviewDocument,
    RiskAssessment,
    TestPlan,
)

T = TypeVar("T", bound=BaseModel)


def _ensure_text(requirement: str) -> str:
    text = requirement.strip()
    if not text:
        raise ValueError("Requirement text cannot be empty.")
    return text


class MockAgentRunner:
    """Deterministic local implementation for demos, testing, and no-key environments."""

    def analyze_requirement(self, requirement: str) -> RequirementAnalysis:
        text = _ensure_text(requirement)
        return RequirementAnalysis(
            core_goal="将模糊或半结构化需求转化为可评审、可执行的技术方案材料。",
            target_users=["产品经理", "研发负责人", "后端/前端工程师", "测试或质量保障同学"],
            pain_points=[
                "需求描述分散，评审前需要反复补齐背景、边界和验收标准。",
                "技术方案、风险评估和测试计划经常由不同角色重复整理。",
                "AI 输出缺少人工审核节点时，容易产生不可控变更风险。",
            ],
            explicit_requirements=[
                "输入一段中文需求描述。",
                "输出需求澄清问题、接口设计草案、实现拆分、风险点、测试建议和评审摘要。",
                "支持人工审核，禁止 AI 直接合入代码或修改线上配置。",
            ],
            implicit_requirements=[
                "需要结构化输出，便于进入评审、归档或工单系统。",
                "需要可追踪的中间结果，方便人工判断 AI 推理是否可靠。",
                "需要可替换模型或 mock 模式，方便本地演示和测试。",
            ],
            open_questions=[
                "输出评审材料是否需要固定模板或接入现有文档系统？",
                "是否需要保存历史版本和评审意见？",
                "是否需要连接 Jira、飞书、Slack、GitHub 或内部知识库？",
                "哪些字段属于敏感信息，需要脱敏或禁止发送给外部模型？",
            ],
            acceptance_criteria=[
                "给定一段需求文本，系统能稳定生成 Markdown 评审文档。",
                "文档包含需求分析、技术方案、风险评估和测试计划四类核心内容。",
                "系统默认启用人工审核流程，不执行任何自动合入或线上变更。",
            ],
        )

    def plan_architecture(self, requirement: str, analysis: RequirementAnalysis) -> ArchitecturePlan:
        _ensure_text(requirement)
        return ArchitecturePlan(
            overview="采用多 Agent 串行工作流：先进行需求解析，再生成技术方案，然后进行风险评估和测试规划，最后汇总为评审文档。",
            major_components=[
                "Requirement Analyzer：提取目标、用户、痛点、显性需求、隐性需求和验收标准。",
                "Architecture Planner：生成组件划分、接口草案、数据模型和实现步骤。",
                "Risk Reviewer：识别技术、产品、安全、隐私和运维风险。",
                "Test Planner：生成单测、集成测试、边界场景和人工审核检查项。",
                "Report Composer：把结构化结果渲染为 Markdown 和 JSON。",
            ],
            api_draft=[
                "POST /plan：输入 requirement 和 mock 标记，返回 Markdown 与结构化 JSON。",
                "GET /health：返回服务健康状态。",
                "CLI：python run_cli.py --input sample_requirement.txt --mock --out outputs/review.md --json outputs/result.json",
            ],
            data_model_notes=[
                "RequirementAnalysis 保存需求解析结果。",
                "ArchitecturePlan 保存技术方案。",
                "RiskAssessment 保存风险和缓解措施。",
                "TestPlan 保存测试计划。",
                "ReviewDocument 作为最终聚合对象。",
            ],
            implementation_steps=[
                "先实现 mock Agent，保证无 API Key 时可演示和测试。",
                "再实现 OpenAI Agent Runner，用 Pydantic schema 解析结构化输出。",
                "实现 CLI 与 FastAPI 两种入口。",
                "补充 pytest 测试，验证 mock 模式和 Markdown 渲染。",
            ],
            integration_points=[
                "可接入需求管理系统读取需求描述。",
                "可接入文档系统写入评审材料。",
                "可接入代码仓库，仅用于读取上下文或创建草稿，不自动合入。",
            ],
        )

    def assess_risks(self, requirement: str, analysis: RequirementAnalysis, plan: ArchitecturePlan) -> RiskAssessment:
        _ensure_text(requirement)
        return RiskAssessment(
            technical_risks=[
                "模型可能遗漏项目特定约束。",
                "需求描述过短时，生成方案可能过度假设。",
                "不同 Agent 输出之间可能存在不一致。",
            ],
            product_risks=[
                "评审文档看似完整，但关键业务决策仍未被确认。",
                "用户可能误以为 AI 输出等同于最终方案。",
            ],
            security_privacy_risks=[
                "需求文本可能包含敏感业务信息或用户数据。",
                "若接入外部模型，需要明确数据边界和脱敏策略。",
            ],
            operational_risks=[
                "模型调用失败、超时或成本超预算。",
                "自动化流程缺少审计记录时，难以定位错误来源。",
            ],
            mitigations=[
                "默认开启 mock/local 测试模式，CI 中不依赖外部 API。",
                "所有输出只生成草稿，必须经人工审核后才能进入开发流程。",
                "对低置信度或缺少上下文的部分显式输出待澄清问题。",
                "记录每个 Agent 的输入输出，便于审计和问题回溯。",
            ],
        )

    def plan_tests(self, requirement: str, analysis: RequirementAnalysis, plan: ArchitecturePlan, risks: RiskAssessment) -> TestPlan:
        _ensure_text(requirement)
        return TestPlan(
            unit_tests=[
                "验证空输入会被拒绝。",
                "验证 RequirementAnalysis、ArchitecturePlan、RiskAssessment、TestPlan 均能正常序列化。",
                "验证 Markdown 渲染包含核心章节标题。",
            ],
            integration_tests=[
                "调用 POST /plan，检查返回 document 和 markdown。",
                "运行 CLI，检查输出文件是否生成。",
                "在 mock 模式和 live 模式下分别验证主流程。",
            ],
            edge_cases=[
                "需求过短，仅包含一句话。",
                "需求包含多个互相冲突的目标。",
                "需求包含敏感字段，需要人工判断是否脱敏。",
            ],
            manual_review_checks=[
                "确认需求边界是否真实符合业务目标。",
                "确认接口草案是否符合团队规范。",
                "确认风险缓解措施是否可执行。",
                "确认 AI 未生成任何自动合入或线上变更动作。",
            ],
        )

    def run(self, requirement: str) -> ReviewDocument:
        analysis = self.analyze_requirement(requirement)
        plan = self.plan_architecture(requirement, analysis)
        risks = self.assess_risks(requirement, analysis, plan)
        tests = self.plan_tests(requirement, analysis, plan, risks)
        return ReviewDocument(
            title="多 Agent 需求评审材料",
            requirement_analysis=analysis,
            architecture_plan=plan,
            risk_assessment=risks,
            test_plan=tests,
            final_summary="该方案适合作为研发提效 PoC：它不直接替代人工决策，而是把需求解析、方案草案、风险识别和测试规划前置自动化，并通过人工审核节点控制交付风险。",
        )


class OpenAIAgentRunner:
    """OpenAI-backed implementation. Requires OPENAI_API_KEY."""

    def __init__(self, model: str | None = None):
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("openai package is not installed. Run: pip install -r requirements.txt") from exc

        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is not set. Use --mock or configure .env / environment variables.")

        self.client = OpenAI()
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    def _parse(self, system_prompt: str, user_payload: dict, schema: Type[T]) -> T:
        # Primary path: modern OpenAI Python SDK structured parsing.
        try:
            completion = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
                ],
                response_format=schema,
            )
            parsed = completion.choices[0].message.parsed
            if parsed is None:
                raise RuntimeError("Model returned no parsed object.")
            return parsed
        except AttributeError as exc:
            raise RuntimeError(
                "Your openai package does not support beta.chat.completions.parse. "
                "Upgrade with: pip install --upgrade openai"
            ) from exc

    def analyze_requirement(self, requirement: str) -> RequirementAnalysis:
        return self._parse(
            "你是资深产品技术分析 Agent。请把需求文本拆解为结构化需求分析，避免编造确定事实；不确定处写入 open_questions。",
            RequirementInput(text=_ensure_text(requirement)).model_dump(),
            RequirementAnalysis,
        )

    def plan_architecture(self, requirement: str, analysis: RequirementAnalysis) -> ArchitecturePlan:
        return self._parse(
            "你是资深架构设计 Agent。请基于需求分析生成务实的技术方案草案，强调人工审核和可验证闭环。",
            {"requirement": _ensure_text(requirement), "analysis": analysis.model_dump()},
            ArchitecturePlan,
        )

    def assess_risks(self, requirement: str, analysis: RequirementAnalysis, plan: ArchitecturePlan) -> RiskAssessment:
        return self._parse(
            "你是风险评审 Agent。请从技术、产品、安全隐私、运维四个维度识别风险，并给出可执行缓解措施。",
            {"requirement": _ensure_text(requirement), "analysis": analysis.model_dump(), "plan": plan.model_dump()},
            RiskAssessment,
        )

    def plan_tests(self, requirement: str, analysis: RequirementAnalysis, plan: ArchitecturePlan, risks: RiskAssessment) -> TestPlan:
        return self._parse(
            "你是测试规划 Agent。请生成单元测试、集成测试、边界场景和人工审核检查项。",
            {
                "requirement": _ensure_text(requirement),
                "analysis": analysis.model_dump(),
                "plan": plan.model_dump(),
                "risks": risks.model_dump(),
            },
            TestPlan,
        )

    def run(self, requirement: str) -> ReviewDocument:
        analysis = self.analyze_requirement(requirement)
        plan = self.plan_architecture(requirement, analysis)
        risks = self.assess_risks(requirement, analysis, plan)
        tests = self.plan_tests(requirement, analysis, plan, risks)
        return ReviewDocument(
            title="多 Agent 需求评审材料",
            requirement_analysis=analysis,
            architecture_plan=plan,
            risk_assessment=risks,
            test_plan=tests,
            final_summary="本评审材料由多 Agent 工作流生成，建议作为草案进入人工评审。关键业务判断、系统边界、安全策略和上线计划仍需负责人确认。",
        )


def build_runner(mock: bool):
    return MockAgentRunner() if mock else OpenAIAgentRunner()
