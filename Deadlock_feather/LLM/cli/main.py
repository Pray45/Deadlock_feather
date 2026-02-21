import argparse
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.engine import FeatherEngine
from core.config import EngineConfig

def main():
    parser = argparse.ArgumentParser(
        description="FeatherLLM — resource-aware local LLM"
    )

    parser.add_argument("--model", required=True, help="Path to GGUF model")
    parser.add_argument("--prompt", required=True, help="Prompt text")
    parser.add_argument("--ctx", type=int, default=1024)
    parser.add_argument("--threads", type=int, default=6)
    parser.add_argument("--max-tokens", type=int, default=256)
    parser.add_argument("--batch", type=int, default=64)
    parser.add_argument("--mode", choices=["fast", "accurate"], default="accurate")
    parser.add_argument("--max-ram", type=int, help="Max RAM in MB")


    args = parser.parse_args()

    config = EngineConfig(
        model_path=args.model,
        context_size=args.ctx,
        threads=args.threads,
        max_tokens=args.max_tokens,
        batch_size=64,
        mode=args.mode,
        max_ram_mb=args.max_ram,
    )


    engine = FeatherEngine(config)
    result = engine.run(args.prompt, max_ram_mb=args.max_ram)

    print("\n--- Response ---")
    print(result["text"])
    print("\n--- Metrics ---")
    print(f"Latency: {result['latency_sec']:.2f}s")
    print(f"RAM Used: {result['ram_mb']:.2f} MB")

if __name__ == "__main__":
    main()
