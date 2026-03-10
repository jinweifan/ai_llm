from typing import Callable

from langchain.agents.middleware import (
    AgentState,
    ModelRequest,
    before_model,
    dynamic_prompt,
    wrap_tool_call,
)
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage
from langgraph.runtime import Runtime
from langgraph.types import Command

from utils.logger_handler import logger
from utils.prompt_loader import load_report_prompt, load_system_prompt

@wrap_tool_call
def monitor_tool(
    request: ToolCallRequest, handler: Callable[ToolCallRequest, ToolMessage | Command]
) -> ToolMessage | Command:
    """ 
    监控工具执行情况，记录工具执行日志
    
    Args:
        request: 工具调用请求
        handler: 工具处理函数
    Returns:
        ToolMessage | Command: 工具执行结果
    """
    logger.info("[monitor_tool]执行工具: %s", str(request.tool_call['name']))
    logger.info("[monitor_tool]执行工具入参: %s", str(request.tool_call['args']))
    try:
        result = handler(request)
        
        if request.tool_call['name'] == 'fetch_external_data':
            request.runtime.context['report'] = True

    except Exception as e:
        logger.error("[monitor_tool]执行工具失败: %s", str(e))
        raise e
    logger.info("[monitor_tool]工具执行成功: %s", str(result))
    return result


@before_model
def log_before_model(state: AgentState, runtime: Runtime):
    """ 
    执行模型前，记录模型执行日志
    Args:
        state: 模型状态
        runtime: 运行时
    Returns:
        AgentState: 模型状态
    """
    logger.info("[log_before_model]执行模型前，带有%d条消息", len(state["messages"]))

    logger.debug(
        "[log_before_model]类型: %s | 内容: %s",
        type(state["messages"][-1]).__name__,
        state["messages"][-1].content,
    )


@dynamic_prompt
def report_prompt_switch(request: ModelRequest) -> str:
    """ 
    根据是否为报告生成场景，动态切换提示词
    Args:
        request: 模型调用请求
    Returns:
        str: 提示词
    """
    is_report = request.runtime.context.get("report", False)
    if is_report:
        logger.info("[report_prompt_switch]切换为报告生成场景")
        logger.critical("[report_prompt_switch]报告生成场景提示词: %s", load_report_prompt())
        return load_report_prompt()

    return load_system_prompt()
