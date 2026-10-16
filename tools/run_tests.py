#!/usr/bin/env python3
"""Run the question tests: Python with pytest, SystemVerilog with Verilator.

    python tools/run_tests.py                 # everything
    python tools/run_tests.py 6 7             # only questions 0006 and 0007
    python tools/run_tests.py --python-only   # skip SystemVerilog
    python tools/run_tests.py --sv-only

SystemVerilog needs Verilator 5.053 or newer (today: a development snapshot built from a
pinned commit, see README.md "Tests" and the CI workflow) with the z3 solver on the PATH,
so that randomize() with constraints runs as published.

SystemVerilog testbenches (tests/<id>/tb.sv) use these directives:

    //@page <marker>                  replaced by the page's SV block that contains <marker>
    //@translation-of <marker> <hash> the testbench holds a hand translation of that block
                                      (for a proven simulator bug; none today); fails when the page changes
    //@flags <verilator flags>        extra flags, e.g. --timing

A testbench passes when it prints a line starting with PASS. Compiled simulators are
cached in .cache/sv/ by the hash of the expanded testbench, so only changed
testbenches are recompiled.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract_code  # noqa: E402

ROOT = extract_code.ROOT
TESTS = ROOT / "tests"
CACHE = ROOT / ".cache" / "sv"
MIN_VERILATOR = (5, 53)       # 5.052 crashes on 0011 and mis-randomizes the 0014 subclass
SIM_TIMEOUT = 300             # seconds; the solver takes ~0.1 s per randomize() on 0014

PAGE = re.compile(r"^(?P<indent>[ \t]*)//@page[ \t]+(?P<marker>.+?)[ \t]*$", re.M)
TRANSLATION = re.compile(r"^//@translation-of[ \t]+(?P<marker>.+?)[ \t]+(?P<hash>[0-9a-f]{12})[ \t]*$", re.M)
FLAGS = re.compile(r"^//@flags[ \t]+(?P<flags>.+)$", re.M)


def selected_dirs(ids: list[str]) -> list[Path]:
    dirs = sorted(d for d in TESTS.iterdir() if d.is_dir() and d.name[:4].isdigit())
    if ids:
        wanted = {f"{int(i):04d}" for i in ids}
        dirs = [d for d in dirs if d.name[:4] in wanted]
    return dirs


def run_python(dirs: list[Path]) -> bool:
    files = [str(f) for d in dirs for f in sorted(d.glob("test_*.py"))]
    if not files:
        return True
    print(f"== Python: {len(files)} file(s)")
    cmd = [sys.executable, "-m", "pytest", "-q", "--import-mode=importlib", "-p", "no:cacheprovider", *files]
    return subprocess.call(cmd, cwd=ROOT) == 0


def expand(tb: Path) -> tuple[str, list[str]]:
    """Return the testbench with page blocks inlined, plus a list of problems."""
    qid = tb.parent.name[:4]
    text = tb.read_text(encoding="utf-8")
    problems = []

    for m in TRANSLATION.finditer(text):
        current = extract_code.fingerprint(extract_code.pick(qid, "systemverilog", m["marker"]))
        if current != m["hash"]:
            problems.append(f"the page code containing {m['marker']!r} changed "
                            f"(hash {current}, testbench expects {m['hash']}); update the translation")

    def inline(m: re.Match) -> str:
        code = extract_code.pick(qid, "systemverilog", m["marker"])
        return "".join(m["indent"] + line if line.strip() else line
                       for line in code.splitlines(keepends=True)).rstrip("\n")

    return PAGE.sub(inline, text), problems


def run_sv(tb: Path, verilator: str, version: str) -> tuple[str, bool, str]:
    name = tb.parent.name
    start = time.time()
    try:
        source, problems = expand(tb)
    except LookupError as e:
        return name, False, str(e)
    if problems:
        return name, False, "; ".join(problems)

    flags = " ".join(m["flags"] for m in FLAGS.finditer(source)).split()
    key = hashlib.sha256((version + " ".join(flags) + source).encode()).hexdigest()[:16]
    work = CACHE / f"{name}-{key}"
    sim = work / "obj_dir" / "sim"
    cached = sim.exists()

    if not cached:
        shutil.rmtree(work, ignore_errors=True)
        work.mkdir(parents=True)
        (work / "tb.sv").write_text(source, encoding="utf-8")
        cmd = [verilator, "--binary", "-Wno-fatal", "-Wno-lint", "-Wno-style", "--top-module", "tb",
               "-j", "2", "-CFLAGS", "-O0", "-o", "sim", *flags, "tb.sv"]
        build = subprocess.run(cmd, cwd=work, capture_output=True, text=True)
        if build.returncode != 0:
            errors = [l for l in (build.stdout + build.stderr).splitlines() if "%Error" in l]
            return name, False, "compile failed: " + " | ".join(errors[:5])

    try:
        result = subprocess.run([str(sim)], cwd=work, capture_output=True, text=True, timeout=SIM_TIMEOUT)
    except subprocess.TimeoutExpired:
        return name, False, "simulation timed out"
    passed = result.returncode == 0 and any(l.startswith("PASS") for l in result.stdout.splitlines())
    summary = next((l for l in result.stdout.splitlines() if l.startswith(("PASS", "FAIL"))), "no PASS line")
    note = "cached" if cached else "compiled"
    return name, passed, f"{summary} ({note}, {time.time() - start:.1f}s)"


def run_all_sv(dirs: list[Path]) -> bool:
    tbs = [d / "tb.sv" for d in dirs if (d / "tb.sv").exists()]
    if not tbs:
        return True
    verilator = shutil.which("verilator")
    if not verilator:
        print("!! verilator not found: install it (e.g. apt install verilator) or use --python-only")
        return False
    version = subprocess.run([verilator, "--version"], capture_output=True, text=True).stdout.strip()
    found = re.search(r"Verilator (\d+)\.(\d+)", version)
    if not found or (int(found[1]), int(found[2])) < MIN_VERILATOR:
        print(f"!! {version or 'unknown Verilator'}: the testbenches need Verilator "
              f"{MIN_VERILATOR[0]}.{MIN_VERILATOR[1]:03d}+ with z3 (see README.md, Tests), or use --python-only")
        return False
    if not shutil.which("z3"):
        print("!! z3 not found: randomize() with constraints needs the z3 solver (apt install z3)")
        return False
    print(f"== SystemVerilog: {len(tbs)} testbench(es), {version}")
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda tb: run_sv(tb, verilator, version), tbs))
    for name, passed, detail in results:
        print(f"  {'ok  ' if passed else 'FAIL'} {name}: {detail}")
    return all(passed for _, passed, _ in results)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("ids", nargs="*", help="question ids to test (default: all)")
    parser.add_argument("--python-only", action="store_true")
    parser.add_argument("--sv-only", action="store_true")
    args = parser.parse_args()

    dirs = selected_dirs(args.ids)
    ok = True
    if not args.sv_only:
        ok &= run_python(dirs)
    if not args.python_only:
        ok &= run_all_sv(dirs)
    print("\nALL TESTS PASSED" if ok else "\nSOME TESTS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
