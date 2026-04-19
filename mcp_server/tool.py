import re
from typing import Annotated, Union
import requests
from datetime import datetime
TOKEN = "6d997a997fbf"
ES_BASE_URL = "http://8.130.25.172:9200"

from fastmcp import FastMCP
mcp = FastMCP(
    name="Tools-MCP-Server",
    instructions="""This server contains some api of tools.""",
)

@mcp.tool
def get_city_weather(city_name: Annotated[str, "The Pinyin of the city name (e.g., 'beijing' or 'shanghai')"]):
    """Retrieves the current weather data using the city's Pinyin name."""
    try:
        return requests.get(f"https://whyta.cn/api/tianqi?key={TOKEN}&city={city_name}").json()["data"]
    except:
        return []

@mcp.tool
def get_address_detail(address_text: Annotated[str, "City Name"]):
    """Parses a raw address string to extract detailed components (province, city, district, etc.)."""
    try:
        return requests.get(f"https://whyta.cn/api/tx/addressparse?key={TOKEN}&text={address_text}").json()["result"]
    except:
        return []

@mcp.tool
def get_tel_info(tel_no: Annotated[str, "Tel phone number"]):
    """Retrieves basic information (location, carrier) for a given telephone number."""
    try:
        return requests.get(f"https://whyta.cn/api/tx/mobilelocal?key={TOKEN}&phone={tel_no}").json()["result"]
    except:
        return []

@mcp.tool
def get_scenic_info(scenic_name: Annotated[str, "Scenic/tourist place name"]):
    """Searches for and retrieves information about a specific scenic spot or tourist attraction."""
    # https://apis.whyta.cn/docs/tx-scenic.html
    try:
        return requests.get(f"https://whyta.cn/api/tx/scenic?key={TOKEN}&word={scenic_name}").json()["result"]["list"]
    except:
        return []

@mcp.tool
def get_flower_info(flower_name: Annotated[str, "Flower name"]):
    """Retrieves the flower language (花语) and details for a given flower name."""
    # https://apis.whyta.cn/docs/tx-huayu.html
    try:
        return requests.get(f"https://whyta.cn/api/tx/huayu?key={TOKEN}&word={flower_name}").json()["result"]
    except:
        return []

@mcp.tool
def get_rate_transform(
    source_coin: Annotated[str, "The three-letter code (e.g., USD, CNY) for the source currency."], 
    aim_coin: Annotated[str, "The three-letter code (e.g., EUR, JPY) for the target currency."], 
    money: Annotated[Union[int, float], "The amount of money to convert."]
):
    """Calculates the currency exchange conversion amount between two specified coins."""
    try:
        return requests.get(f"https://whyta.cn/api/tx/fxrate?key={TOKEN}&fromcoin={source_coin}&tocoin={aim_coin}&money={money}").json()["result"]["money"]
    except:
        return []


@mcp.tool
def sentiment_classification(text: Annotated[str, "The text to analyze"]):
    """Classifies the sentiment of a given text."""
    positive_keywords_zh = ['喜欢', '赞', '棒', '优秀', '精彩', '完美', '开心', '满意']
    negative_keywords_zh = ['差', '烂', '坏', '糟糕', '失望', '垃圾', '厌恶', '敷衍']

    positive_pattern = '(' + '|'.join(positive_keywords_zh) + ')'
    negative_pattern = '(' + '|'.join(negative_keywords_zh) + ')'

    positive_matches = re.findall(positive_pattern, text)
    negative_matches = re.findall(negative_pattern, text)

    count_positive = len(positive_matches)
    count_negative = len(negative_matches)

    if count_positive > count_negative:
        return "积极 (Positive)"
    elif count_negative > count_positive:
        return "消极 (Negative)"
    else:
        return "中性 (Neutral)"


@mcp.tool
def query_salary_info(user_name: Annotated[str, "用户名"]):
    """Query user salary baed on the username."""

    # TODO 基于用户名，在数据库中查询，返回数据库查询结果

    if len(user_name) == 2:
        return 1000
    elif len(user_name) == 3:
        return 2000
    else:
        return 3000


