import os

# https://bailian.console.aliyun.com/?tab=model#/api-key
os.environ["OPENAI_API_KEY"] = "sk-aa76fcf6520f48d38b356ae436c16af0"
os.environ["OPENAI_BASE_URL"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"

from agents.mcp.server import MCPServerSse
import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from openai.types.responses import ResponseTextDeltaEvent
from agents.mcp import MCPServer
from agents import set_default_openai_api, set_tracing_disabled
set_default_openai_api("chat_completions")
set_tracing_disabled(True)

async def run(mcp_server: MCPServer):
    external_client = AsyncOpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.environ["OPENAI_BASE_URL"],
    )
    
    # 关键：instructions 必须明确告诉大模型可以并且应该使用工具
    agent = Agent(
        name="企业职能助手",
        instructions="""你是企业的智能助手，专门帮助员工查询企业内部信息。

【重要】你拥有以下工具可以使用：
- query_employee_info: 查询员工详细信息（部门、职位、邮箱等）
- check_vacation_balance: 查询员工假期余额
- get_office_facilities: 查询办公设施（会议室、打印机等）
- get_city_weather: 查询天气
- 其他可用工具...

【使用规则】
1. 当用户询问员工信息、假期、办公设施等问题时，你必须使用对应的工具查询
2. 不要说"我无法查询"，你应该调用工具获取数据
3. 工具会返回真实数据，你只需要根据工具返回的结果组织语言回答
4. 如果工具返回错误，告诉用户查询失败的原因

【回答格式】
根据工具返回的数据，用友好的语气回答用户。""",
        mcp_servers=[mcp_server],
        model=OpenAIChatCompletionsModel(
            model="qwen-flash",
            openai_client=external_client,
        )
    )

    # 测试1: 查询员工信息
    message = "查一下李四的email"
    print(f"\n{'='*60}")
    print(f"测试1: 员工信息查询")
    print(f"{'='*60}")
    print(f"用户问题: {message}")
    print(f"{'='*60}")
    print("AI回答: ", end="", flush=True)

    result = Runner.run_streamed(agent, input=message)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
    
    print("\n")

    # 测试2: 查询假期余额
    message = "查询EMP001的年假余额"
    print(f"\n{'='*60}")
    print(f"测试2: 假期余额查询")
    print(f"{'='*60}")
    print(f"用户问题: {message}")
    print(f"{'='*60}")
    print("AI回答: ", end="", flush=True)

    result = Runner.run_streamed(agent, input=message)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
    
    print("\n")

    # 测试3: 查询办公设施
    message = "A栋2楼有哪些会议室？"
    print(f"\n{'='*60}")
    print(f"测试3: 办公设施查询")
    print(f"{'='*60}")
    print(f"用户问题: {message}")
    print(f"{'='*60}")
    print("AI回答: ", end="", flush=True)

    result = Runner.run_streamed(agent, input=message)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
    
    print("\n")


async def main():
    async with MCPServerSse(
            name="SSE Python Server",
            params={
                "url": "http://localhost:8900/sse",
            },
    )as server:
        await run(server)

if __name__ == "__main__":
    asyncio.run(main())
