import yaml
import networkx as nx
from langchain.llms.fake import FakeListLLM

from .data_models.base import InteractiveDocument


def read_yaml(filepath):
    with open(filepath, "r") as f:
        yml = yaml.safe_load(f)
    return yml


def get_links(doc: InteractiveDocument):
    for node in doc.nodes:
        for link in node.links:
            # (source, dest)
            yield (node.name, link.link_to)


def draw_graph(g):
    import matplotlib.pyplot as plt

    plt.plot()
    nx.draw_circular(g, with_labels=True)
    plt.show()


def get_fake_llm(responses=None):
    if responses is None:
        responses = list(range(100))
    return FakeListLLM(responses=responses)


def get_llamacpp_llm(model_filepath, **kwargs):
    from langchain.llms import LlamaCpp

    kwargs = (
        dict(
            verbose=False,
            n_gpu_layers=40,
            # full context window
            n_ctx=2048,
            # Infinite max tokens -- rely on prompt to limit tokens
            # max_tokens=-1,
            # seed for replicability
            seed=2023,
            # TODO
            # Test w/ only moderate variability
        )
        | kwargs
    )
    llm = LlamaCpp(model_path=model_filepath, **kwargs)
    return llm
