from g4f.client import Client


def get_gpt_response(messages=None, model="gpt-4o", temperature=0):
    """
    Sends a chat completion request to the specified model using g4f Client.

    Args:
        messages (list): List of message dicts (e.g., [{"role": "user", "content": "Hello"}])
        model (str): The model name (default is "gpt-4o")
        temperature (float): Sampling temperature (default is 0)

    Returns:
        str: The content of the model's response
    """
    if messages is None:
        messages = []

    client = Client()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )

    return response.choices[0].message.content
