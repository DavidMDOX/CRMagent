import json
import os
from typing import Any

from openai import OpenAI

from .data_store import competitors, leads, market_snapshot, procurement_scores, sales_recommendation


def _fallback(agent_type: str, question: str) -> str:
    market = market_snapshot()
    top_supplier = procurement_scores()[0]
    sales = sales_recommendation()
    base = {
        "market": f"市场判断：当前铜价偏强震荡，LME 最新 {market['headline']['lme_last']}，SHFE 最新 {market['headline']['shfe_last']}，库存延续去化。建议：对刚需订单分批锁价，避免一次性追高。",
        "procurement": f"采购建议：优先联系 {top_supplier['name']}，综合得分最高，到岸成本约 {top_supplier['landed_cost']} 元/吨，交期 {top_supplier['lead_days']} 天。可同时保留进口渠道 D 作为价格锚点压价。",
        "sales": f"销售建议：竞品均价约 {sales['avg_competitor']} 元/吨，建议本轮主报价 {sales['suggested_offer']} 元/吨，并对高潜客户给出 50~80 元/吨灵活折扣。重点跟进 {leads()[1]['company']}。",
        "boss": "老板驾驶舱结论：库存下降与矿端扰动共同支撑价格，建议采购端保持滚动锁价，销售端加快高毛利客户转化，并在价格波动加大时每日复盘。",
    }
    suffix = f"\n\n用户问题：{question}" if question else ""
    return base.get(agent_type, base["boss"]) + suffix + "\n\n当前为内置 AI 演示模式。配置 OPENAI_API_KEY 后可切换为真实大模型分析。"


def agent_reply(agent_type: str, question: str) -> dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"mode": "fallback", "content": _fallback(agent_type, question)}

    payload = {
        "market": market_snapshot(),
        "suppliers": procurement_scores(),
        "competitors": competitors(),
        "leads": leads(),
        "sales_recommendation": sales_recommendation(),
    }
    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5.4"),
        input=[
            {
                "role": "system",
                "content": "你是铜贸易企业的经营分析 agent。请结合结构化业务数据输出中文、专业、简洁、可执行建议。回答分成：结论、原因、建议动作、风险提示。不要编造数据。",
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": f"agent类型: {agent_type}\n用户问题: {question}"},
                    {"type": "input_text", "text": "业务数据如下:" + json.dumps(payload, ensure_ascii=False)},
                ],
            },
        ],
    )
    return {"mode": "openai", "content": getattr(response, "output_text", None) or _fallback(agent_type, question)}
