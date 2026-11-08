#!/usr/bin/env python3
"""Validate the example Sigma rules in detections/sigma.

Checks that each file parses with pySigma (including correlation rules), runs pySigma's
built-in rule validators, and confirms that every ekc.* tag names a sub-technique that
exists in data/ekc.yaml. Example rules must say so in their title and description.
"""
import pathlib
import sys

import yaml
from sigma.collection import SigmaCollection
from sigma.correlations import SigmaCorrelationRule
from sigma.rule import SigmaRule
from sigma.validators.core import validators as core_validators

ROOT = pathlib.Path(__file__).resolve().parent.parent
RULES = ROOT / "detections" / "sigma"

# Skipped pySigma checks: NamespaceTagValidator rejects the custom ekc.* namespace these rules
# exist to demonstrate; the ATT&CK/D3FEND/CAR tag validators download reference data and the
# rules carry no tags in those namespaces.
SKIP = {"NamespaceTagValidator", "ATTACKTagValidator", "D3FENDTagValidator", "CARTagValidator"}


def main() -> int:
    src = yaml.safe_load((ROOT / "data" / "ekc.yaml").read_text(encoding="utf-8"))
    ekc_ids = {t["id"][4:].lower() for s in src["stages"] for t in s["sub_techniques"]}
    validators = [v() for name, v in core_validators.items() if v.__name__ not in SKIP]

    problems: list[str] = []
    seen_ids: dict[str, str] = {}
    count = 0
    for path in sorted(RULES.glob("*.yml")):
        rel = path.relative_to(ROOT)
        try:
            coll = SigmaCollection.from_yaml(path.read_text(encoding="utf-8"), collect_errors=True)
        except Exception as e:  # noqa: BLE001
            problems.append(f"{rel}: does not parse: {e}")
            continue
        try:
            coll.resolve_rule_references()
        except Exception as e:  # noqa: BLE001
            problems.append(f"{rel}: correlation reference error: {e}")
        for item in coll.rules:
            count += 1
            for err in getattr(item, "errors", []):
                problems.append(f"{rel}: {item.title}: {err}")
            rid = str(item.id)
            if rid in seen_ids:
                problems.append(f"{rel}: duplicate rule id {rid} (also in {seen_ids[rid]})")
            seen_ids[rid] = str(rel)
            if not item.title.startswith("EKC Example"):
                problems.append(f"{rel}: title must start with 'EKC Example'")
            if "EXAMPLE RULE" not in (item.description or ""):
                problems.append(f"{rel}: description must start with 'EXAMPLE RULE.'")
            tags = [t for t in item.tags if t.namespace == "ekc"]
            if not tags:
                problems.append(f"{rel}: {item.title}: no ekc.* tag")
            for t in tags:
                if t.name.lower() not in ekc_ids:
                    problems.append(f"{rel}: tag ekc.{t.name} is not an EKC ID in data/ekc.yaml")
            if isinstance(item, SigmaRule):
                try:
                    for cond in item.detection.parsed_condition:
                        cond.parse()
                except Exception as e:  # noqa: BLE001
                    problems.append(f"{rel}: {item.title}: condition does not parse: {e}")
                for v in validators:
                    for issue in v.validate(item):
                        problems.append(f"{rel}: {item.title}: {type(issue).__name__}: {issue.description}")
            elif not isinstance(item, SigmaCorrelationRule):
                problems.append(f"{rel}: unexpected document type {type(item).__name__}")

    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    print(f"OK: {count} Sigma rules in {RULES.relative_to(ROOT)}, all ekc.* tags resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
