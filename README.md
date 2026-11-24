# Festival Operations Assistant: Lab Build Guide

This guide is for the lab team. Fork this repo, then use this guide to set up the Azure resources and build the lab VM for each student. Students follow a separate lab guide.

The lab's scripts analyse festival evidence (written feedback, a spoken staff report, a site photo and a supplier invoice) with Azure AI services, then send it to an agent the student creates in Microsoft Foundry.

## 1. Set up Azure for each student

Create these in the student's Azure subscription:

| Resource | Type | Used by |
|---|---|---|
| A Foundry resource and project | Microsoft Foundry | `run_agent.py`, `vision_analysis.py`, `document_analysis.py`, `festival_operations_app.py` |
| `qa-lab-speech` | Azure AI Speech | `speech_analysis.py` |
| `qa-lab-language` | Azure AI Language | `text_analysis.py` |

- Put the Foundry resource in a region that supports Content Understanding.
- Language endpoint names must be unique across Azure. If more than one student's environment uses the name `qa-lab-language`, give each resource a unique custom domain name.

Give the student's lab account:

- The **Azure AI User** role on the Foundry project
- Permission to view the keys of the Foundry, Speech and Language resources
- Permission to deploy models and configure Content Understanding on the Foundry resource

Don't create these, because the student does them during the lab:

- The `gpt-5` and `gpt-5-mini` model deployments
- The `festival-operations-assistant` agent
- The Content Understanding setup in Content Understanding Studio

## 2. Install the tools on the VM

- VS Code with the Python extension
- Git
- Python 3.10 or later
- Azure CLI (`az`)

To check whether the Azure CLI is installed, run `az --version` in a terminal. If the command isn't found, install it:

- **Windows:** `winget install --exact --id Microsoft.AzureCLI`, or use the [MSI installer](https://aka.ms/installazurecliwindows)
- **macOS:** `brew install azure-cli`
- **Linux:** follow the [Azure CLI install guide](https://learn.microsoft.com/cli/azure/install-azure-cli-linux)

Then close and reopen the terminal (on Windows, restart VS Code) so it can find `az`.

## 3. Get the code

Clone your fork onto the VM. In VS Code, open the Command Palette (`Ctrl+Shift+P`, or `Cmd+Shift+P` on macOS), run **Git: Clone**, paste your fork's URL and open the cloned folder.

Or, in a terminal:

```bash
git clone <your-fork-url>
cd festival-operations-lab
```

## 4. Install the Python packages

Open a terminal in VS Code (``Ctrl+` ``). On Windows, check that the shell name at the top right of the terminal panel says **PowerShell**. If it says Command Prompt or Git Bash, use the dropdown arrow next to the `+` to open a PowerShell terminal instead. Make sure the terminal is in the `festival-operations-lab` folder.

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

**macOS / Linux**

```bash
./install.sh
source .venv/bin/activate
```

Both create `.env` from `.env.example`. Leave its values empty, because the student fills them in during the lab.

If VS Code asks which Python interpreter to use, choose the one in `.venv`.

## 5. Test the build

To check the build works, sign in with a test account that has the same access as a student, fill in `.env`, and run the scripts.

```bash
az login
```

The agent and image-analysis scripts use this Entra ID sign-in rather than a key. If the account has more than one tenant, use `az login --tenant <tenant-id>`.

Before you capture or hand over the VM, run `az logout` and clear the values in `.env`, so the student starts with a clean environment.

## Troubleshooting

| Problem | Fix |
|---|---|
| `Missing setting: ...` | That value is empty in `.env`. Fill it in and run again. |
| `ModuleNotFoundError` | The virtual environment isn't active. Run `source .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\Activate.ps1` (Windows). |
| `command not found: az` (macOS/Linux) or `The term 'az' is not recognized` (Windows) | The Azure CLI isn't installed, or the terminal opened before it was installed. Install it (see [step 2](#2-install-the-tools-on-the-vm)), then open a new terminal. On Windows, restart VS Code. |
| `DefaultAzureCredential failed to retrieve a token` | Run `az login` again. |
| `PermissionDenied` or `401`/`403` from the agent | The account needs the **Azure AI User** role on the Foundry project. |
| `Error code: 400 ... There was an issue with your request` from the agent | Make sure the agent uses `gpt-5` or `gpt-5-mini`, not `model-router`. |
| `NotOpenSSLWarning` from `urllib3` | Harmless. It appears with older macOS system Python. |
| "running scripts is disabled on this system" when running `.venv\Scripts\Activate.ps1` | PowerShell is blocking scripts. Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then activate again. |
