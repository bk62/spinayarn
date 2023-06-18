"""langchain chains for generation."""
from langchain import LLMChain

from .prompts import story_prompt


def get_story_generation_chain(llm):
    llm_chain = LLMChain(llm=llm, prompt=story_prompt)
    return llm_chain
