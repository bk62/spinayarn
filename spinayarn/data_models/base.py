"""Base data models."""
from pydantic import BaseModel, Field


class NodeLink(BaseModel):
    link_to: str = Field(metadata=dict(title="Name of node this links to"))
    text: str = Field(default="", metadata=dict(title="Text describing the link"))


class Node(BaseModel):
    name: str = Field(metadata=dict(title="Name of node"))
    text: str = Field(default="", metadata=dict(title="Generated node text"))
    links: dict[str, NodeLink] = Field(default_factory=list)


class InteractiveDocument(BaseModel):
    title: str = "Untitled"
    nodes: dict[str, Node] = Field(default_factory=list)
