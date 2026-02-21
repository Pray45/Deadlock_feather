from llama_cpp import Llama
from core.metrics import Metrics
from core.config import EngineConfig
import os

def file_size_mb(path):
    return os.path.getsize(path) / (1024 ** 2)


class FeatherEngine:
    
    def __init__(self, config: EngineConfig):
        
        model_size_mb = file_size_mb(config.model_path)

        print(f"[FeatherLLM] Model size on disk: {model_size_mb:.2f} MB")
        
        if hasattr(config, "max_ram_mb") and config.max_ram_mb:
            if model_size_mb > config.max_ram_mb * 0.9:
                raise RuntimeError(
                    f"Model too large for RAM limit. "
                    f"Model ~{model_size_mb:.0f} MB, "
                    f"limit {config.max_ram_mb:.0f} MB"
                )

        
        self.metrics = Metrics()
        self.config = config

        if config.mode == "fast":
            ctx = min(config.context_size, 512)
            batch = 32
        else:
            ctx = config.context_size
            batch = config.batch_size

        print(f"[FeatherLLM] Mode: {config.mode}")
        print(f"[FeatherLLM] RAM before load: {self.metrics.ram_mb():.2f} MB")

        self.llm = Llama(
            model_path=config.model_path,
            n_ctx=ctx,
            n_threads=config.threads,
            n_batch=batch,
            use_mlock=False,
            verbose=False,
        )

        print(f"[FeatherLLM] RAM after load: {self.metrics.ram_mb():.2f} MB")

    def run(self, prompt: str, max_ram_mb: float | None = None):
        try:
            return self._run_internal(prompt, max_ram_mb)
        except MemoryError:
            print("[FeatherLLM] Memory pressure detected. Degrading...")
            self.config.context_size = min(self.config.context_size, 512)
            self.config.max_tokens = min(self.config.max_tokens, 128)
            return self._run_internal(prompt, max_ram_mb)

    def _run_internal(self, prompt, max_ram_mb):
        if max_ram_mb:
            self.metrics.enforce_limit(max_ram_mb)

        def _infer():
            return self.llm(
                prompt,
                max_tokens=self.config.max_tokens,
                stop=["</s>"],
            )

        output, duration = self.metrics.timed(_infer)

        return {
            "text": output["choices"][0]["text"].strip(),
            "latency_sec": duration,
            "ram_mb": self.metrics.ram_mb(),
        }
