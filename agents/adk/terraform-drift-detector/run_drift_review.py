import asyncio
import json
import sys

from google.adk.runners import InMemoryRunner
from google.genai import errors as genai_errors
from google.genai import types

from agent import root_agent


async def review(plan_text: str) -> dict:
    runner = InMemoryRunner(agent=root_agent, app_name="terraform_drift_detector")
    session = await runner.session_service.create_session(
        app_name="terraform_drift_detector", user_id="ci", session_id="ci-run"
    )
    final_response = None
    try:
        async for event in runner.run_async(
            user_id="ci",
            session_id=session.id,
            new_message=types.Content(role="user", parts=[types.Part.from_text(text=plan_text)]),
        ):
            if event.is_final_response():
                if event.content is None:
                    raise RuntimeError(f"Agent returned no content (event: {event})")
                final_response = event.content.parts[0].text
    except genai_errors.APIError as exc:
        print(f"Gemini API call failed: {exc}", file=sys.stderr)
        sys.exit(1)
    if final_response is not None:
        return json.loads(final_response)
    raise RuntimeError("Agent produced no final response")


if __name__ == "__main__":
    result = asyncio.run(review(sys.stdin.read()))
    print(json.dumps(result, indent=2))
