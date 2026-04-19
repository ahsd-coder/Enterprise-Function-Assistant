import asyncio
import json
from fastmcp import Client

client = Client("http://localhost:8900/sse")


def print_result(result):
    for item in result.content:
        if item.type == "text":
            try:
                print(json.dumps(json.loads(item.text), indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                print(item.text)


async def test_es_tools():
    async with client:
        # 1. 列出所有索引
        print("=" * 50)
        print("1. 列出所有索引")
        result = await client.call_tool("es_list_indices")
        print_result(result)

        # 2. 创建索引
        print("\n" + "=" * 50)
        print("2. 创建索引 test_index")
        result = await client.call_tool("es_create_index", arguments={
            "index_name": "test_index",
            "mappings": {
                "properties": {
                    "title": {"type": "text"},
                    "content": {"type": "text"},
                    "author": {"type": "keyword"}
                }
            }
        })
        print_result(result)

        # 3. 插入文档
        print("\n" + "=" * 50)
        print("3. 插入文档")
        result = await client.call_tool("es_add_document", arguments={
            "index_name": "test_index",
            "document": {"title": "测试标题", "content": "这是一条测试内容", "author": "张三"},
            "doc_id": "1"
        })
        print_result(result)

        # 4. 查询文档
        print("\n" + "=" * 50)
        print("4. 根据ID查询文档")
        result = await client.call_tool("es_get_document", arguments={
            "index_name": "test_index",
            "doc_id": "1"
        })
        print_result(result)

        # 5. 更新文档
        print("\n" + "=" * 50)
        print("5. 更新文档")
        result = await client.call_tool("es_update_document", arguments={
            "index_name": "test_index",
            "doc_id": "1",
            "document": {"title": "更新后的标题"}
        })
        print_result(result)

        # 6. 搜索文档
        print("\n" + "=" * 50)
        print("6. 搜索文档（match_all）")
        result = await client.call_tool("es_search", arguments={
            "index_name": "test_index",
            "query": {"match_all": {}},
            "size": 10
        })
        print_result(result)

        # 7. 关键词搜索
        print("\n" + "=" * 50)
        print("7. 关键词搜索")
        result = await client.call_tool("es_search", arguments={
            "index_name": "test_index",
            "query": {"match": {"content": "测试"}},
            "size": 5
        })
        print_result(result)

        # 8. 删除文档
        print("\n" + "=" * 50)
        print("8. 删除文档")
        result = await client.call_tool("es_delete_document", arguments={
            "index_name": "test_index",
            "doc_id": "1"
        })
        print_result(result)


asyncio.run(test_es_tools())
