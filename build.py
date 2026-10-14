#!/usr/bin/env python3
"""Build the word family lessons.

Each family below becomes <family>.html from lesson.template.html.
index.html becomes the menu, and sw.js gets the new file list and a new
cache version so the iPad picks up the change.

Usage: python3 build.py
"""
import json, re, hashlib, pathlib

ROOT = pathlib.Path(__file__).parent

# w: the word, on: the first sound(s), e: the picture (shown after she reads)
# nogame: words left out of the picture game (names, or pictures that don't say the word clearly)
# story: [line with <b>family words</b>, plain text to read aloud, picture]
FAMILIES = [
    {
        "f": "am", "stretch": "aaaa-mmm", "blend": "j… am… jam!",
        "booklets": "“Pam and Sam”, then “Shhh!”",
        "story_title": "Sam the Ram",
        "sample": ["jam", "ham, jam, ram"],
        "words": [
            ("h","ham","🍖"),("j","jam","🫙🍓"),("r","ram","🐏"),("y","yam","🍠"),
            ("S","Sam","👦"),("P","Pam","👧"),("cl","clam","🐚"),("sw","swam","🏊"),
            ("tr","tram","🚋"),("wh","wham","💥"),
        ],
        "nogame": ["Sam","Pam"],
        "story": [
            ["I am <b>Sam</b>.","I am Sam.","🐏"],
            ["I am a <b>ram</b>!","I am a ram!","🐏"],
            ["I like <b>ham</b>.","I like ham.","🍖"],
            ["I like <b>jam</b>.","I like jam.","🫙🍓"],
            ["I like a <b>yam</b>.","I like a yam.","🍠"],
            ["Here is <b>Pam</b>.","Here is Pam.","👧"],
            ["<b>Pam</b> is in a <b>tram</b>.","Pam is in a tram.","🚋"],
            ["<b>Pam</b> has a <b>clam</b>.","Pam has a clam.","🐚"],
            ["The <b>clam</b> is for <b>Sam</b>!","The clam is for Sam!","🐚🐏"],
            ["<b>Sam</b> <b>swam</b> to <b>Pam</b>.","Sam swam to Pam.","🏊"],
            ["<b>Wham</b>! <b>Slam</b>!","Wham! Slam!","💥"],
            ["The <b>tram</b> ran!","The tram ran!","🚋"],
            ["<b>Sam</b> and <b>Pam</b> had <b>jam</b>.","Sam and Pam had jam.","🫙🍓"],
            ["I am a glad <b>ram</b>!","I am a glad ram!","🐏"],
        ],
    },
    {
        "f": "ap", "stretch": "aaaa… p", "blend": "c… ap… cap!",
        "booklets": "“Hap Can See”, then “I Like to Dance!”",
        "story_title": "Hap the Pup",
        "sample": ["cap", "cap, map, nap"],
        "words": [
            ("c","cap","🧢"),("m","map","🗺️"),("n","nap","😴"),("t","tap","🚰"),
            ("z","zap","⚡"),("y","yap","🐶"),("cl","clap","👏"),("tr","trap","🪤"),
            ("sn","snap","🐊"),("H","Hap","🐶"),
        ],
        "nogame": ["Hap","yap","snap"],
        "story": [
            ["Here is <b>Hap</b>.","Here is Hap.","🐶"],
            ["<b>Hap</b> is a pup.","Hap is a pup.","🐶"],
            ["<b>Hap</b> has a red <b>cap</b>.","Hap has a red cap.","🧢"],
            ["<b>Hap</b> has a <b>map</b>.","Hap has a map.","🗺️"],
            ["<b>Hap</b> can <b>tap</b>, <b>tap</b>, <b>tap</b>.","Hap can tap, tap, tap.","🐾"],
            ["<b>Hap</b> can <b>clap</b>, <b>clap</b>, <b>clap</b>!","Hap can clap, clap, clap!","👏"],
            ["Look! A <b>trap</b>!","Look! A trap!","🪤"],
            ["<b>Snap</b>! went the <b>trap</b>.","Snap! went the trap.","🪤"],
            ["<b>Hap</b> did not get in the <b>trap</b>.","Hap did not get in the trap.","🐶"],
            ["<b>Zap</b>! <b>Zap</b>! <b>Hap</b> ran!","Zap! Zap! Hap ran!","⚡"],
            ["<b>Hap</b> ran to his mat.","Hap ran to his mat.","🐶"],
            ["<b>Hap</b> had a <b>nap</b>.","Hap had a nap.","😴"],
            ["<b>Yap</b>! <b>Yap</b>! <b>Hap</b> is glad.","Yap! Yap! Hap is glad.","🐶"],
        ],
    },
]

