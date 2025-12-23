"""Test script to verify the Clinical Supervisor Agent runs on CPU."""

import argparse
import sys

from rich.console import Console
from rich.panel import Panel

from trialagent.agents.clinical_supervisor import ClinicalSupervisorAgent

console = Console()


def main() -> int:
    """Test the Clinical Supervisor Agent."""
    parser = argparse.ArgumentParser(
        description="Test the Clinical Supervisor Agent with Qwen on CPU"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="Qwen/Qwen3-8B",
        help="HuggingFace model identifier (default: Qwen/Qwen3-8B)",
    )
    parser.add_argument(
        "--disease",
        type=str,
        default="Alzheimer's disease",
        help="Seed disease to test with (default: Alzheimer's disease)",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        help="Device to run inference on (default: cpu)",
    )
    parser.add_argument(
        "--enable-thinking",
        action="store_true",
        help="Enable thinking mode for Qwen3 (default: False for efficiency)",
    )
    
    args = parser.parse_args()
    
    try:
        console.print(Panel.fit(
            "[bold blue]TrialAgent: Clinical Supervisor Agent Test[/bold blue]\n"
            f"Model: {args.model}\n"
            f"Device: {args.device}\n"
            f"Thinking Mode: {args.enable_thinking}\n"
            f"Seed Disease: {args.disease}",
            border_style="blue"
        ))
        
        # Initialize agent
        console.print("\n[bold]Initializing Clinical Supervisor Agent...[/bold]")
        agent = ClinicalSupervisorAgent(
            model_name=args.model,
            device=args.device,
            enable_thinking=args.enable_thinking,
        )
        
        # Test 1: Generate hypothesis
        console.print("\n[bold cyan]Test 1: Generating hypothesis[/bold cyan]")
        hypothesis = agent.generate_hypothesis(
            seed_disease=args.disease,
            max_new_tokens=256,
        )
        console.print(Panel(
            hypothesis,
            title="[bold green]Generated Hypothesis[/bold green]",
            border_style="green"
        ))
        
        # Test 2: Identify candidate drugs
        console.print("\n[bold cyan]Test 2: Identifying candidate drugs[/bold cyan]")
        candidates = agent.identify_candidate_drugs(
            seed_disease=args.disease,
            max_new_tokens=256,
        )
        console.print(Panel(
            candidates,
            title="[bold green]Candidate Drugs[/bold green]",
            border_style="green"
        ))
        
        console.print("\n[bold green]✓ All tests passed! Qwen is running successfully on CPU.[/bold green]")
        return 0
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        return 1
    except Exception as e:
        console.print(f"\n[bold red]Error: {e}[/bold red]", file=sys.stderr)
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        return 1


if __name__ == "__main__":
    sys.exit(main())
