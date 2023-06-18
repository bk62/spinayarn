"""Alpaca style prompts for storywriting."""
from langchain.prompts.pipeline import PipelinePromptTemplate
from langchain.prompts.prompt import PromptTemplate


story_attrs_template = """The protagonist: {protagonist}
The setting is: {setting}"""
start_or_continue_prompt_template = """{% if story_so_far %}
Read the following partially written story delimited by triple backticks
```
{{story_so_far}}
```
Your task will be to write the paragraph that comes after the above while following the given instructions and ensuring that details in the story are consistent.
{% else %}
Write the opening paragraph of the story.
{% endif %}"""
story_prompt_template = """Below is an instruction that describes a task, paired with an input that provides further context.
### Instruction:
You are an AI writer who writes individual scenes for short stories from a plot outlines.
You writing style is simple and clear.
The story must be written in first person point of view.
{StoryAttributesPrompt}
{StartOrContinuePrompt}
You will be given a prompt with short descriptions of the plot of the story.
You must then write a single paragraph with a maximum of 2 lines setting up the described scene using vivid and descriptive language.

Your story must follow the plot exactly.
There should not be any incomplete sentences in the story.

The story must end abruptly where the text `END` appears in the plot.
{PlotPrompt}

### Response:"""
plot_prompt_template = """
{additional_instructions}
### Input:
Plot: {plot} END"""
story_attrs_prompt = PromptTemplate.from_template(story_attrs_template)
start_or_continue_prompt = PromptTemplate.from_template(
    template=start_or_continue_prompt_template, template_format="jinja2"
)
plot_prompt = PromptTemplate(
    template=plot_prompt_template, input_variables=["plot", "additional_instructions"]
)
story_final_prompt = PromptTemplate.from_template(
    template=story_prompt_template,
)
story_prompt = PipelinePromptTemplate(
    final_prompt=story_final_prompt,
    pipeline_prompts=[
        ("StoryAttributesPrompt", story_attrs_prompt),
        ("StartOrContinuePrompt", start_or_continue_prompt),
        ("PlotPrompt", plot_prompt),
    ],
    input_variables=[
        "story_so_far",
        "setting",
        "protagonist",
        "additional_instructions",
        "plot",
        "num_lines",
    ],
)
