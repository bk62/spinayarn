"""Functions to read InteractiveStory Spec Files."""
from . import data_models
from . import utils


def load_story_outline(filepath):
    story_spec_dict = utils.read_yaml(filepath)
    story = data_models.InteractiveStory.from_dict(story_spec_dict["story_outline"])
    return story
