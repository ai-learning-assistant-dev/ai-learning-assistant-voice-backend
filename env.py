import os
from typing import Any, Callable

# The begin-* and end* here are used by the documentation generator
# to extract the used env vars.

# --8<-- [start:env-vars-definition]
environment_variables: dict[str, Callable[[], Any]] = {

    # ================== Installation Time Env Vars ==================

    # Sample rate of the audio files.
    "AUDIO_SAMPLE_RATE": lambda: os.getenv("AUDIO_SAMPLE_RATE", 24000),
    
    # ================== Runtime Env Vars ==================
    # The default model to use.
    "DEFAULT_MODEL": lambda: os.getenv("DEFAULT_MODEL", "kokoro"),
    
    # Whether to use GPU for inference.
    "USE_GPU": lambda: os.getenv("USE_GPU", "false").lower() in ("true", "1", "yes")
}

# --8<-- [end:env-vars-definition]


def __getattr__(name: str):
    # lazy evaluation of environment variables
    if name in environment_variables:
        return environment_variables[name]()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return list(environment_variables.keys())