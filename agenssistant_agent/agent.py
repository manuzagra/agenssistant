from pydantic_ai import Agent, RunContext

from agenssistant_common import types

# Main agent
agentssistant = Agent[types.AgentDependencies, str](
    model="gpt-4o-mini",
    deps_type=types.AgentDependencies,
    result_type=str,
    tools=[],
    system_prompt=(),
)


@agentssistant.system_prompt(dynamic=True)
async def system_prompt(ctx: RunContext[types.AgentDependencies]) -> str:
    user = ctx.deps.user
    propmt = f"The first name of the user is {user.first_name}"
    propmt += f", the last name is {user.last_name}" if user.last_name else ""
    propmt += f", the username is {user.username}" if user.username else ""
    propmt += f", and the language code is {user.language_code}" if user.language_code else ""
    propmt += "."
    return propmt
