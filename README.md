# TrialAgent: A Self-Driving Clinical Lab

**Ayush Noori**

Artificial intelligence (AI) offers unprecedented opportunities to understand disease biology, repurpose existing drugs ([Zitnik, 2024](https://www.nature.com/articles/s41591-024-03233-x)), and advance towards novel therapeutics for complex diseases ([Zitnik, 2025](https://www.nature.com/articles/s41591-025-03832-2)). For example, there is an active effort underway to create "virtual cell" models, or computational models that simulate the functions and reactions of the cell ([Bunne, 2024](https://www.cell.com/cell/fulltext/S0092-8674\(24\)01332-1)). These models aim to predict responses to drugs, including small-molecule and genetic perturbations ([Adduri, 2025](https://www.biorxiv.org/content/10.1101/2025.06.26.661135v2)), setting the stage for "*in silico* clinical trials" ([Gandhi, 2025](https://www.biorxiv.org/content/10.1101/2025.10.23.683759v1); [Tahoe Team, 2025](https://www.tahoebio.ai/news/tahoe-x1-blog)). However, current virtual cell efforts suffer from a knowledge gap: they are currently trained largely on gene expression data, which captures only one modality, often at only one time point, and within a limited repertoire of perturbations, cell types, or other contexts. Moreover, even if we are successfully able to recapitulate the behavior or responses of a single cell, the therapeutic insights gleaned may not translate to the level of tissues or the whole human organism.

Alternatively, some of the critical missing data signals in modeling whole human responses to external factors in health and disease can be recovered through analyses of real-world, population-scale observational health data. Prospective analyses, in the form of randomized controlled trials (RCTs), are the gold standard for validating therapeutic hypotheses; however, they are lengthy, expensive, and challenging to conduct. Where RCTs are resource-prohibitive, retrospective analyses, known as real-world evidence (RWE) studies, can be performed on electronic health records (EHRs) or other types of real-world data (RWD) routinely collected during healthcare delivery to derive signals about the "benefits or risks of medical products" ([Concato and Corrigan-Curay, 2022](https://www.nejm.org/doi/full/10.1056/NEJMp2200089); [U.S. FDA, 2025](https://www.fda.gov/drugs/development-resources/advancing-real-world-evidence-program)). However, RWE is often still difficult to collect: due to the intricacies of structured data curation and harmonization, cohort design, causal modeling, and appropriate correction for confounding factors, there exist standalone papers for individual emulated RCTs. Approaches such as TRIALSCOPE ([González, 2025](https://ai.nejm.org/doi/full/10.1056/AIoa2400859)) structure clinical text at scale to facilitate target trial emulation; however, there still does not exist a unified platform capable of:
1. Automatically and scalably extracting RWE from structured RWD.
2. Adaptively learning from RWE to propose, design, and execute new causal experiments.
3. Extending beyond predicting "benefits or risks of medical products" to connect these macroscopic clinical insights back to the molecular scale.

Here, we propose TrialAgent, an AI agent-based self-driving clinical lab. The experiments TrialAgent conducts are not with pipettes, robotics, or embodied systems; rather, TrialAgent performs emulated target trials, survival analyses, and other retrospective exposure-outcome cohort studies. Unlike previous tools (*e.g.*, TRIALSCOPE), which act as assistants for human-designed trials, TrialAgent is an autonomous investigator capable of designing, executing, and interpreting thousands of emulated trials to generate new biological hypotheses. Importantly, TrialAgent integrates RWE with molecular and cellular data – including drug interactions, mechanisms of action, protein-protein interactions, and cellular organization – from biomedical knowledge graphs (*e.g.*, OptimusKG) to identify new drug targets and suggest new mechanisms of disease pathology based on signals from RWE.

TrialAgent serves as the macroscopic counterpart to the microscopic virtual cell. By linking molecular mechanisms (via KGs) to population-level outcomes (via RWE), we create a closed-loop system for biological discovery grounded in human health.

## Model Architecture

Inspired by the Virtual Lab ([Swanson, 2025](https://www.nature.com/articles/s41586-025-09442-9)), TrialAgent utilizes a closed-loop, multi-agent architecture. TrialAgent treats a biomedical knowledge graph (KG) as a dynamic world model that evolves as agents extract facts from RWD. The architecture consists of two modules connected by an iterative feedback loop:

### Hypothesis Generation Module

This module is composed of the following agents:

1. **Clinical supervisor agent.** The supervisor agent oversees the outputs of emulated trials run across a wide pharmacopeia, identifies unexpected signals (e.g., a diabetes drug reducing Alzheimer's risk), and generates new hypotheses on pathways of pathology. For example, if Drug X (targeting Protein Y) mitigates Disease Z in RWE, Protein Y is implicated in the etiology of Disease Z.

   Importantly, instead of randomly testing associations, the trial lead agent traverses the KG-based world model to identify interesting or biologically plausible drug-disease links that lack clinical validation. For example, consider the following workflow. First, a human researcher provides a "seed node," such as "Alzheimer's disease."

   The Supervisor agent identifies all drugs within the two-hop neighborhood of the seed node; then, from this list, the agent selects drugs with epistemic uncertainty or high therapeutic potential as candidate links. The supervisor agent filters pairs based on feasibility, selecting drugs without existing links to Alzheimer's and that have been approved for a non-Alzheimer's indication, and ensuring the drugs and diseases map to specific ICD-9 and ATC-5 codes present in the EHR data. The agent then passes hypotheses to the Tournament agent.

2. **Tournament agent.** Inspired by Google's AI Co-Scientist ([Gottweis, 2025](https://arxiv.org/abs/2502.18864)), for every potential link, evidence is accumulated both for and against a given hypothesis. Specifically, the Tournament agent formulates a competitive pair: a Primary Hypothesis (H1, e.g., "Metformin reduces the hazard ratio of Alzheimer's onset"), and a corresponding Competing Hypothesis (H-1, e.g., "Metformin increases the hazard ratio of Alzheimer's onset") and/or Null Hypothesis (H0). The Tournament agent orchestrates a tournament between the Primary Hypothesis and the Competing Hypothesis. Each hypothesis is passed to the Laboratory module, which accumulates evidence supporting the hypothesis under a fixed runtime budget.

3. **Judge agent.** After the Laboratory module returns supporting evidence, this agent compares the evidence for H1 against H-1 or H0.
   - Decision logic: Only signals that overwhelmingly defeat both the Null and the Competing Hypotheses are committed to the KG-based world model. If the result is ambiguous or the null holds, the hypothesis is discarded or flagged for refinement.
   - World model update: If H1 wins the tournament, it is converted into a new "fact" and added as an edge (with a specific "discovery" edge type) to the KG-based world model.
   - Feedback loop: The supervisor agent is notified of all updates to the world model, which it can use to traverse further into the KG and generate second-order hypotheses.

### Laboratory Module

This module is composed of the following agents:

1. **Data scientist agent** for cohort construction. Maps natural language concepts to specific diagnosis (ICD-9, CHR, and ICPC) and medication (ATC-5) codes, and defines inclusion and exclusion criteria.

2. **Clinical agent** for confounder identification. Identifies necessary covariates and potential confounders for a specific disease-drug pair. Confounders are provided to the cohort construction agent to include in the cohort design.

3. **Statistician agent.** Selects and executes the appropriate causal inference model (e.g., Cox proportional hazards, propensity score matching, inverse probability weighting, prevalence analyses).

4. **Critic agent.** Validates the trial design and proposes improvements.


## Setup

### Hugging Face Hub with JFrog Artifactory

To configure Hugging Face Hub to work with JFrog Artifactory, you need to set the following environment variables:

**Using uv (Recommended):**

**Option 1: Use the helper script (easiest)**

On Unix/macOS:
```bash
./run_with_hf.sh test-supervisor
```

On Windows:
```cmd
run_with_hf.bat test-supervisor
```

The script will automatically create a `.env` file if it doesn't exist.

**Option 2: Create .env file manually**

Create a `.env` file in the project root with:

```bash
HF_HUB_ETAG_TIMEOUT=86400
HF_HUB_DOWNLOAD_TIMEOUT=86400
HF_ENDPOINT=https://jfrog.apps.ocpdmzp.wclalit.org.il/artifactory/api/huggingfaceml/huggingface
HF_TOKEN=cmVmdGtu0jAx0jE3OTgwMTIxNDY6Q11zTXp4RHAYRXI2b3Z6bn1WMWRBSUthSnNp
```

Then run commands with:

```bash
uv run --env-file .env test-supervisor
```

**Option 3: Inline environment variables**

```bash
uv run --env HF_ENDPOINT=https://jfrog.apps.ocpdmzp.wclalit.org.il/artifactory/api/huggingfaceml/huggingface --env HF_TOKEN=cmVmdGtu0jAx0jE3OTgwMTIxNDY6Q11zTXp4RHAYRXI2b3Z6bn1WMWRBSUthSnNp test-supervisor
```

**Manual setup (alternative methods):**

**On Unix/Linux/macOS (bash/zsh):**

```bash
export HF_HUB_ETAG_TIMEOUT=86400
export HF_HUB_DOWNLOAD_TIMEOUT=86400
export HF_ENDPOINT=https://jfrog.apps.ocpdmzp.wclalit.org.il/artifactory/api/huggingfaceml/huggingface
export HF_TOKEN=<your-token>
```

For convenience, you can source the provided setup script:

```bash
source setup_hf.sh
```

**On Windows (Command Prompt):**

Run the batch file using `call` to set variables in the current shell:

```cmd
call setup_hf.bat
```

Or set the variables directly in your current shell:

```cmd
set HF_HUB_ETAG_TIMEOUT=86400
set HF_HUB_DOWNLOAD_TIMEOUT=86400
set HF_ENDPOINT=https://jfrog.apps.ocpdmzp.wclalit.org.il/artifactory/api/huggingfaceml/huggingface
set HF_TOKEN=cmVmdGtu0jAx0jE3OTgwMTIxNDY6Q11zTXp4RHAYRXI2b3Z6bn1WMWRBSUthSnNp
```

**On Windows (PowerShell):**

**Option 1: Set variables directly (Recommended - avoids execution policy issues):**

```powershell
$env:HF_HUB_ETAG_TIMEOUT = "86400"
$env:HF_HUB_DOWNLOAD_TIMEOUT = "86400"
$env:HF_ENDPOINT = "https://jfrog.apps.ocpdmzp.wclalit.org.il/artifactory/api/huggingfaceml/huggingface"
$env:HF_TOKEN = "cmVmdGtu0jAx0jE3OTgwMTIxNDY6Q11zTXp4RHAYRXI2b3Z6bn1WMWRBSUthSnNp"
```

**Option 2: Bypass execution policy for this script:**

```powershell
powershell -ExecutionPolicy Bypass -File .\setup_hf.ps1
```

**Option 3: Use the batch file from PowerShell:**

```powershell
cmd /c "call setup_hf.bat"
```

**Note:** For Hugging Face client version 0.19.0 and above, the `HF_HUB_ETAG_TIMEOUT` parameter allows you to resolve models using pipelines and tokenizers.

### Installation with uv

Install dependencies using uv:

```bash
uv sync
```