def js(v):
    return json.dumps(v, ensure_ascii=False)

tpl = (ROOT / "lesson.template.html").read_text()
pages = []
for fam in FAMILIES:
    f = fam["f"]
    words = [{"on": on, "w": w, "e": e} for on, w, e in fam["words"]]
    for _, w, _ in fam["words"]:
        assert w.lower().endswith(f), w
    out = tpl
    for k, v in {
        "{{CAP}}": f.capitalize(), "{{F}}": f, "{{L1}}": f[0], "{{L2}}": f[1:],
        "{{STRETCH}}": fam["stretch"], "{{BLEND}}": fam["blend"], "{{BOOKLETS}}": fam["booklets"],
        "{{STORYTITLE}}": fam["story_title"], "{{WORDS}}": js(words), "{{NOGAME}}": js(fam["nogame"]),
        "{{STORY}}": js(fam["story"]), "{{FQ}}": js(f),
        "{{SAMPLE1}}": js(fam["sample"][0]), "{{SAMPLE3}}": js(fam["sample"][1]),
    }.items():
        out = out.replace(k, v)
    assert "{{" not in out, f
    (ROOT / f"{f}.html").write_text(out)
    pages.append(fam)

# Menu page: reuse the template's head and styles
head = tpl[: tpl.index('<div class="wrap">')]
head = head.replace("<title>The {{CAP}} Family</title>", "<title>Word Families</title>")
assert "{{" not in head
cards = "\n".join(
    f'''    <a class="fam" href="{p["f"]}.html">
      <span class="mini" aria-hidden="true"><span class="mroof"></span><span class="mwalls">{p["f"]}</span></span>
      <span class="ftext"><span class="fname">The -{p["f"]} family</span>
      <span class="fwords">{", ".join(w for _, w, _ in p["words"][:4])}…</span></span>
    </a>''' for p in pages)
menu = head + f'''<style>
.fam{{display:flex;align-items:center;gap:20px;background:var(--panel);border:3px solid var(--line);border-radius:28px;padding:16px 20px;color:var(--ink);text-decoration:none}}
.fam:focus-visible{{outline:4px solid var(--butter);outline-offset:3px}}
.fam:active{{transform:scale(.98)}}
.mini{{display:flex;flex-direction:column;align-items:center;flex:none}}
.mroof{{width:0;height:0;border-left:48px solid transparent;border-right:48px solid transparent;border-bottom:28px solid var(--jam)}}
.mwalls{{background:var(--butter);color:#1D2742;width:80px;border-radius:0 0 10px 10px;padding:6px 0;text-align:center;font-family:var(--read);font-weight:700;font-size:2rem;line-height:1.1}}
.ftext{{display:flex;flex-direction:column;gap:2px;min-width:0}}
.fname{{font-family:var(--display);font-weight:800;font-size:1.7rem;line-height:1.1}}
.fwords{{color:var(--soft);font-size:1.15rem}}
.list{{display:flex;flex-direction:column;gap:16px}}
</style>
<div class="wrap">
  <header style="display:flex;flex-direction:column;gap:8px">
    <h1>Word <span class="am">Families</span></h1>
    <p class="lead">Pick a family house to play!</p>
  </header>
  <nav class="list" aria-label="Word families">
{cards}
  </nav>
</div>
<script>
if("serviceWorker" in navigator){{window.addEventListener("load",()=>{{navigator.serviceWorker.register("sw.js").catch(()=>{{}})}});}}
</script>
</body>
</html>
'''
(ROOT / "index.html").write_text(menu)

# Service worker: list every file, version = hash of contents so any change ships
assets = ["index.html", "manifest.webmanifest"] + [f'{p["f"]}.html' for p in pages] \
    + sorted(str(x.relative_to(ROOT)) for x in (ROOT / "icons").glob("*.png")) \
    + sorted(str(x.relative_to(ROOT)) for x in (ROOT / "fonts").glob("*.woff2"))
h = hashlib.sha256()
for a in assets:
    h.update((ROOT / a).read_bytes())
sw = (ROOT / "sw.js").read_text()
sw = re.sub(r'const VERSION = "[^"]*";', f'const VERSION = "wf-{h.hexdigest()[:10]}";', sw)
files = ",\n".join(f'  "{a}"' for a in ["./"] + assets)
sw = re.sub(r"const FILES = \[[\s\S]*?\];", "const FILES = [\n" + files + "\n];", sw)
(ROOT / "sw.js").write_text(sw)
print("built:", ", ".join(f'{p["f"]}.html' for p in pages), "+ index.html, sw.js", sw[sw.index("VERSION"):sw.index(";")])
