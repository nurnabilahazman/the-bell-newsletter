import json
from pathlib import Path

LIBRARY_PATH  = Path("config/diagram_library.json")
ROTATION_PATH = Path("config/diagram_rotation.json")


def _load_library():
    return json.loads(LIBRARY_PATH.read_text())


def _load_rotation():
    if ROTATION_PATH.exists():
        return json.loads(ROTATION_PATH.read_text())
    return {}


def _save_rotation(rotation):
    ROTATION_PATH.write_text(json.dumps(rotation, indent=2))


def detect_bucket(text: str, library: dict) -> str:
    text_lower = text.lower()
    for bucket, cfg in library.items():
        for kw in cfg["keywords"]:
            if kw in text_lower:
                return bucket
    return "RESULTS"


def _next_variant(bucket: str, library: dict, rotation: dict) -> str:
    variants = library[bucket]["variants"]
    idx = rotation.get(bucket, 0)
    variant = variants[idx % len(variants)]
    rotation[bucket] = (idx + 1) % len(variants)
    return variant


def _fallback_bucket(library: dict, used: set) -> str:
    fallback_order = ["RESULTS", "PROCESS", "DATA", "AUTOMATION", "GROWTH",
                      "BEFORE_AFTER", "TOOLS", "VOLUME", "TIME", "CONTRAST",
                      "FAILURE", "BEGINNER"]
    for b in fallback_order:
        if b not in used:
            return b
    return "RESULTS"


def assign_diagrams(slides: list) -> list:
    """
    Given a list of slide dicts (each with a 'text' key),
    returns a list of SVG strings — one per slide — with no bucket
    repeated within the same carousel.
    """
    library = _load_library()
    rotation = _load_rotation()
    used_buckets: set = set()
    svgs = []

    for slide in slides:
        text = slide.get("text") or slide.get("title", "")
        bucket = detect_bucket(text, library)
        if bucket in used_buckets:
            bucket = _fallback_bucket(library, used_buckets)
        used_buckets.add(bucket)
        variant = _next_variant(bucket, library, rotation)
        svg = _render_variant(variant)
        svgs.append(svg)

    _save_rotation(rotation)
    return svgs


def _render_variant(variant: str) -> str:
    module_path = Path("tools/diagrams") / f"{variant}.py"
    if not module_path.exists():
        return _fallback_svg(variant)
    namespace: dict = {}
    exec(module_path.read_text(), namespace)
    return namespace["render"]()


def _fallback_svg(variant: str) -> str:
    label = variant.replace("_", " ").upper()
    return f"""<svg width="820" height="460" viewBox="0 0 820 460" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;">
  <rect x="50" y="80" width="720" height="300" rx="12" fill="#1A1A2E"/>
  <text x="410" y="245" font-size="28" fill="#C9A84C" text-anchor="middle" font-weight="700">{label}</text>
</svg>"""
