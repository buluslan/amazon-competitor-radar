#!/usr/bin/env python3
"""Validate a skill's release metadata and document references (no API calls)."""

import ast
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]


def check(condition, message):
    if not condition:
        raise ValueError(message)


def validate(root):
    manifest = yaml.safe_load((root / "release.yml").read_text(encoding="utf-8"))
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", skill, re.S)
    check(match is not None, "SKILL.md must start with YAML frontmatter")
    frontmatter = yaml.safe_load(match.group(1))
    check(isinstance(manifest, dict), "release.yml must be a mapping")
    check(isinstance(frontmatter, dict), "SKILL.md frontmatter must be a mapping")
    name = manifest.get("name")
    version = manifest.get("version")
    check(isinstance(name, str) and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name),
          "Skill name must use kebab-case")
    check(len(name) <= 64, "Skill name exceeds 64 characters")
    check(frontmatter.get("name") == name, "Skill name differs from manifest")
    description = frontmatter.get("description")
    check(isinstance(description, str) and 0 < len(description.strip()) <= 1024,
          "Description must contain 1-1024 characters")
    check("<" not in description and ">" not in description, "Description contains angle brackets")
    check(isinstance(version, str) and re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", version),
          "Version must use SemVer")
    check(frontmatter.get("metadata", {}).get("version") == version,
          "SKILL.md version differs from manifest")
    check(frontmatter.get("license") == "MIT", "Expected MIT license metadata")
    check(manifest.get("developer") == manifest.get("github_owner") == "buluslan",
          "Unexpected developer or repository owner")
    check(manifest.get("brand") == "新西楼.AI", "Unexpected brand")
    check(manifest.get("visibility") in {"private", "public"}, "Visibility must be private or public")
    check(manifest.get("publish_tencent") is False and manifest.get("publish_xhs") is False,
          "This release targets GitHub only")
    readme = (root / "README.md").read_text(encoding="utf-8")
    check("version-%s-black.svg" % version in readme, "README version differs from manifest")
    check("## %s" % version in (root / "CHANGELOG.md").read_text(encoding="utf-8"),
          "Changelog lacks release version")
    intro = readme.split("## 项目简介\n", 1)[1].lstrip().split("\n\n", 1)[0]
    check(intro.startswith(manifest["display_name"]) and "buluslan（公众号：新西楼.AI）" in intro,
          "README introduction lacks project attribution")
    check("Created By Buluu@新西楼.AI" in readme, "README lacks author attribution")
    check(all(agent in readme for agent in ("Claude Code", "Codex", "Cursor")),
          "README lacks multi-agent usage guidance")
    check("MIT License" in (root / "LICENSE").read_text(encoding="utf-8"), "MIT license missing")
    evals = json.loads((root / "evals/evals.json").read_text(encoding="utf-8"))
    check(evals.get("skill_name") == name, "Eval skill name differs from manifest")
    cases = evals.get("evals", [])
    check(len(cases) == 4, "Expected four existing behavior-evaluation cases")
    check(len({case["id"] for case in cases}) == len(cases), "Duplicate eval identifiers")
    for case in cases:
        check(bool(case.get("prompt")) and bool(case.get("expected_output")), "Incomplete eval case")
        for filename in case.get("files", []):
            check((root / filename).is_file(), "Missing eval input: %s" % filename)
    private_dirs = {"reports", "report", "outputs", "output", "logs", "cache", ".flow_state"}
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if ".git" in relative.parts or ".venv" in relative.parts:
            continue
        check(not path.is_symlink(), "Unexpected symlink: %s" % relative)
        if not path.is_file():
            continue
        check(not (private_dirs & set(relative.parts[:-1])), "Runtime artifact: %s" % relative)
        check(path.name not in {".env", ".mcp.json"} and not path.name.startswith(".env."),
              "Private configuration: %s" % relative)
        if path.suffix == ".py":
            ast.parse(path.read_text(encoding="utf-8"), filename=str(relative))
        elif path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
        elif path.suffix in {".yml", ".yaml"}:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        elif path.suffix == ".md":
            text = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.S)
            for target in re.findall(r"!?\[[^\]]*\]\(([^)\s]*)\)", text):
                parts = urlsplit(target)
                if not target or parts.scheme or parts.netloc or target.startswith("#"):
                    continue
                check((path.parent / unquote(parts.path)).is_file(),
                      "Broken document link in %s: %s" % (relative, target))
    for target in set(re.findall(r"references/[A-Za-z0-9_.-]+\.md", skill)):
        check((root / target).is_file(), "Missing skill reference: %s" % target)
    for path in (root / "references").glob("*.md"):
        for target in set(re.findall(r"(?<![\w/-])([a-z][a-z0-9-]*\.md)\b",
                                     path.read_text(encoding="utf-8"))):
            check((path.parent / target).is_file() or (root / target).is_file(),
                  "Missing reference: %s" % target)
    if (root / ".git").exists():
        subprocess.run(["git", "-C", str(root), "diff", "--check"], check=True)
        subprocess.run(["git", "-C", str(root), "diff", "--cached", "--check"], check=True)
    print("PASS: metadata, versions, 4 eval definitions, JSON/YAML, syntax, references, release hygiene")
    print("NOTE: agent behavior and live marketplace data are not executed by this validator")


if __name__ == "__main__":
    try:
        validate(ROOT)
    except (ValueError, KeyError, IndexError, TypeError, OSError, yaml.YAMLError,
            subprocess.CalledProcessError) as error:
        print("FAIL: %s" % error, file=sys.stderr)
        sys.exit(1)