@mcp.tool
def work_survival_guide(overtime_hours: Annotated[int, "今日加班时长(小时)"],
                        boss_mood: Annotated[str, "老板心情(好/正常/暴躁)"]):
    """Get survival advice based on overtime and boss mood."""

    if overtime_hours == 0:
        return "准点下班的人，建议低头快走，别在老板面前晃悠"
    elif overtime_hours < 2:
        if boss_mood == "暴躁":
            return "加班不够，建议再熬半小时，别当出头鸟🐤"
        else:
            return "加得刚刚好，明天可以摸鱼2小时"
    else:
        return f"加班{overtime_hours}小时勇士，老板心情{boss_mood}时建议：\n- 立刻提交周报\n- 回复所有未读消息\n- 然后默默消失"


@mcp.tool
def daily_horoscope(zodiac: Annotated[str, "星座"],
                    mood: Annotated[str, "今天心情(好/一般/差)"]):
    """Predict daily fortune based on zodiac and mood."""

    if mood == "好":
        return f"{zodiac}座今天运气爆棚，买彩票可能中5块，表白成功率+10%"
    elif mood == "差":
        return f"{zodiac}座今天建议躺平，吵架可能吵不赢，外卖可能被偷"
    else:
        if zodiac in ["处女座", "摩羯座"]:
            return f"{zodiac}座心情一般也没关系，你本来就很佛系😌"
        else:
            return f"{zodiac}座建议立刻点杯奶茶，心情直升两个level"


@mcp.tool
def wechat_steps_detective(steps: Annotated[int, "微信步数"]):
    """Deduce what someone did today based on steps."""

    if steps < 100:
        return "今日状态：床就是我的一切，厕所是唯一的远行🚽"
    elif 100 <= steps < 1000:
        return "今日状态：去拿了次外卖+上了两次厕所，充实的一天呢"
    elif 1000 <= steps < 5000:
        return "今日状态：正常上班族，地铁站到公司的距离，毫无惊喜"
    elif 5000 <= steps < 10000:
        return "今日状态：逛了趟超市/商场，大概率是被女朋友拉去的"
    elif 10000 <= steps < 20000:
        return "今日状态：旅游/爬山/逛展，朋友圈素材已就绪📸"
    else:
        return "今日状态：马拉松选手？还是手机绑狗身上了？🐕"


@mcp.tool
def garbage_classification(item_name: Annotated[str, "物品名称"]):
    """查询物品属于哪种垃圾分类（可回收物、有害垃圾、厨余垃圾、其他垃圾）。"""

    recyclable = ['纸箱', '塑料瓶', '易拉罐', '玻璃瓶', '旧衣服', '报纸', '金属', '书本', '牛奶盒']
    hazardous = ['电池', '灯泡', '过期药品', '油漆', '水银温度计', '杀虫剂', '指甲油']
    kitchen = ['剩饭', '果皮', '菜叶', '蛋壳', '茶渣', '骨头', '鱼刺', '残羹剩饭', '花生壳']
    other = ['纸巾', '烟蒂', '陶瓷碎片', '一次性餐具', '尘土', '卫生纸', '尿不湿', '污损塑料袋']

    for item in recyclable:
        if item in item_name:
            return f"「{item_name}」属于【可回收物】♻️ — 请投放至蓝色垃圾桶，保持清洁干燥"
    for item in hazardous:
        if item in item_name:
            return f"「{item_name}」属于【有害垃圾】⚠️ — 请投放至红色垃圾桶，注意轻放防破损"
    for item in kitchen:
        if item in item_name:
            return f"「{item_name}」属于【厨余垃圾】🍂 — 请投放至绿色垃圾桶，沥干水分后投放"
    for item in other:
        if item in item_name:
            return f"「{item_name}」属于【其他垃圾】🗑️ — 请投放至灰色垃圾桶"

    return f"「{item_name}」未在数据库中找到，建议查询当地垃圾分类标准或咨询社区"


# ===================== Elasticsearch 工具 =====================

@mcp.tool
def es_list_indices():
    """列出Elasticsearch中所有索引及其基本信息（名称、文档数、大小等）。"""
    try:
        url = f"{ES_BASE_URL}/_cat/indices?format=json"
        resp = requests.get(url)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool
