import os

from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentunderstanding import ContentUnderstandingClient

load_dotenv()

endpoint = os.environ["CONTENT_UNDERSTANDING_ENDPOINT"]
key = os.environ["CONTENT_UNDERSTANDING_KEY"]

client = ContentUnderstandingClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key),
)

def extract_invoice(file_path):
    with open(file_path, "rb") as invoice_file:
        invoice_bytes = invoice_file.read()

    poller = client.begin_analyze_binary(
        analyzer_id="prebuilt-invoice",
        binary_input=invoice_bytes,
    )

    result = poller.result()
    document = result.contents[0]
    fields = document.fields or {}

    def get_field_value(field_name):
        field = fields.get(field_name)
        return getattr(field, "value", None) if field else None

    invoice_data = {
        "supplier": get_field_value("VendorName"),
        "invoice_number": get_field_value("InvoiceId"),
        "invoice_date": get_field_value("InvoiceDate"),
        "customer": get_field_value("CustomerName"),
    }

    total_field = fields.get("TotalAmount")
    total_value = getattr(total_field, "value", {}) if total_field else {}

    if isinstance(total_value, dict):
        invoice_data["total"] = getattr(
            total_value.get("Amount"), "value", None
        )
        invoice_data["currency"] = getattr(
            total_value.get("CurrencyCode"), "value", None
        )

    return invoice_data


if __name__ == "__main__":
    invoice = extract_invoice("festival_supplier_invoice.pdf")

    print(f"Supplier: {invoice.get('supplier')}")
    print(f"Invoice number: {invoice.get('invoice_number')}")
    print(f"Invoice date: {invoice.get('invoice_date')}")
    print(f"Customer: {invoice.get('customer')}")
    print(f"Total: {invoice.get('total'):.2f} {invoice.get('currency')}")
    print(
        "\nThese extracted values are AI-generated "
        "and should be checked against the invoice."
    )