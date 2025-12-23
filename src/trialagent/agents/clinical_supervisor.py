"""Clinical Supervisor Agent for TrialAgent.

The supervisor agent oversees the outputs of emulated trials, identifies unexpected
signals, and generates new hypotheses on pathways of pathology.
"""

import os
import re
from typing import List, Optional

from rich.console import Console
from transformers import AutoModelForCausalLM, AutoTokenizer

console = Console()


class ClinicalSupervisorAgent:
    """Clinical supervisor agent that uses Qwen as its reasoning backbone.
    """
    
    def __init__(
        self,
        model_name: str = "Qwen/Qwen3-8B",
        device: str = "cpu",
        enable_thinking: bool = False,
    ):
        """Initialize the clinical supervisor agent.
        
        Args:
            model_name: HuggingFace model identifier for Qwen
            device: Device to run inference on (default: "cpu")
            enable_thinking: Enable thinking mode for Qwen3 (default: False for efficiency)
        """
        self.model_name = model_name
        self.device = device
        self.enable_thinking = enable_thinking
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self) -> None:
        """Load Qwen model and tokenizer for CPU inference."""
        # Check if HF_ENDPOINT is set (for JFrog)
        hf_endpoint = os.getenv("HF_ENDPOINT")
        if hf_endpoint:
            console.print(f"[dim]Using HuggingFace endpoint: {hf_endpoint}[/dim]")
        else:
            console.print("[yellow]Warning: HF_ENDPOINT not set. Run: setup_hf.bat[/yellow]")
        
        console.print(f"[bold blue]Loading Qwen model: {self.model_name}[/bold blue]")
        
        console.print("[dim]Loading tokenizer...[/dim]")
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
        )
        
        console.print("[dim]Loading model...[/dim]")
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype="auto",
            device_map=None,
            trust_remote_code=True,
            low_cpu_mem_usage=True,
        )
        self.model = self.model.to(self.device)
        
        console.print("[bold green]✓ Model loaded successfully[/bold green]")
    
    def generate_hypothesis(
        self,
        seed_disease: str,
        context: Optional[str] = None,
        max_new_tokens: int = 512,
    ) -> str:
        """Generate a hypothesis about potential drug-disease relationships.
        
        Args:
            seed_disease: The seed disease node (e.g., "Alzheimer's disease")
            context: Optional context about available drugs or knowledge graph info
            max_new_tokens: Maximum tokens to generate
            
        Returns:
            Generated hypothesis text
        """
        system_prompt = """You are a clinical supervisor agent in a self-driving clinical laboratory. 
Your role is to identify unexpected signals from clinical trials and generate hypotheses about 
drug-disease relationships. You analyze patterns in real-world evidence to suggest biologically 
plausible connections between drugs and diseases."""
        
        user_prompt = f"""Given the seed disease: {seed_disease}
        
Generate a hypothesis about potential drug-disease relationships. Consider:
1. Drugs that might target pathways related to this disease
2. Unexpected signals (e.g., a diabetes drug reducing Alzheimer's risk)
3. Biological plausibility of the connection

{context if context else ""}

Provide a concise hypothesis about a potential drug-disease link."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=self.enable_thinking,
        )
        
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.device)
        
        # Qwen3 best practices: thinking mode uses different parameters
        if self.enable_thinking:
            temperature, top_p, top_k = 0.6, 0.95, 20
        else:
            temperature, top_p, top_k = 0.7, 0.8, 20
        
        with console.status("[bold yellow]Generating hypothesis...[/bold yellow]"):
            generated_ids = self.model.generate(
                **model_inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                do_sample=True,
            )
        
        generated_ids = [
            output_ids[len(input_ids):] 
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        # Parse thinking content for Qwen3 if thinking mode is enabled
        if self.enable_thinking:
            response = self._parse_thinking_content(response)
        
        return response
    
    def identify_candidate_drugs(
        self,
        seed_disease: str,
        max_new_tokens: int = 256,
    ) -> str:
        """Identify candidate drugs for a given seed disease.
        
        Args:
            seed_disease: The seed disease node
            max_new_tokens: Maximum tokens to generate
            
        Returns:
            List of candidate drugs with brief rationale
        """
        system_prompt = """You are a clinical supervisor agent. Your task is to identify 
candidate drugs that might have therapeutic potential for a given disease, even if they 
are not currently approved for that indication."""
        
        user_prompt = f"""For the disease: {seed_disease}

Identify 3-5 candidate drugs that might have therapeutic potential. For each drug, provide:
1. The drug name
2. Its current approved indication(s)
3. A brief rationale for why it might be relevant to {seed_disease}

Format as a simple list."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=self.enable_thinking,
        )
        
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.device)
        
        # Qwen3 best practices: thinking mode uses different parameters
        if self.enable_thinking:
            temperature, top_p, top_k = 0.6, 0.95, 20
        else:
            temperature, top_p, top_k = 0.7, 0.8, 20
        
        with console.status("[bold yellow]Identifying candidate drugs...[/bold yellow]"):
            generated_ids = self.model.generate(
                **model_inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                do_sample=True,
            )
        
        generated_ids = [
            output_ids[len(input_ids):] 
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        # Parse thinking content for Qwen3 if thinking mode is enabled
        if self.enable_thinking:
            response = self._parse_thinking_content(response)
        
        return response
    
    def _parse_thinking_content(self, response: str) -> str:
        """Parse thinking content from Qwen3 output.
        
        For Qwen3, thinking content is wrapped in <think>...</think> tags.
        This method extracts only the final response content.
        
        Args:
            response: Raw response from the model
            
        Returns:
            Final response content without thinking tags
        """
        # Remove thinking content wrapped in <think>...</think>
        response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
        return response.strip()
