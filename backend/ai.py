import base64
import json
import logging
from typing import Any

from fastapi import HTTPException
from openai import APIConnectionError, APIStatusError, AsyncOpenAI

from .config import OPENAI_API_KEY, OPENAI_MODEL

logger = logging.getLogger(__name__)


def file_content(filename: str, content_type: str, data: bytes) -> dict[str, Any]:
    encoded = base64.b64encode(data).decode("ascii")
    data_url = f"data:{content_type};base64,{encoded}"
    if content_type.startswith("image/"):
        return {"type": "input_image", "image_url": data_url}
    return {"type": "input_file", "filename": filename, "file_data": data_url}


async def analyze_file(
    filename: str,
    content_type: str,
    data: bytes,
    instructions: str,
    extra_text: str = "",
) -> dict[str, Any]:
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=503, detail="Set OPENAI_API_KEY in the .env file.")
    content: list[dict[str, Any]] = [file_content(filename, content_type, data)]
    if extra_text:
        content.append({"type": "input_text", "text": extra_text})
    # json_object mode requires the word JSON in an input message (not only in instructions).
    content.append({"type": "input_text", "text": "Return the result as a valid JSON object."})
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    try:
        response = await client.responses.create(
            model=OPENAI_MODEL,
            instructions=instructions,
            input=[{"role": "user", "content": content}],
            text={"format": {"type": "json_object"}},
            store=False,
        )
    except APIStatusError as exc:
        # Log only provider diagnostics, never request headers or credentials.
        error_body = exc.body if isinstance(exc.body, dict) else {}
        error_code = error_body.get("code") or getattr(exc, "code", None)
        error_param = error_body.get("param")
        error_message = str(error_body.get("message", ""))[:500]
        logger.warning(
            "OpenAI request failed: status=%s code=%s param=%s message=%s request_id=%s",
            exc.status_code,
            error_code,
            error_param,
            error_message,
            exc.request_id,
        )
        if exc.status_code == 400:
            detail = "OpenAI rejected the request or uploaded file (HTTP 400). Check the Python backend terminal for the specific error."
        elif exc.status_code == 401:
            detail = "OpenAI rejected the API key. Check OPENAI_API_KEY in .env and restart the backend."
        elif exc.status_code == 403:
            detail = "This OpenAI key or project does not have access to the selected model."
        elif exc.status_code == 429:
            detail = "OpenAI rate limit or account quota reached. Check the API project billing and limits."
        else:
            detail = f"OpenAI returned an error (HTTP {exc.status_code}). Check the backend log for its request ID."
        raise HTTPException(status_code=502, detail=detail) from exc
    except APIConnectionError as exc:
        logger.warning("OpenAI connection failed: %s", type(exc).__name__)
        raise HTTPException(
            status_code=502,
            detail="Could not reach OpenAI. Check the server's internet connection, firewall, or proxy settings.",
        ) from exc
    except Exception as exc:
        logger.exception("Unexpected OpenAI integration error: %s", type(exc).__name__)
        raise HTTPException(status_code=502, detail="Unexpected error while processing the file with OpenAI.") from exc
    finally:
        await client.close()
    try:
        result = json.loads(response.output_text or "")
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=502, detail="The AI returned invalid JSON.") from exc
    if not isinstance(result, dict):
        raise HTTPException(status_code=502, detail="The AI response format is not usable.")
    return result


def safe_list(value: Any, limit: int = 12) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item)[:500] for item in value[:limit]]


def safe_score(value: Any) -> float:
    try:
        return max(0.0, min(100.0, float(value)))
    except (TypeError, ValueError):
        return 0.0
