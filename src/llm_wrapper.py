# src/llm_wrapper.py
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

genai.configure(api_key=api_key)

DEFAULT_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.0"))
DEFAULT_MAX_OUTPUT = int(os.getenv("LLM_MAX_OUTPUT", "1024"))
DEFAULT_CANDIDATES = int(os.getenv("LLM_CANDIDATES", "1"))

LOG_DIR = Path(os.getenv("LLM_LOG_DIR", "logs"))
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "llm_calls.log"
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)


def gemini_llm(prompt: str,
               temperature: float | None = None,
               max_output_tokens: int | None = None,
               candidate_count: int | None = None,
               model_name: str = 'gemini-2.0-flash') -> str:
    """
    Call Gemini with deterministic defaults. Logs prompt and response to `logs/llm_calls.log`.

    Parameters are optional and will default to deterministic values unless overridden by env vars.
    """
    temperature = DEFAULT_TEMPERATURE if temperature is None else temperature
    max_output_tokens = DEFAULT_MAX_OUTPUT if max_output_tokens is None else max_output_tokens
    candidate_count = DEFAULT_CANDIDATES if candidate_count is None else candidate_count

    model = genai.GenerativeModel(model_name)

    kwargs = {
        "temperature": float(temperature),
        "max_output_tokens": int(max_output_tokens),
        "candidate_count": int(candidate_count)
    }

    try:
        response = model.generate_content(prompt, **kwargs)
    except TypeError:
        response = model.generate_content(prompt)

    text = None
    if hasattr(response, 'text'):
        text = response.text
    else:
        try:
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                text = getattr(candidate, 'content', None) or getattr(candidate, 'output', None) or str(candidate)
            else:
                text = str(response)
        except Exception:
            text = str(response)

    try:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "model": model_name,
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
            "candidate_count": candidate_count,
            "prompt_snippet": prompt[:200].replace('\n', ' '),
            "response_snippet": (text or '')[:500].replace('\n', ' ')
        }
        logging.info(log_entry)
    except Exception:
        pass

    return text or ""


def set_deterministic_mode(enabled: bool = True):
    """Set deterministic defaults at runtime.

    When enabled=True, temperature is set to 0.0 and candidate_count=1.
    When enabled=False, defaults fall back to environment variables.
    """
    global DEFAULT_TEMPERATURE, DEFAULT_CANDIDATES
    if enabled:
        DEFAULT_TEMPERATURE = 0.0
        DEFAULT_CANDIDATES = 1
    else:
        DEFAULT_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        DEFAULT_CANDIDATES = int(os.getenv("LLM_CANDIDATES", "1"))
