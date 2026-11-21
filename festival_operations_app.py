from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from text_analysis import analyse_feedback
from speech_analysis import transcribe_report
from vision_analysis import analyse_image
from document_analysis import extract_invoice


endpoint = (
    "https://matt-9712-resource.services.ai.azure.com/"
    "api/projects/matt-9712-resource-project"
)
agent_name = "festival-operations-assistant"


print("Collecting festival evidence...\n")

feedback = analyse_feedback("festival_feedback.txt")
transcript = transcribe_report()
image_observations = analyse_image("festival_site.jpg")
invoice = extract_invoice("festival_supplier_invoice.pdf")

key_phrases = ", ".join(feedback["key_phrases"])

entities = ", ".join(
    f"{entity['text']} ({entity['category']})"
    for entity in feedback["entities"]
)

invoice_total = invoice.get("total")
if isinstance(invoice_total, (int, float)):
    invoice_total = f"{invoice_total:.2f}"

evidence_package = f"""
FESTIVAL EVIDENCE

Written feedback:
{feedback["source_text"]}

Text-analysis results:
- Overall sentiment: {feedback["sentiment"]}
- Key phrases: {key_phrases}
- Entities: {entities}

Spoken staff report transcript:
{transcript}

Festival-site image observations:
{image_observations}

Supplier invoice:
- Supplier: {invoice.get("supplier")}
- Invoice number: {invoice.get("invoice_number")}
- Invoice date: {invoice.get("invoice_date")}
- Customer: {invoice.get("customer")}
- Total: {invoice_total} {invoice.get("currency")}
"""

question = """
Compare only the evidence about the east entrance from:

1. The written attendee feedback.
2. The spoken staff report.
3. The festival-site image observations.

For each source, state exactly what it confirms. Then explain:

- Whether the sources genuinely conflict.
- Whether they might describe different times.
- How the image's limited viewpoint affects certainty.
- What information is still missing.

Do not infer that the entrance is blocked, unsafe or operating poorly.
Do not recommend an operational decision.
"""

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint,
        credential=credential,
        allow_preview=True,
    ) as project_client,
):
    openai_client = project_client.get_openai_client(
        agent_name=agent_name
    )

    conversation = openai_client.conversations.create()

    response = openai_client.responses.create(
        conversation=conversation.id,
        input=[
            {
                "role": "user",
                "content": f"{evidence_package}\n{question}",
            }
        ],
    )

    print("\nFestival Operations Assistant response:\n")
    print(response.output_text)

    print(
        "\nThe response is AI-generated. The festival operations "
        "manager should review the evidence before taking action."
    )