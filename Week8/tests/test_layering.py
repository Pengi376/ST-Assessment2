"""Architecture fitness tests: the dependency direction is enforced by the test-suite.

Presentation -> Services -> Domain ; Services -> Repositories(contracts) ; Persistence -> Repositories/Domain.
"""
import ast, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1] / "smartcare"
LAYERS = ["domain", "repositories", "services", "persistence", "presentation"]
# layer -> layers it is ALLOWED to import from (besides itself)
ALLOWED = {
    "domain": set(),
    "repositories": {"domain"},
    "services": {"domain", "repositories"},
    "persistence": {"domain", "repositories"},
    "presentation": {"domain", "services"},
}
STDLIB_FORBIDDEN_OUTSIDE_PERSISTENCE = {"sqlite3"}


def imports(path):
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            yield ("." * node.level) + (node.module or ""), node.level
        elif isinstance(node, ast.Import):
            for n in node.names:
                yield n.name, 0


def test_dependency_direction_is_respected():
    for layer in LAYERS:
        for f in (ROOT / layer).glob("*.py"):
            for mod, level in imports(f):
                if level >= 2:                                   # "from ..other import x"
                    target = mod.lstrip(".").split(".")[0]
                    if target in LAYERS and target != layer:
                        assert target in ALLOWED[layer], f"{f.name}: {layer} must not import {target}"


def test_only_persistence_knows_about_sqlite():
    for layer in LAYERS:
        if layer == "persistence":
            continue
        for f in (ROOT / layer).glob("*.py"):
            names = {m.split(".")[0] for m, _ in imports(f)}
            assert not (names & STDLIB_FORBIDDEN_OUTSIDE_PERSISTENCE), f"{f} imports sqlite3"


def test_domain_has_no_io():
    src = (ROOT / "domain" / "model.py").read_text()
    for banned in ("input(", "print(", "open(", "sqlite3"):
        assert banned not in src
