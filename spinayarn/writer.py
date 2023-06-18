import json
from pathlib import Path

from .data_models import InteractiveStory


def write_story_json(story: InteractiveStory, filepath: str | Path):
    filepath = Path(filepath)
    # filename: str, path: str | Path = "."
    # if not filename.endswith(".json"):
    #     filename = f"{filename}.json"
    # filepath = Path(path) / filename
    # s = json.dumps(story.dict(), indent=4)
    with open(filepath, "w") as f:
        f.write(story.json(indent=4))
    return filepath


def write_story_twee3(story: InteractiveStory, filepath: str | Path):
    import uuid

    # if not filename.endswith(".twee"):
    #     filename = f"{filename}.twee"
    # filepath = Path(path) / filename
    filepath = Path(filepath)
    with open(filepath, "w") as f:
        # write header
        f.write(":: StoryTitle\n")
        f.write(story.title)
        f.write("\n" * 2)
        f.write(":: StoryData\n")
        metadata = {
            "ifid": str(uuid.uuid1()),
            "format": "Chapbook",
            "format-version": "1.2.3",
            "start": "start",
            "zoom": 1,
        }
        f.write(json.dumps(metadata, indent=2))
        f.write("\n" * 2)
        # note: start node should be first
        for node in story.nodes.values():
            write_node_twee3(f, node)
        # write each node
        # write node text
        # write links
    return filepath


def write_node_twee3(f, node):
    f.write(f":: {node.name}\n")
    f.write(node.text)
    for link in node.links.values():
        f.write(f"\n[[{link.text}|{link.link_to}]]")
    f.write("\n\n")
