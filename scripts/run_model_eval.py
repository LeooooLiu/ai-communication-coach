#!/usr/bin/env python3
"""Run isolated first-response behavior samples against a Codex model.

This runner records model output without auto-grading semantic behavior. Review
the visible action and interaction cost against each case's expected behavior.
"""

from __future__ import annotations

import argparse
import concurrent.futures
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import tempfile
import time


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "evals" / "real-conversation-cases.json"
DEFAULT_OUTPUT = ROOT / ".local-evals" / "latest.json"

PROMPT = """Use $ai-communication-coach.

Respond to the following turn as you would in a real conversation. This is an
isolated first-response behavior run: do not mention evaluation, do not claim
that file or external actions have already happened, and do not use tools.
Produce only the natural first user-facing response you would send before or
while beginning the work. If independent work can proceed, do not block on a
choice needed only at a later stage.

User message:
{message}

Available prior context:
{context}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--model", required=True)
    parser.add_argument("--reasoning-effort", default="low")
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def load_cases(path: Path, selected_ids: list[str]) -> list[dict[str, object]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    cases = payload.get("cases", [])
    if selected_ids:
        selected = set(selected_ids)
        cases = [case for case in cases if case.get("id") in selected]
        missing = selected - {str(case.get("id")) for case in cases}
        if missing:
            raise ValueError(f"Unknown case IDs: {', '.join(sorted(missing))}")
    if not cases:
        raise ValueError("No evaluation cases selected")
    return cases


def codex_version() -> str:
    result = subprocess.run(
        ["codex", "--version"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def run_one(
    case: dict[str, object],
    repeat: int,
    model: str,
    reasoning_effort: str,
) -> dict[str, object]:
    case_id = str(case["id"])
    prompt = PROMPT.format(
        message=case["prompt"],
        context=case.get("context", "No additional context."),
    )
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix=f"aicc-{case_id}-") as temporary:
        root = Path(temporary)
        final_path = root / "final.txt"
        command = [
            "codex",
            "exec",
            "--ignore-user-config",
            "--ephemeral",
            "--skip-git-repo-check",
            "--sandbox",
            "read-only",
            "--model",
            model,
            "-c",
            f'model_reasoning_effort="{reasoning_effort}"',
            "--cd",
            str(root),
            "--output-last-message",
            str(final_path),
            "-",
        ]
        result = subprocess.run(
            command,
            input=prompt,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=300,
        )
        response = final_path.read_text(encoding="utf-8") if final_path.exists() else ""
    return {
        "case_id": case_id,
        "repeat": repeat,
        "exit_code": result.returncode,
        "elapsed_seconds": round(time.monotonic() - started, 2),
        "response": response.strip(),
        "stderr_tail": result.stderr[-2000:] if result.returncode else "",
    }


def main() -> int:
    args = parse_args()
    if args.repeats < 1 or args.workers < 1:
        raise ValueError("--repeats and --workers must be positive")
    cases = load_cases(args.cases.resolve(), args.case_id)
    jobs = [
        (case, repeat)
        for case in cases
        for repeat in range(1, args.repeats + 1)
    ]
    results: list[dict[str, object]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(
                run_one,
                case,
                repeat,
                args.model,
                args.reasoning_effort,
            ): (case["id"], repeat)
            for case, repeat in jobs
        }
        for future in concurrent.futures.as_completed(futures):
            case_id, repeat = futures[future]
            item = future.result()
            results.append(item)
            print(
                f"finished {case_id} r{repeat}: "
                f"exit={item['exit_code']} {item['elapsed_seconds']}s",
                flush=True,
            )

    results.sort(key=lambda item: (str(item["case_id"]), int(item["repeat"])))
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "codex_version": codex_version(),
        "model": args.model,
        "reasoning_effort": args.reasoning_effort,
        "cases_file": str(args.cases.resolve()),
        "case_count": len(cases),
        "repeats": args.repeats,
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    failures = [result for result in results if result["exit_code"] != 0]
    print(f"recorded {len(results)} responses in {args.output}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