def es_browse_all(size: Annotated[int, "每个索引最多返回的文档数，默认5"] = 5):
    """一站式浏览数据库：列出所有用户索引名称和文档数量，并返回每个索引中的文档摘要。返回中包含doc_count（总数）和shown（本次展示数），若shown<doc_count表示还有更多文档未展示，需用es_search查看。"""
    try:
        indices_url = f"{ES_BASE_URL}/_cat/indices?format=json"
        indices = requests.get(indices_url).json()
        result = []
        for idx in indices:
            index_name = idx["index"]
            # 过滤系统索引（以.开头的）
            if index_name.startswith("."):
                continue
            doc_count = int(idx.get("docs.count", 0))
            index_info = {"index": index_name, "doc_count": doc_count}
            if doc_count > 0:
                search_url = f"{ES_BASE_URL}/{index_name}/_search"
                body = {"query": {"match_all": {}}, "size": size}
                search_resp = requests.get(search_url, json=body, headers={"Content-Type": "application/json"})
                hits = search_resp.json().get("hits", {}).get("hits", [])
                docs = []
                for h in hits:
                    src = h["_source"]
                    # 只保留最多3个关键字段，减少输出量
                    keys = list(src.keys())[:3]
                    doc = {"id": h["_id"]}
                    for k in keys:
                        val = src[k]
                        # 字段值过长则截断
                        if isinstance(val, str) and len(val) > 50:
                            val = val[:50] + "..."
                        doc[k] = val
                    docs.append(doc)
                index_info["docs"] = docs
                index_info["shown"] = len(docs)
            else:
                index_info["docs"] = []
                index_info["shown"] = 0
            result.append(index_info)
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool
def es_create_index(
    index_name: Annotated[str, "索引名称（小写字母、数字、下划线组成）"],
    mappings: Annotated[dict, "索引映射定义，如 {\"properties\": {\"title\": {\"type\": \"text\"}, \"content\": {\"type\": \"text\"}}}"] = None
):
    """在Elasticsearch中创建一个新索引，可自定义字段映射。"""
    try:
        url = f"{ES_BASE_URL}/{index_name}"
        body = {}
        if mappings:
            body["mappings"] = mappings
        resp = requests.put(url, json=body)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool
def es_add_document(
    index_name: Annotated[str, "索引名称"],
    document: Annotated[dict, "要插入的文档内容，如 {\"title\": \"测试\", \"content\": \"内容\"}"],
    doc_id: Annotated[str, "文档ID（可选，不指定则自动生成）"] = None
):
    """向Elasticsearch指定索引中插入一条文档。"""
    try:
        if doc_id:
            url = f"{ES_BASE_URL}/{index_name}/_doc/{doc_id}"
        else:
            url = f"{ES_BASE_URL}/{index_name}/_doc"
        resp = requests.post(url, json=document, headers={"Content-Type": "application/json"})
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool
def es_get_document(
    index_name: Annotated[str, "索引名称"],
    doc_id: Annotated[str, "文档ID"]
):
    """根据文档ID从Elasticsearch中查询一条文档。"""
    try:
        url = f"{ES_BASE_URL}/{index_name}/_doc/{doc_id}"
        resp = requests.get(url)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool
def es_update_document(
    index_name: Annotated[str, "索引名称"],
    doc_id: Annotated[str, "文档ID"],
    document: Annotated[dict, "要更新的字段内容，如 {\"title\": \"新标题\"}"]
):
    """更新Elasticsearch中指定ID文档的部分字段。"""
    try:
        url = f"{ES_BASE_URL}/{index_name}/_update/{doc_id}"
        body = {"doc": document}
        resp = requests.post(url, json=body, headers={"Content-Type": "application/json"})
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool
def es_delete_document(
    index_name: Annotated[str, "索引名称"],
    doc_id: Annotated[str, "文档ID"]
):
    """根据文档ID从Elasticsearch中删除一条文档。"""
    try:
        url = f"{ES_BASE_URL}/{index_name}/_doc/{doc_id}"
        resp = requests.delete(url)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool
def es_search(
    index_name: Annotated[str, "索引名称"],
    query: Annotated[dict, "ES查询条件，如 {\"match_all\": {}} 或 {\"match\": {\"title\": \"关键词\"}}"],
    size: Annotated[int, "返回结果数量，默认10"] = 10
):
    """在Elasticsearch指定索引中搜索文档。query参数只需传查询条件部分，函数会自动包装为完整的ES请求体。"""
    try:
        url = f"{ES_BASE_URL}/{index_name}/_search"
        body = {"query": query, "size": size}
        resp = requests.get(url, json=body, headers={"Content-Type": "application/json"})
        return resp.json()
    except Exception as e:
        return {"error": str(e)}
