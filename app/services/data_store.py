from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any

@dataclass
class User:
    username: str
    password: str
    role: str
    display_name: str

USERS = {
    "admin": User("admin", "admin123", "admin", "系统管理员"),
    "buyer": User("buyer", "buyer123", "buyer", "采购经理"),
    "sales": User("sales", "sales123", "sales", "销售经理"),
    "boss": User("boss", "boss123", "boss", "总经理"),
}

def market_snapshot() -> dict[str, Any]:
    today = date.today()
    days = [(today - timedelta(days=i)).strftime("%m-%d") for i in range(9, -1, -1)]
    lme = [8535, 8560, 8612, 8588, 8662, 8710, 8738, 8696, 8768, 8820]
    shfe = [68840, 68950, 69320, 69210, 69780, 70150, 70320, 70010, 70680, 70990]
    inventory = [128, 126, 125, 123, 122, 120, 119, 118, 117, 115]
    usd_cny = [7.19, 7.20, 7.19, 7.18, 7.18, 7.17, 7.17, 7.16, 7.16, 7.15]
    return {"days": days, "lme": lme, "shfe": shfe, "inventory": inventory, "usd_cny": usd_cny,
            "headline": {"lme_last": lme[-1], "shfe_last": shfe[-1], "inventory_last": inventory[-1], "fx_last": usd_cny[-1], "signal": "偏强震荡"},
            "events": ["海外矿端扰动预期升温，短期对铜价形成情绪支撑。", "国内库存延续去化，现货升水有改善迹象。", "美元偏弱时段有利于有色金属价格表现。"]}

def suppliers() -> list[dict[str, Any]]:
    return [
        {"name":"华东精铜供应A","region":"上海","price":70860,"freight":120,"purity":99.95,"lead_days":3,"reliability":94,"capacity":380},
        {"name":"华南再生铜供应B","region":"佛山","price":70280,"freight":260,"purity":99.88,"lead_days":5,"reliability":88,"capacity":520},
        {"name":"西南冶炼厂C","region":"云南","price":70520,"freight":210,"purity":99.92,"lead_days":4,"reliability":91,"capacity":640},
        {"name":"进口渠道D","region":"洋山港","price":70010,"freight":330,"purity":99.97,"lead_days":9,"reliability":86,"capacity":800},
    ]

def competitors() -> list[dict[str, Any]]:
    return [
        {"company":"竞品甲","platform":"1688","price":71450,"update":"10:20","note":"主打高纯阴极铜"},
        {"company":"竞品乙","platform":"微信社群","price":71280,"update":"10:42","note":"现货库存充足"},
        {"company":"竞品丙","platform":"阿里国际站","price":71820,"update":"11:05","note":"强调稳定交期"},
    ]

def leads() -> list[dict[str, Any]]:
    return [
        {"company":"苏州精密连接器厂","contact":"王经理","demand":"月需120吨","stage":"待跟进","score":86},
        {"company":"宁波电缆企业","contact":"李总","demand":"关注低氧铜杆","stage":"已沟通","score":91},
        {"company":"东莞五金加工厂","contact":"陈采购","demand":"询价铜带材料","stage":"报价中","score":78},
    ]

def publish_tasks() -> list[dict[str, Any]]:
    return [
        {"channel":"1688","title":"高纯阴极铜现货供应","status":"已排队","eta":"今日 15:00"},
        {"channel":"企业微信朋友圈","title":"本周铜价窗口+库存到货","status":"草稿","eta":"待审核"},
        {"channel":"阿里国际站","title":"Copper Cathode Export Offer","status":"已发布","eta":"今日 11:30"},
    ]

def procurement_scores() -> list[dict[str, Any]]:
    scored=[]
    for item in suppliers():
        score=((71500-item["price"])*0.25 + (100-item["freight"]/4)*0.15 + item["purity"]*35 + (100-item["lead_days"]*8)*0.1 + item["reliability"]*0.25 + min(item["capacity"],600)*0.03)
        scored.append({**item,"score":round(score,2),"landed_cost":item["price"]+item["freight"]})
    return sorted(scored,key=lambda x:x["score"],reverse=True)

def sales_recommendation() -> dict[str, Any]:
    market = market_snapshot()["headline"]
    avg_comp = sum(x["price"] for x in competitors()) / len(competitors())
    target = round(avg_comp - 80)
    floor = 70480
    return {"avg_competitor": round(avg_comp,2), "suggested_offer": max(target,floor), "margin_comment":"建议保留每吨 220~350 元弹性区间，便于对核心客户快速谈判。", "market_signal": market["signal"]}
