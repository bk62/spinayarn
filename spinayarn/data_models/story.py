"""Data models for interactive stories."""
from enum import Enum
from pathlib import Path

from pydantic import Field

from .base import NodeLink, Node, InteractiveDocument


class StoryNodeLink(NodeLink):
    pass


class StoryNode(Node):
    plot: str = Field(metadata=dict(title="Plot of the node"))
    links: dict[str, StoryNodeLink] = Field(default_factory=list)
    prompt: str | None = Field(
        default=None, metadata=dict(title="Prompt used to generate node text")
    )

    def add_link(self, link_to, link_text):
        self.links[link_to] = StoryNodeLink(link_to=link_to, text=link_text)

    def clear_links(self):
        self.links = dict()
        return self


class InteractiveStoryType(str, Enum):
    outline = "outline"
    generated = "generated"


class InteractiveStory(InteractiveDocument):
    type: InteractiveStoryType = InteractiveStoryType.outline

    pov: str | None = "third person"
    style: str | None = "simple and clear"
    audience: str | None = ""
    central_theme: str | None = ""
    tone: str | None = ""
    pacing: str | None = ""
    setting: str | None = Field(default=None, metadata=dict(title="Story setting"))
    style_examples: list[str] = Field(default_factory=list)

    nodes: dict[str, StoryNode] = Field(default_factory=list)

    def export_to_dict(self, include={}):
        return self.dict(
            include={
                "title": True,
                # TODO
                "nodes": {"name": True, "text": True, "links": {"link_to", "text"}},
            }
            | include
        )

    def get_node(self, node_name):
        return self.nodes[node_name]

    def add_node(self, node: StoryNode):
        self.nodes[node.name] = node

    def clear_nodes(self):
        self.nodes = dict()
        return self

    def build_generated_node(
        self, outline_node: StoryNode, node_text: str, node_name: str
    ):
        # copy outline node w/out links
        new_node = outline_node.copy(deep=True).clear_links()
        new_node.name = node_name
        # insert generated text
        new_node.text = node_text
        # copy over modified links
        # with prefix b/c node names might be different (i.e. path dependent)
        # in generated nodes
        for link in outline_node.links.values():
            linked_node = f"{node_name}__{link.link_to}"
            new_node.add_link(linked_node, link.text)
        self.add_node(new_node)
        return new_node

    def set_type(self, type=InteractiveStoryType):
        self.type = type
        return self

    def generate_copy(self):
        return (
            self.copy(deep=True).clear_nodes().set_type(InteractiveStoryType.generated)
        )

    def get_or_create_node(self, node_name: str):
        try:
            return self.nodes[node_name]
        except KeyError:
            self.nodes[node_name] = StoryNode(name=node_name)
            return self.nodes[node_name]

    def is_outline(self):
        return self.type == InteractiveStoryType.outline

    def is_generated(self):
        return self.type == InteractiveStoryType.generated

    @staticmethod
    def from_dict(story_spec_dict):
        # TODO validation errors
        nodes = {}
        for name, node in story_spec_dict["nodes"].items():
            links = {
                lname: StoryNodeLink(link_to=lname, text=ltext)
                for lname, ltext in node.get("links", {}).items()
            }
            node = StoryNode(
                name=name, plot=node["plot"], links=links
            )
            nodes[name] = node
        story = InteractiveStory.parse_obj(story_spec_dict | dict(nodes=nodes))
        return story

    # Convenience wrapper methods:
    @staticmethod
    def from_outline_yaml(filepath):
        from ..reader import load_story_outline
        return load_story_outline(filepath)

    def to_json_file(self, filepath: Path | str) -> Path:
        from ..writer import write_story_json
        return write_story_json(self, filepath)

    def to_twee3_file(self, filepath: Path | str) -> Path:
        if not self.is_generated():
            raise Exception("Cannot write story outline to Twee3 file.")
        from ..writer import write_story_twee3
        return write_story_twee3(self, filepath)
