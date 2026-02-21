from dataclasses import dataclass

@dataclass
class EngineConfig:
    model_path: str
    context_size: int
    threads: int
    batch_size: int
    max_tokens: int
    mode: str = "accurate"
    max_ram_mb: int | None = None

