import base64

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from config import get_setting

endpoint = get_setting("FOUNDRY_PROJECT_ENDPOINT")
model_name = get_setting("FOUNDRY_MODEL_DEPLOYMENT")


def analyse_image(file_path):
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(
            endpoint=endpoint,
            credential=credential,
            allow_preview=True,
        ) as project_client,
    ):
        openai_client = project_client.get_openai_client()

        response = openai_client.responses.create(
            model=model_name,
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "Review this festival-site image. List only visible "
                                "operational observations about entrances, crowding, "
                                "waste, barriers and signage. Do not identify people, "
                                "infer personal characteristics or claim anything "
                                "that is not visibly supported. Highlight uncertainty."
                            ),
                        },
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{encoded_image}",
                        },
                    ],
                }
            ],
        )

        return response.output_text


if __name__ == "__main__":
    observations = analyse_image("festival_site.jpg")

    print("Image-analysis observations:")
    print(observations)
    print("\nThis analysis is AI-generated and should be checked against the image.")