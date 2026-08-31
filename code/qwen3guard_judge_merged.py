"""Run Qwen3Guard-Gen over prompt/response pairs in a JSON array.

Example:
    python qwen3guard_judge_merged.py input.json output.json
"""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from typing import Any


MODEL = "Qwen/Qwen3Guard-Gen-8B"
RAW_FIELD = "qwen3guard_raw_output"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="UTF-8 JSON array with prompt/response fields")
    parser.add_argument("output", type=Path, help="output JSON path")
    parser.add_argument("--model", default=MODEL, help="Hugging Face model ID")
    parser.add_argument("--tensor-parallel-size", type=int, default=1)
    parser.add_argument("--max-model-len", type=int, default=32000)
    parser.add_argument("--gpu-memory-utilization", type=float, default=0.85)
    parser.add_argument("--max-tokens", type=int, default=10000)
    return parser


def load_records(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError("input JSON must be a top-level array")
    for index, record in enumerate(data, start=1):
        if not isinstance(record, dict):
            raise ValueError(f"record {index} must be an object")
        for field in ("prompt", "response"):
            if field not in record:
                raise ValueError(f"record {index} is missing {field}")
            if not isinstance(record[field], str):
                raise ValueError(f"record {index} field {field} must be a string")
    return data


def render_prompt(tokenizer: Any, prompt: str, response: str) -> str:
    return tokenizer.apply_chat_template(
        [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": response},
        ],
        tokenize=False,
        add_generation_prompt=True,
    )


def generate_raw_outputs(
    args: argparse.Namespace, records: list[dict[str, Any]]
) -> list[str]:
    from transformers import AutoTokenizer
    from vllm import LLM, SamplingParams

    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    llm = LLM(
        model=args.model,
        tensor_parallel_size=args.tensor_parallel_size,
        max_model_len=args.max_model_len,
        enable_prefix_caching=True,
        trust_remote_code=True,
        gpu_memory_utilization=args.gpu_memory_utilization,
    )
    sampling_params = SamplingParams(temperature=0.0, max_tokens=args.max_tokens)
    prompts = [
        render_prompt(tokenizer, record["prompt"], record["response"])
        for record in records
    ]
    return [result.outputs[0].text for result in llm.generate(prompts, sampling_params)]


def add_raw_outputs(
    records: list[dict[str, Any]], outputs: list[str]
) -> list[dict[str, Any]]:
    if len(records) != len(outputs):
        raise ValueError("number of model outputs does not match number of records")
    return [{**record, RAW_FIELD: output} for record, output in zip(records, outputs)]


def write_records(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, suffix=".tmp", delete=False
        ) as handle:
            json.dump(records, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            temporary_path = Path(handle.name)
        temporary_path.replace(path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def run(args: argparse.Namespace) -> None:
    input_path = args.input.resolve()
    output_path = args.output.resolve()
    if input_path == output_path:
        raise ValueError("input and output paths must be different")
    records = load_records(input_path)
    if not records:
        write_records(output_path, [])
        return
    outputs = generate_raw_outputs(args, records)
    write_records(output_path, add_raw_outputs(records, outputs))


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        run(args)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
