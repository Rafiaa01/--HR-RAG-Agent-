import logging

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from src.prompt.system_prompt import SYSTEM_PROMPT
from src.tools.employee_tool import get_employee_details
from src.tools.leave_tool import calculate_leave_balance
from src.tools.policy_tool import search_company_policy

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

logger = logging.getLogger(__name__)


@wrap_tool_call
def log_tool_calls(request, handler):
    tool_call = request.tool_call

    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    logger.info("Tool called: %s", tool_name)
    logger.info("Tool arguments: %s", tool_args)

    try:
        result = handler(request)
        logger.info("Tool result: %s", result.content)
        return result

    except Exception:
        logger.exception("Tool execution failed: %s", tool_name)
        raise


agent = create_agent(
    model="gpt-4o-mini-2024-07-18",
    tools=[search_company_policy, calculate_leave_balance, get_employee_details],
    system_prompt=SYSTEM_PROMPT,
    middleware=[log_tool_calls],
)
