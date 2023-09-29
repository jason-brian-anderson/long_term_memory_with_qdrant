"""
An example of extension. It does nothing, but you can add transformations
before the return statements to customize the webui behavior.

Starting from history_modifier and ending in output_modifier, the
functions are declared in the same order that they are called at
generation time.
"""

import gradio as gr

from extensions.long_term_memory.long_term_memory import LTM

from modules import chat


params = {
    "display_name": "Long Term Memory",
    "is_tab": False,
    "limit": 3,
    "address": "http://qdrant:6333",
    "query_output": "vdb search results",
    'verbose': True,
}


def state_modifier(state):
    """
    Modifies the state variable, which is a dictionary containing the input
    values in the UI like sliders and checkboxes.
    """
    state['limit'] = params['limit']
    state['address'] = params['address']
    return state


def custom_generate_chat_prompt(user_input, state, **kwargs):
    """
    Replaces the function that generates the prompt from the chat history.
    Only used in chat mode.
    """

    prompt_line = chat.generate_chat_prompt(user_input, state, **kwargs)
    prompts = prompt_line.split("\n")
    if params['verbose']:
        print("****initial prompt****\n")
        for count, prompt_line in enumerate(prompts, 1):
            print(f"({count}/{len(prompts)}):  {prompt_line}")

    collection = state['name2'].strip()
    username = state['name1'].strip()
    verbose = params['verbose']
    limit = params['limit']
    address = params['address']
    ltm = LTM(collection, verbose, limit, address=address)

    long_term_memories = ltm.store_and_recall(user_input)
    long_term_memories = [
        f"{username}: {memory}" for memory in long_term_memories]

    state['query_output'] = "\n".join(long_term_memories)

    # insert the formated vdb outputs after the context but before the chat his
    # tory, this placement seems to work fine but could be played with.
    prompts[1:1] = long_term_memories

    if params['verbose']:
        print("****final prompt with injected memories****\n")
        for count, prompt_line in enumerate(prompts, 1):
            print(f"({count}/{len(prompts)}):  {prompt_line}")

    prompts = "\n".join(prompts)
    return prompts


def setup():
    """
    Gets executed only once, when the extension is imported.
    """
    pass


def ui():
    """
    Gets executed when the UI is drawn. Custom gradio elements and
    their corresponding event handlers should be defined here.

    To learn about gradio components, check out the docs:
    https://gradio.app/docs/
    """

    # Gradio elements
    with gr.Accordion("Long Term Memory"):
        with gr.Row():
            limit = gr.Slider(
                1, 10,
                step=1,
                value=params['limit'],
                label='Long Term Memory Result Count (Top N scoring results)',
                )
            limit.change(lambda x: params.update({'limit': x}), limit, None)
