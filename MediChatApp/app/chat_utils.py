from euriai.langchain import create_chat_model

def get_chat_model(api_key: str, model_name: str = "gpt-4.1-nano", temperature: float = 0.7):
    """
    Initialize and return a chat model using the specified model name and temperature.

    Args:
        model_name (str): The name of the chat model to use (default is "gpt-4").
        temperature (float): The temperature setting for the model (default is 0.7).

    Returns:
        ChatModel: An instance of the chat model.
    """
    chat_model = create_chat_model(api_key=api_key, model=model_name, temperature=temperature)
    return chat_model

def ask_chat_model(chat_model, prompt: str):
    """
    Send a prompt to the chat model and return the response.

    Args:
        chat_model (ChatModel): The chat model instance.
        prompt (str): The prompt string to send to the model.

    Returns:
        str: The response from the chat model.
    """
    response = chat_model.invoke(prompt)
    return response.content