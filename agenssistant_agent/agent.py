from pydantic_ai import Agent

agentssistant = Agent[None, str](
    model="gpt-4o-mini",
    deps_type=None,
    result_type=str,
    tools=[],
    system_prompt=(),
)
