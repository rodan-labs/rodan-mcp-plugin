"""Checks, sync and ChatGPT ZIP build for the Rodan plugin repository.

Run inside Docker through the shell wrappers in scripts/. Standard library only.

    sync   copy the shared skill, icons and licence into each plugin folder
    check  validate every manifest, the listing copy limits and the writing rules
    zip    build dist/rodan-chatgpt-plugin-<version>.zip and validate the built ZIP
"""
import json
import re
import struct
import sys
import zipfile
from pathlib import Path

MCP_URL = "https://mcp.rodananalytics.com/mcp"
ZIP_DATE = (2026, 10, 31, 0, 0, 0)  # fixed, so the same input gives the same ZIP

errors: list[str] = []
warnings: list[str] = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def png_size(data: bytes):
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", data[16:24])


def luminance(hex_colour: str) -> float:
    rgb = [int(hex_colour[i : i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def frontmatter(text: str) -> dict:
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


# --------------------------------------------------------------------------- sync
def sync(repo: Path):
    skill = (repo / "shared/skills/rodan-findings/SKILL.md").read_bytes()
    licence = (repo / "LICENSE").read_bytes()
    for plugin in ("cursor", "claude", "chatgpt"):
        dest = repo / f"plugins/{plugin}/skills/rodan-findings/SKILL.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(skill)
    for plugin in ("cursor", "claude"):
        (repo / f"plugins/{plugin}/LICENSE").write_bytes(licence)
    for plugin, sizes in (("cursor", (512,)), ("claude", (512,)), ("chatgpt", (512, 256))):
        (repo / f"plugins/{plugin}/assets").mkdir(parents=True, exist_ok=True)
        for size in sizes:
            src = (repo / f"assets/rodan-icon-{size}.png").read_bytes()
            (repo / f"plugins/{plugin}/assets/rodan-icon-{size}.png").write_bytes(src)
    print("synced")


# --------------------------------------------------------------------------- shared checks
def load_json(path: Path):
    try:
        return json.loads(path.read_text())
    except Exception as exc:  # noqa: BLE001
        err(f"{path}: not valid JSON ({exc})")
        return None


def check_copies(repo: Path):
    skill = (repo / "shared/skills/rodan-findings/SKILL.md").read_bytes()
    fm = frontmatter(skill.decode())
    if not fm.get("name") or not fm.get("description"):
        err("shared skill needs name and description in its front matter")
    for plugin in ("cursor", "claude", "chatgpt"):
        p = repo / f"plugins/{plugin}/skills/rodan-findings/SKILL.md"
        if not p.exists() or p.read_bytes() != skill:
            err(f"{p} differs from shared/skills; run scripts/sync.sh")
    for plugin in ("cursor", "claude"):
        if (repo / f"plugins/{plugin}/LICENSE").read_bytes() != (repo / "LICENSE").read_bytes():
            err(f"plugins/{plugin}/LICENSE differs from LICENSE; run scripts/sync.sh")
    for plugin, sizes in (("cursor", (512,)), ("claude", (512,)), ("chatgpt", (512, 256))):
        for size in sizes:
            a = repo / f"plugins/{plugin}/assets/rodan-icon-{size}.png"
            b = repo / f"assets/rodan-icon-{size}.png"
            if not a.exists() or a.read_bytes() != b.read_bytes():
                err(f"{a} differs from assets/; run scripts/sync.sh")


def check_icons(repo: Path):
    p = repo / "assets/rodan-icon-512.png"
    size = png_size(p.read_bytes())
    if size != (512, 512):
        err(f"{p} must be 512 x 512, is {size}")
    if p.stat().st_size >= 1_000_000:
        err(f"{p} must be under 1 MB for Google")
    for f in (repo / "assets").glob("*.png"):
        s = png_size(f.read_bytes())
        if not s or s[0] != s[1]:
            err(f"{f} must be a square PNG")


def check_cursor(repo: Path):
    root = repo / "plugins/cursor"
    m = load_json(root / ".cursor-plugin/plugin.json")
    mp = load_json(repo / ".cursor-plugin/marketplace.json")
    if not m or not mp:
        return
    if not re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", m["name"]):
        err("cursor name must be lowercase kebab-case")
    entry = mp["plugins"][0]
    if entry["name"] != m["name"]:
        err("marketplace entry name must equal plugin name")
    if not (repo / entry["source"]).is_dir():
        err("marketplace source folder is missing")
    for field in ("description", "version", "author", "homepage", "repository", "license", "keywords", "logo"):
        if field not in m:
            err(f"cursor plugin.json is missing {field}")
    for field in ("logo",):
        v = m[field]
        if v.startswith("/") or ".." in v:
            err(f"cursor {field} must be a relative path with no ..")
        elif not (root / v).exists():
            err(f"cursor {field} file does not exist: {v}")
    if m["author"]["name"] != "Rodan Analytics Limited":
        err("cursor author must be Rodan Analytics Limited")
    mcp = load_json(root / "mcp.json")
    if mcp and mcp["mcpServers"]["rodan"]["url"] != MCP_URL:
        err("cursor mcp.json must point at the Rodan server")
    if len((root / "README.md").read_text().split()) < 40:
        err("plugins/cursor/README.md is too short")


def check_claude(repo: Path):
    root = repo / "plugins/claude"
    m = load_json(root / ".claude-plugin/plugin.json")
    mcp = load_json(root / ".mcp.json")
    mp = load_json(repo / ".claude-plugin/marketplace.json")
    if m:
        if not re.fullmatch(r"[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?", m["name"]):
            err("claude name must be lowercase letters, digits and hyphens, up to 64 characters")
        if m["name"] in {"claude", "anthropic", "official", "plugin", "mcp", "test"}:
            err("claude name is a reserved word")
        for field in ("description", "author", "version", "license"):
            if field not in m:
                err(f"claude plugin.json is missing {field}")
        if not m["displayName"].isascii() or not m["author"]["name"].isascii():
            err("claude displayName and author.name must be plain ASCII here")
    if mcp:
        srv = mcp["mcpServers"]["rodan"]
        if srv.get("type") != "http" or srv.get("url") != MCP_URL:
            err("claude .mcp.json must use type http and the Rodan URL")
    if mp and not (repo / mp["plugins"][0]["source"]).is_dir():
        err("claude marketplace source folder is missing")
    readme = (root / "README.md").read_text()
    words = len(re.sub(r"```.*?```", "", readme, flags=re.S).split())
    if words < 40:
        err(f"plugins/claude/README.md has {words} words outside code blocks; needs 40")
    if not (root / "LICENSE").exists():
        err("plugins/claude/LICENSE is missing")
    files = [f for f in root.rglob("*") if f.is_file()]
    if len(files) > 512:
        err("claude plugin has more than 512 files")
    for f in files:
        if f.name in {".DS_Store", "Thumbs.db", "desktop.ini"}:
            err(f"{f} is a system file")
        if f.is_symlink():
            err(f"{f} is a symlink")
        if f.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
            continue
        if f.stat().st_size >= 256 * 1024:
            err(f"{f} is over 256 KiB")
        try:
            f.read_text()
        except UnicodeDecodeError:
            err(f"{f} is not a text or image file")


# --------------------------------------------------------------------------- ChatGPT
def validate_chatgpt_files(files: dict[str, bytes], label: str):
    """files maps ZIP paths to bytes. Checks the documented ChatGPT plugin structure."""
    bad = [n for n in files if n.startswith("/") or ".." in n.split("/") or n.startswith("__MACOSX")]
    if bad:
        err(f"{label}: unsafe paths {bad}")
    for required in ("plugin.json", "mcp.json"):
        if required not in files:
            err(f"{label}: {required} must be at the ZIP root")
    if any(n.endswith(".DS_Store") for n in files):
        err(f"{label}: contains .DS_Store")
    if any(n == ".app.json" or n.startswith("hooks/") or n.endswith("/hooks.json") for n in files):
        err(f"{label}: apps and lifecycle hooks cannot be submitted")
    if "plugin.json" not in files or "mcp.json" not in files:
        return
    plugin = json.loads(files["plugin.json"])
    mcp = json.loads(files["mcp.json"])
    text = files["plugin.json"].decode()
    for banned in ("test_credentials", "reviewer_instructions", "clientSecret", '"apps"', '"hooks"'):
        if banned in text or banned in files["mcp.json"].decode():
            err(f"{label}: must not contain {banned}")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", plugin.get("name", "")) or len(plugin["name"]) > 64:
        err(f"{label}: name must be stable kebab-case, up to 64 characters")
    for field in ("version", "description", "author"):
        if field not in plugin:
            err(f"{label}: missing {field}")
    if len(plugin.get("description", "")) > 4000:
        err(f"{label}: description over 4000 characters")
    if not plugin.get("author", {}).get("name"):
        err(f"{label}: author.name is required")
    ext = plugin.get("extensions", {}).get("com.openai")
    if not ext:
        err(f"{label}: extensions.com.openai is missing")
        return
    ui = ext["interface"]
    limits = {"displayName": 30, "shortDescription": 30, "longDescription": 4000, "developerName": 80}
    for k, n in limits.items():
        if not ui.get(k):
            err(f"{label}: interface.{k} is required")
        elif len(ui[k]) > n:
            err(f"{label}: interface.{k} is {len(ui[k])} characters, limit {n}")
    for k in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        v = ui.get(k, "")
        if not v.startswith("https://") or len(v) > 1024 or "@" in v.split("/")[2]:
            err(f"{label}: interface.{k} must be an HTTPS URL up to 1024 characters with no credentials")
    for k in ("category", "capabilities"):
        if k not in ui:
            err(f"{label}: interface.{k} is missing")
    prompts = ui.get("defaultPrompt", [])
    if not 1 <= len(prompts) <= 3 or any(len(p) > 128 or "@" in p for p in prompts):
        err(f"{label}: defaultPrompt needs 1 to 3 prompts of 128 characters or fewer, with no @mentions")
    for k in ("brandColor", "brandColorDark"):
        v = ui.get(k)
        if v and not re.fullmatch(r"#[0-9A-Fa-f]{6}", v):
            err(f"{label}: {k} must be #RRGGBB")
    if ui.get("brandColor") and contrast(ui["brandColor"], "#FFFFFF") < 2:
        err(f"{label}: brandColor needs 2:1 contrast against white")
    if ui.get("brandColorDark") and contrast(ui["brandColorDark"], "#212121") < 2:
        err(f"{label}: brandColorDark needs 2:1 contrast against #212121")
    for k in ("logo", "composerIcon", "logoDark", "composerIconDark"):
        if k not in ui:
            if k in ("logo", "composerIcon"):
                err(f"{label}: interface.{k} is required")
            continue
        path = ui[k]
        if not path.startswith("./"):
            err(f"{label}: {k} must start with ./")
        name = path[2:]
        if name not in files:
            err(f"{label}: {k} points at {name}, which is not in the ZIP")
            continue
        data = files[name]
        size = png_size(data)
        if not size or size[0] != size[1] or size[0] < 48 or size[0] > 4096:
            err(f"{label}: {k} must be a square PNG from 48 to 4096 pixels, is {size}")
        if len(data) > 5 * 1024 * 1024:
            err(f"{label}: {k} is over 5 MiB")
    onboarding = ext.get("onboardingSkill")
    if onboarding:
        if onboarding.startswith("./") and onboarding[2:] in files:
            pass
        else:
            err(f"{label}: onboardingSkill points at a file that is not in the ZIP")
    skills = [n for n in files if n.startswith("skills/") and n.endswith("/SKILL.md")]
    if not skills:
        err(f"{label}: no skills/<name>/SKILL.md found")
    for n in skills:
        fm = frontmatter(files[n].decode())
        if not fm.get("name") or not fm.get("description"):
            err(f"{label}: {n} needs name and description in its front matter")
        elif fm["name"] != n.split("/")[1] and n.split("/")[1] != "rodan-findings":
            err(f"{label}: {n} name {fm['name']!r} does not match its folder")
    servers = mcp.get("mcpServers", {})
    if len(servers) != 1:
        err(f"{label}: mcp.json must hold exactly one remote server")
    for s in servers.values():
        if s.get("url") != MCP_URL:
            err(f"{label}: MCP URL must be {MCP_URL}")
        if s.get("headers"):
            err(f"{label}: public submission rejects server headers")
        auth = s.get("extensions", {}).get("com.openai", {}).get("auth", {})
        if auth.get("type") != "oauth" or auth.get("client", {}).get("mode") != "dcr":
            err(f"{label}: expected OAuth with dynamic client registration")
        if "clientId" in auth.get("client", {}) or "clientSecret" in auth.get("client", {}):
            err(f"{label}: no client credentials in the package")
    review = ext.get("review", {})
    tc = review.get("test_cases", {})
    pos, neg = tc.get("positive", []), tc.get("negative", [])
    if len(pos) != 5 or len(neg) != 3:
        err(f"{label}: needs 5 positive and 3 negative test cases, has {len(pos)} and {len(neg)}")
    for c in pos:
        for k in ("description", "prompt", "tools_triggered", "expected_behavior"):
            if not c.get(k):
                err(f"{label}: positive case {c.get('description')!r} lacks {k}")
    for c in neg:
        for k in ("description", "prompt"):
            if not c.get(k):
                err(f"{label}: negative case lacks {k}")
    if not review.get("demo_recording_url"):
        warn(f"{label}: review.demo_recording_url is not set. OpenAI requires it for MCP review. Add it after you record the video.")
    pub = ext.get("publication", {})
    for c in pub.get("countries", []):
        if not re.fullmatch(r"[A-Z]{2}", c):
            err(f"{label}: country code {c!r} must be two uppercase letters")
    if not pub.get("release_notes"):
        err(f"{label}: release_notes are missing")
    total = sum(len(v) for v in files.values())
    if total > 20 * 1024 * 1024:
        err(f"{label}: ZIP content is unexpectedly large ({total} bytes)")


def collect_chatgpt(repo: Path) -> dict[str, bytes]:
    root = repo / "plugins/chatgpt"
    out = {}
    for f in sorted(root.rglob("*")):
        if f.is_file() and f.name != ".DS_Store":
            out[f.relative_to(root).as_posix()] = f.read_bytes()
    return out


def build_zip(repo: Path):
    files = collect_chatgpt(repo)
    plugin = json.loads(files["plugin.json"])
    dist = repo / "dist"
    dist.mkdir(exist_ok=True)
    out = dist / f"rodan-chatgpt-plugin-{plugin['version']}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items():
            info = zipfile.ZipInfo(name, ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, data)
    # Validate what was actually written, not the source folder.
    with zipfile.ZipFile(out) as z:
        if z.testzip() is not None:
            err("ZIP failed its own integrity test")
        built = {n: z.read(n) for n in z.namelist() if not n.endswith("/")}
    validate_chatgpt_files(built, out.name)
    print(f"built {out.relative_to(repo)} ({out.stat().st_size} bytes, {len(built)} files)")
    for n in sorted(built):
        print(f"  {n}")


# --------------------------------------------------------------------------- listing and writing rules
FIELD = re.compile(r"\((max|under) ([\d,]+) (characters|words)\)")


def check_listing(repo: Path):
    checked = 0
    for f in sorted((repo / "listing").glob("*.md")):
        heading = None
        in_fence = False
        buf: list[str] = []
        for line in f.read_text().splitlines():
            if line.startswith("```"):
                if not in_fence:
                    in_fence, buf = True, []
                else:
                    in_fence = False
                    m = FIELD.search(heading or "")
                    if m:
                        kind, n, unit = m.group(1), int(m.group(2).replace(",", "")), m.group(3)
                        value = "\n".join(buf)
                        size = len(value) if unit == "characters" else len(value.split())
                        limit_ok = size <= n if kind == "max" else size < n
                        checked += 1
                        if not limit_ok:
                            err(f"{f.name}: '{heading.strip('# ').strip()}' is {size} {unit}, limit {kind} {n}")
                continue
            if in_fence:
                buf.append(line)
            elif line.startswith("#"):
                heading = line
    print(f"listing fields checked against their limits: {checked}")
    if checked < 16:
        err("expected at least 16 limit-checked listing fields")


def check_listing_contents(repo: Path):
    google = (repo / "listing/google.md").read_text()
    # Pull the en-GB example prompts and apply Google's rules.
    block = re.search(r"### Example prompts \(en-GB\).*?```text\n(.*?)```", google, re.S)
    if not block:
        err("google.md: en-GB example prompts block not found")
        return
    prompts = [p for p in block.group(1).splitlines() if p.strip()]
    if len(prompts) < 3:
        err("google.md: need at least 3 example prompts")
    if sum(p.startswith("@Rodan") for p in prompts) < 2:
        err("google.md: at least 2 example prompts must start with @Rodan")
    if not any("Rodan" in p and not p.startswith("@Rodan") for p in prompts):
        err("google.md: at least 1 example prompt must mention Rodan mid-sentence")
    if any(re.match(r"^\s*\d+[.)]", p) or '"' in p or "“" in p for p in prompts):
        err("google.md: example prompts must have no numbering or quotation marks")
    caps = re.search(r"### Capabilities \(en-GB\).*?```text\n(.*?)```", google, re.S)
    if not caps or len([c for c in caps.group(1).splitlines() if c.strip()]) < 3:
        err("google.md: need at least 3 capabilities")
    elif any(re.match(r"^\s*\d+[.)]", c) for c in caps.group(1).splitlines()):
        err("google.md: capabilities must not start with numbers")

    claude = (repo / "listing/claude.md").read_text()
    if len(re.findall(r"^#### Acknowledgement \d", claude, re.M)) != 7:
        err("claude.md: explain exactly seven acknowledgements")
    openai = (repo / "listing/openai.md").read_text()
    plugin = json.loads((repo / "plugins/chatgpt/plugin.json").read_text())
    review = plugin["extensions"]["com.openai"]["review"]["test_cases"]
    for c in review["positive"] + review["negative"]:
        if c["prompt"] not in openai:
            err(f"openai.md does not contain the test prompt: {c['prompt']}")
    ui = plugin["extensions"]["com.openai"]["interface"]
    for k in ("displayName", "shortDescription", "longDescription", "developerName"):
        if ui[k] not in openai:
            err(f"openai.md does not contain interface.{k} from plugin.json")


BANNED = ["revolutionary", "leverage", "utilise", "seamless", "robust", "unlock", "ai-powered", "deep dive", "—"]
# Built by concatenation so this script does not match itself.
HIDDEN = "quant" + "sole"
US_SPELLING = re.compile(r"\b(summariz\w*|organiz\w*|analyz\w*|recogniz\w*|prioritiz\w*|behavior\w*|centeriz\w*)\b", re.I)
SECRET = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY"),
    re.compile(r"Bearer\s+[A-Za-z0-9._-]{20,}"),
]


def check_writing(repo: Path):
    skip_dirs = {".git", "scripts", "dist", "source"}
    for f in sorted(repo.rglob("*")):
        if not f.is_file() or skip_dirs & set(f.relative_to(repo).parts) or f.suffix in {".png"}:
            continue
        rel = f.relative_to(repo).as_posix()
        try:
            text = f.read_text()
        except UnicodeDecodeError:
            err(f"{rel}: unexpected binary file")
            continue
        low = text.lower()
        if HIDDEN in low:
            err(f"{rel}: must not mention the later product")
        for pat in SECRET:
            if pat.search(text):
                err(f"{rel}: looks like a secret ({pat.pattern})")
        for m in re.finditer(r"(?i)(password|secret|token)\s*[:=]\s*(\S+)", text):
            if not re.match(r"^(\{\{|\[|<|`|\*|$)", m.group(2)) and len(m.group(2)) > 3 and f.suffix == ".md":
                if not re.match(r"(?i)^(the|a|and|or|in|is|are|must|only|for|never|that|of|to)\b", m.group(2)):
                    err(f"{rel}: possible credential after '{m.group(1)}': check it is a placeholder")
        if f.suffix == ".md":
            prose = re.sub(r"```.*?```", "", text, flags=re.S)
            for w in BANNED:
                if w in prose.lower():
                    err(f"{rel}: banned word or mark {w!r}")
            if re.search(r"(?<!\!)\!(?!\[)", prose):
                err(f"{rel}: exclamation mark in prose")
            if rel != "listing/google.md" and US_SPELLING.search(prose):
                err(f"{rel}: American spelling {US_SPELLING.search(prose).group(0)!r}")


def check(repo: Path):
    check_copies(repo)
    check_icons(repo)
    check_cursor(repo)
    check_claude(repo)
    files = collect_chatgpt(repo)
    validate_chatgpt_files(files, "plugins/chatgpt")
    cur = json.loads((repo / "plugins/cursor/mcp.json").read_text())["mcpServers"]
    cla = json.loads((repo / "plugins/claude/.mcp.json").read_text())["mcpServers"]
    gpt = json.loads((repo / "plugins/chatgpt/mcp.json").read_text())["mcpServers"]
    urls = {next(iter(s.values()))["url"] for s in (cur, cla, gpt)}
    if urls != {MCP_URL}:
        err(f"all plugins must use one server URL, found {urls}")
    for f in (repo / "LICENSE",):
        t = f.read_text()
        if "Copyright (c) 2026 Rodan Analytics Limited" not in t or not t.startswith("MIT License"):
            err("LICENSE must be MIT, copyright Rodan Analytics Limited")
    check_listing(repo)
    check_listing_contents(repo)
    check_writing(repo)


def main():
    cmd, repo = sys.argv[1], Path(sys.argv[2])
    if cmd == "sync":
        sync(repo)
        return
    if cmd == "check":
        check(repo)
    elif cmd == "zip":
        build_zip(repo)
    else:
        sys.exit(f"unknown command {cmd}")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"FAIL  {e}")
    print(f"{len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
