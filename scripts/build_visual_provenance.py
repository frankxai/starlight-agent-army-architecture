#!/usr/bin/env python3
"""Compile deterministic visual lineage evidence for the canonical portfolio."""

from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "portfolio" / "canonical-portfolio.v1.json"
SOURCE_MAP_PATH = ROOT / "portfolio" / "visual-source-map.v1.json"
ASSET_ROOT = ROOT / "assets" / "starlight-constellation" / "v1"
OUTPUT_PATH = ASSET_ROOT / "visual-provenance.manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def webp_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) < 30 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        raise ValueError(f"Not a WebP file: {path}")
    chunk = data[12:16]
    if chunk == b"VP8X":
        width = 1 + int.from_bytes(data[24:27], "little")
        height = 1 + int.from_bytes(data[27:30], "little")
        return width, height
    if chunk == b"VP8 ":
        marker = data.find(b"\x9d\x01\x2a", 20, 40)
        if marker < 0:
            raise ValueError(f"VP8 frame marker missing: {path}")
        width, height = struct.unpack_from("<HH", data, marker + 3)
        return width & 0x3FFF, height & 0x3FFF
    if chunk == b"VP8L":
        b0, b1, b2, b3 = data[21:25]
        width = 1 + (((b2 & 0x3F) << 8) | b1)
        height = 1 + (((b3 & 0xF) << 10) | (b2 >> 6) | (b3 & 0xF0) << 2 | b0 >> 6)
        return width, height
    raise ValueError(f"Unsupported WebP encoding {chunk!r}: {path}")


def canonical_json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")


def main() -> None:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    source_map = json.loads(SOURCE_MAP_PATH.read_text(encoding="utf-8"))
    agents: dict[str, tuple[dict, dict]] = {}
    for swarm in catalog["swarms"]:
        for agent in swarm["agents"]:
            if agent["id"] in agents:
                raise ValueError(f"Duplicate agent id: {agent['id']}")
            agents[agent["id"]] = (swarm, agent)

    source_ids = set(source_map["sources"])
    agent_ids = set(agents)
    if source_ids != agent_ids:
        missing = sorted(agent_ids - source_ids)
        extra = sorted(source_ids - agent_ids)
        raise ValueError(f"Visual source drift; missing={missing}, extra={extra}")

    entries = []
    for agent_id in sorted(agent_ids):
        swarm, agent = agents[agent_id]
        source = source_map["sources"][agent_id]
        asset_rel = Path("agents") / swarm["id"] / f"{agent_id}.webp"
        asset_path = ASSET_ROOT / asset_rel
        if not asset_path.is_file():
            raise FileNotFoundError(asset_path)
        width, height = webp_dimensions(asset_path)
        entry = {
            "agent_id": agent_id,
            "asset_id": f"{agent_id}-v1",
            "asset_path": asset_rel.as_posix(),
            "bytes": asset_path.stat().st_size,
            "display_name": agent["display_name"],
            "height": height,
            "inspection_status": source_map["inspection"]["status"],
            "prompt_spec": {
                "archetype": agent["visual_dna"]["archetype"],
                "portrait_brief": agent["visual_dna"]["portrait_brief"],
                "signature": agent["visual_dna"]["signature"],
                "silhouette": agent["visual_dna"]["silhouette"],
                "swarm_visual_world": swarm["visual_world"],
            },
            "rights_status": source_map["rights"]["status"],
            "sha256": sha256(asset_path),
            "source_file": source["source_file"],
            "swarm_id": swarm["id"],
            "width": width,
        }
        if "notes" in source:
            entry["notes"] = source["notes"]
        entries.append(entry)

    output = {
        "schema_version": "starlight.visual_provenance_manifest.v1",
        "portfolio_id": source_map["portfolio_id"],
        "portfolio_source_sha256": sha256(CATALOG_PATH),
        "collection_id": source_map["collection_id"],
        "generated_on": source_map["generated_on"],
        "generation": {
            "provider": source_map["provider"],
            "session_id": source_map["generation_session_id"],
            "tool_surface": source_map["tool_surface"],
            "prompt_contract": source_map["prompt_contract"],
        },
        "rights": source_map["rights"],
        "inspection": source_map["inspection"],
        "counts": {"agents": len(entries), "assets": len(entries)},
        "assets": entries,
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_bytes(canonical_json_bytes(output))
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT).as_posix()} with {len(entries)} assets")


if __name__ == "__main__":
    main()
