# Before running the sample:
#    pip install "azure-ai-projects>=2.1.0"

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

endpoint = "https://matt-9712-resource.services.ai.azure.com/api/projects/matt-9712-resource-project"
agent_name = "festival-operations-assistant"


with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint,
        credential=credential,
        allow_preview=True,
    ) as project_client,
):
    # Bind the OpenAI client to the existing agent endpoint.
    openai_client = project_client.get_openai_client(agent_name=agent_name)

    # GitHub Copilot preview agents require a conversation for every Responses turn.
    conversation = openai_client.conversations.create()

    print("Festival Operations Assistant")
    print("Responses are AI-generated and should be reviewed.")
    print("Enter 'quit' to end the conversation.\n")

    while True:
        user_message = input("You: ").strip()

        if user_message.lower() == "quit":
            print("Conversation ended.")
            break

        if not user_message:
            continue

        response = openai_client.responses.create(
            conversation=conversation.id,
            input=[{"role": "user", "content": user_message}],
        )

        print(f"\nAssistant: {response.output_text}\n")
