from typing import Optional, Dict
from dotenv import load_dotenv

from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph, END

from .config import ProjectConfig
from .tools import generate_fastapi_boilerplate_func

# Load environment variables from .env file
load_dotenv()


class State(TypedDict):
    user_request: str
    config: Optional[dict]
    files: Optional[Dict[str, str]]


llm = ChatOpenAI(model="gpt-4o-mini")

parser = PydanticOutputParser(pydantic_object=ProjectConfig)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You convert a user request into a ProjectConfig configuration. "
            "The output must match this exact schema:\n"
            "- project_name: string (required)\n"
            "- db: either 'postgres' or 'sqlite' (default: 'postgres')\n"
            "- auth_enabled: boolean (default: true)\n"
            "- docker: boolean (default: true)\n"
            "- ci: either 'gitlab', 'github', or 'none' (default: 'github')\n\n"
            "Respond ONLY with valid JSON matching this schema. "
            "Use simple boolean values for docker and auth_enabled fields.",
        ),
        ("human", "{user_request}"),
    ]
)


def to_config_dict(user_request: str) -> dict:
    msg = prompt.format_messages(user_request=user_request)
    result = llm.invoke(msg)
    config = parser.parse(result.content)
    return config.dict()


def build_config(state: State) -> State:
    config = to_config_dict(state["user_request"])
    return {**state, "config": config}


def generate_code(state: State) -> State:
    files = generate_fastapi_boilerplate_func(state["config"])
    return {**state, "files": files}


def build_app():
    graph = StateGraph(State)
    graph.add_node("build_config", build_config)
    graph.add_node("generate_code", generate_code)

    graph.set_entry_point("build_config")
    graph.add_edge("build_config", "generate_code")
    graph.add_edge("generate_code", END)

    return graph.compile()
