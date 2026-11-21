import os

from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

load_dotenv()

language_endpoint = os.environ["AZURE_LANGUAGE_ENDPOINT"]
language_key = os.environ["AZURE_LANGUAGE_KEY"]

text_analytics_client = TextAnalyticsClient(
    endpoint=language_endpoint,
    credential=AzureKeyCredential(language_key),
)

def analyse_feedback(file_path):
    with open(file_path, "r", encoding="utf-8") as feedback_file:
        feedback_text = feedback_file.read()

    sentiment_result = text_analytics_client.analyze_sentiment(
        documents=[feedback_text]
    )[0]

    key_phrase_result = text_analytics_client.extract_key_phrases(
        documents=[feedback_text]
    )[0]

    entity_result = text_analytics_client.recognize_entities(
        documents=[feedback_text]
    )[0]

    if sentiment_result.is_error:
        raise RuntimeError(
            f"Sentiment error: {sentiment_result.error}"
        )

    if key_phrase_result.is_error:
        raise RuntimeError(
            f"Key-phrase error: {key_phrase_result.error}"
        )

    if entity_result.is_error:
        raise RuntimeError(
            f"Entity error: {entity_result.error}"
        )

    return {
        "source_text": feedback_text,
        "sentiment": sentiment_result.sentiment,
        "key_phrases": list(key_phrase_result.key_phrases),
        "entities": [
            {
                "text": entity.text,
                "category": entity.category,
            }
            for entity in entity_result.entities
        ],
    }


if __name__ == "__main__":
    analysis = analyse_feedback("festival_feedback.txt")

    print(f"Overall sentiment: {analysis['sentiment']}")

    print("\nKey phrases:")
    for phrase in analysis["key_phrases"]:
        print(f"- {phrase}")

    print("\nEntities:")
    if analysis["entities"]:
        for entity in analysis["entities"]:
            print(
                f"- {entity['text']} "
                f"({entity['category']})"
            )
    else:
        print("- No entities identified")

    print(
        "\nThese results are AI-generated "
        "and should be reviewed."
    )