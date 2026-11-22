# Festival Operations Assistant: Lab Setup

This repo contains the sample code for the Festival Operations Assistant lab. The scripts analyse festival evidence (written feedback, a spoken staff report, a site photo and a supplier invoice) with Azure AI services, then send it to an agent you create in Microsoft Foundry.

## What you need

- An Azure subscription with a Microsoft Foundry resource and project
- The **Azure AI User** role on the Foundry project, plus permission to view the resource's keys
- VS Code with the Python extension
- Git
- Python 3.10 or later
- Azure CLI (`az`)

## 1. Deploy a model and create an agent

In the [Foundry portal](https://ai.azure.com), open your project, then:

1. Go to **Models + endpoints** and select **Deploy model**. Deploy `gpt-5` (or `gpt-5-mini`) and note the deployment name.
2. Go to **Agents** and create a new agent named `festival-operations-assistant`. Select the model you just deployed.
3. Go to the project **Overview** page and copy the **Project endpoint**.

> Don't use `model-router` as the agent's model. It rejects the full evidence package used in this lab.

## 2. Get the code

In VS Code, open the Command Palette (`Ctrl+Shift+P`, or `Cmd+Shift+P` on macOS), run **Git: Clone**, paste the repo URL and open the cloned folder.

Or, in a terminal:

```bash
git clone <repo-url>
cd <repo-folder>
```

## 3. Install the Python packages

Open a terminal in VS Code (``Ctrl+` ``).

**macOS / Linux**

```bash
./install.sh
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Your prompt shows `(.venv)` when the environment is active. Activate it again in every new terminal.

If VS Code asks which Python interpreter to use, choose the one in `.venv`.

## 4. Fill in your settings

Open `.env` (created from `.env.example`) and fill in every value:

| Setting | Where to find it |
|---|---|
| `FOUNDRY_PROJECT_ENDPOINT` | Foundry portal > project **Overview** > **Project endpoint** |
| `FOUNDRY_AGENT_NAME` | The name of the agent you created |
| `FOUNDRY_MODEL_DEPLOYMENT` | The deployment name of the model you deployed |
| `SPEECH_KEY`, `AZURE_LANGUAGE_KEY`, `CONTENT_UNDERSTANDING_KEY` | Azure portal > Foundry resource > **Keys and Endpoint** > **KEY 1** |
| `SPEECH_REGION` | Same page, **Location/Region** (e.g. `swedencentral`) |
| `AZURE_LANGUAGE_ENDPOINT` | `https://<resource-name>.cognitiveservices.azure.com/` |
| `CONTENT_UNDERSTANDING_ENDPOINT` | `https://<resource-name>.services.ai.azure.com/` |

`.env` is ignored by Git, so your keys are never committed.

## 5. Sign in to Azure

The agent and image-analysis scripts use your Entra ID sign-in rather than a key.

```bash
az login
```

Sign in with your lab account. If you have more than one tenant, use `az login --tenant <tenant-id>`.

## 6. Run the scripts

Each analysis script can be run on its own:

```bash
python text_analysis.py       # sentiment, key phrases and entities from festival_feedback.txt
python speech_analysis.py     # transcribes festival_site_report.wav
python vision_analysis.py     # describes festival_site.jpg
python document_analysis.py   # extracts fields from festival_supplier_invoice.pdf
```

Chat with your agent:

```bash
python run_agent.py
```

Run the full app, which gathers all the evidence and asks the agent to compare it:

```bash
python festival_operations_app.py
```

## Troubleshooting

| Problem | Fix |
|---|---|
| `Missing setting: ...` | That value is empty in `.env`. Fill it in and run again. |
| `ModuleNotFoundError` | The virtual environment isn't active. Run `source .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\Activate.ps1` (Windows). |
| `command not found: az` | Install the Azure CLI, then open a new terminal. |
| `DefaultAzureCredential failed to retrieve a token` | Run `az login` again. |
| `PermissionDenied` or `401`/`403` from the agent | Your account needs the **Azure AI User** role on the Foundry project. |
| `Error code: 400 ... There was an issue with your request` from the agent | Make sure the agent uses `gpt-5` or `gpt-5-mini`, not `model-router`. |
| `NotOpenSSLWarning` from `urllib3` | Harmless. It appears with older macOS system Python. |
