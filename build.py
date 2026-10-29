#!/usr/bin/env python3
"""Build the word family lessons.

Each entry in PAGES becomes <slug>.html from lesson.template.html.
index.html becomes the menu, and sw.js gets the new file list and a new
cache version so the iPad picks up the change.

Usage: python3 build.py
"""
import json, re, hashlib, pathlib

ROOT = pathlib.Path(__file__).parent

# Pictures for every word. They only appear after she has read or spelled the word.
PICS = {
    "ham": "🍖", "jam": "🫙🍓", "ram": "🐏", "yam": "🍠", "Sam": "👦", "Pam": "👧",
    "clam": "🐚", "swam": "🏊", "tram": "🚋", "wham": "💥",
    "cap": "🧢", "map": "🗺️", "nap": "😴", "tap": "🚰", "zap": "⚡", "yap": "🐶",
    "clap": "👏", "trap": "🪤", "snap": "🐊", "Hap": "🐶", "rap": "🎤",
}

def grown(blend, booklets=None):
    items = [
        "Keep it short: about 10 minutes, stop while she still wants more.",
        f"In Part 2, have her say the first sound, then the ending, then blend them: “{blend}” Blending is the skill word families build.",
        "In Part 3 (Spell it), let her say the word slowly and touch each box as she says each sound before she picks letters. Spelling a word helps her remember it for reading.",
        "In Part 4, only first-try answers earn a star. If she misses, the word splits into sounds: have her sound it out before she taps again. Missed words come back at the end, and the list at the end shows what to practise tomorrow.",
    ]
    if booklets:
        items.append(f"Pair this with the school's booklets on Hubbard's Cupboard ({booklets}) and magnetic letters on the fridge.")
    items.append("Praise the sounding out, not just right answers.")
    return "".join(f"<li>{i}</li>" for i in items)

PAGES = [
    {
        "slug": "am", "menu_name": "The -am family", "title": "The Am Family",
        "h1": 'The <span class="am">-am</span> Family',
        "lead": "All these words end the same way: <b>a</b> + <b>m</b> says <b>“am”</b>!",
        "house_title": "Meet the family house",
        "house_hint": "Say it with me: “aaaa-mmm… am!” Tap to hear it.",
        "rimes": ["am"],
        "onsets": ["h", "j", "r", "y", "S", "P", "cl", "sw", "tr", "wh"],
        "spell": ["ham", "jam", "ram", "yam", "clam", "tram"],
        "game": ["ham", "jam", "ram", "yam", "clam", "swam", "tram", "wham"],
        "game_len": 10,
        "sample": ["jam", "ham, jam, ram"],
        "story_title": "Sam the Ram",
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
        "grownup": grown("j… am… jam!", "“Pam and Sam”, then “Shhh!”"),
    },
    {
        "slug": "ap", "menu_name": "The -ap family", "title": "The Ap Family",
        "h1": 'The <span class="am">-ap</span> Family',
        "lead": "All these words end the same way: <b>a</b> + <b>p</b> says <b>“ap”</b>!",
        "house_title": "Meet the family house",
        "house_hint": "Say it with me: “aaaa… p… ap!” Tap to hear it.",
        "rimes": ["ap"],
        "onsets": ["c", "m", "n", "t", "z", "y", "cl", "tr", "sn", "H"],
        "spell": ["cap", "map", "nap", "tap", "clap", "trap"],
        "game": ["cap", "map", "nap", "tap", "zap", "clap", "trap"],
        "game_len": 10,
        "sample": ["cap", "cap, map, nap"],
        "story_title": "Hap the Pup",
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
        "grownup": grown("c… ap… cap!", "“Hap Can See”, then “I Like to Dance!”"),
    },
    {
        "slug": "mix-am-ap", "menu_name": "Mix it up: -am and -ap", "title": "Am and Ap Mix",
        "h1": 'Mix it up! <span class="am">-am</span> <span class="am">+ -ap</span>',
        "lead": "Look all the way to the end! Is it <b>am</b> or <b>ap</b>?",
        "house_title": "Two family houses",
        "house_hint": "“am” ends with your lips closed: mmm. “ap” ends with a little pop: p! Tap to hear them.",
        "rimes": ["am", "ap"],
        # every first sound here makes a real word with BOTH endings (ram / rap, clam / clap...)
        "onsets": ["r", "y", "cl", "tr"],
        "spell": ["ham", "map", "jam", "cap", "ram", "nap", "clam", "clap"],
        "spell_extra": ["m", "p"],
        # look-alike pairs (clam/clap, tram/trap) are offered as wrong answers first
        "game": ["ham", "jam", "yam", "ram", "clam", "tram", "cap", "map", "nap", "tap", "clap", "trap"],
        "game_len": 12,
        "sample": ["clam, clap", "jam, cap, tram, trap"],
        "story_title": "Sam and Hap",
        "story": [
            ["<b>Sam</b> the <b>ram</b> has a <b>cap</b>.","Sam the ram has a cap.","🐏🧢"],
            ["<b>Hap</b> the pup has a <b>map</b>.","Hap the pup has a map.","🐶🗺️"],
            ["<b>Sam</b> can <b>clap</b>.","Sam can clap.","👏"],
            ["<b>Hap</b> had a <b>nap</b>.","Hap had a nap.","😴"],
            ["Look! A <b>tram</b>!","Look! A tram!","🚋"],
            ["Look! A <b>trap</b>!","Look! A trap!","🪤"],
            ["<b>Snap</b>! went the <b>trap</b>.","Snap! went the trap.","🪤"],
            ["<b>Hap</b> and <b>Sam</b> ran to the <b>tram</b>.","Hap and Sam ran to the tram.","🚋"],
            ["<b>Pam</b> has <b>ham</b> and <b>jam</b>.","Pam has ham and jam.","👧🍖"],
            ["Yum! <b>Sam</b> had a <b>yam</b>.","Yum! Sam had a yam.","🍠"],
            ["<b>Yap</b>! <b>Yap</b>! <b>Hap</b> is glad.","Yap! Yap! Hap is glad.","🐶"],
            ["<b>Clap</b>, <b>clap</b>, <b>clap</b>! The end!","Clap, clap, clap! The end!","👏"],
        ],
        "grownup": "".join(f"<li>{i}</li>" for i in [
            "Use this page once she reads -am and -ap words on their own pages without much help.",
            "This page is the real test: the ending changes, so she has to read every letter. Word pairs like clam / clap and tram / trap are there on purpose.",
            "If she guesses the ending, point at the last letter and ask “m or p?” Let her feel it: lips stay closed for m, a little pop for p.",
            "In Spell it, both m and p are always in the letters, so she has to listen to the end of the word.",
            "Wrong first taps in the game come back at the end, and the list at the end shows what to practise tomorrow.",
            "Keep it to about 10 minutes, and praise the sounding out.",
        ]),
    },
]

def js(v):
    return json.dumps(v, ensure_ascii=False)

# ---------- Built-in voice ----------
# Every word and sentence the pages say is recorded ahead of time with Kokoro, an open
# neural voice (Apache 2.0), and saved as small MP3s in audio/. The iPad plays these,
# so the voice is the same on every device and works offline.
# Recording needs the model files (about 350 MB, not stored in the repo):
#   https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0
#   kokoro-v1.0.onnx and voices-v1.0.bin in the folder named by KOKORO_DIR (default ../tts)
#   pip install kokoro-onnx soundfile ; ffmpeg on the PATH
# Clips already in audio/ are reused, so only new sentences get recorded.
import os, subprocess, tempfile
VOICE = "af_heart"      # warm US English voice
SPEED = 0.9             # a little slower than normal speech for a beginning reader
SLOW = 0.7              # "Hear the word" in Spell it
AUDIO_DIR = ROOT / "audio"

def spoken_texts(p):
    """Everything this page can say: (key, text, speed)."""
    words = [o + r for o in p["onsets"] for r in p["rimes"] if o + r in PICS]
    words += p["spell"] + p["game"] + p["rimes"]
    items = [(w, w, SPEED) for w in words]
    items += [("slow:" + w, w, SLOW) for w in p["spell"]]
    items += [(t, t, SPEED) for _, t, _ in p["story"]]
    items += [(p["sample"][0], p["sample"][0], SPEED),
              ("Hi! Let's read. " + p["sample"][1], "Hi! Let's read. " + p["sample"][1], SPEED),
              ("pick a sound first", "Pick a sound first!", SPEED),
              ("pick a first sound and an ending", "Pick a first sound and an ending!", SPEED)]
    return items

def clip_name(text, speed):
    return "audio/" + hashlib.sha1(f"{VOICE}|{speed}|{text}".encode()).hexdigest()[:12] + ".mp3"

_kokoro = None
def record(text, speed, out):
    global _kokoro
    if _kokoro is None:
        from kokoro_onnx import Kokoro
        d = pathlib.Path(os.environ.get("KOKORO_DIR", ROOT.parent / "tts"))
        _kokoro = Kokoro(str(d / "kokoro-v1.0.onnx"), str(d / "voices-v1.0.bin"))
    import soundfile as sf
    samples, rate = _kokoro.create(text, voice=VOICE, speed=speed, lang="en-us")
    with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
        sf.write(tmp.name, samples, rate)
        # trim leading silence, keep a short tail, mono 48 kbps MP3
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp.name,
                        "-af", "silenceremove=start_periods=1:start_threshold=-50dB,apad=pad_dur=0.15",
                        "-ac", "1", "-b:a", "48k", str(out)], check=True)

def audio_map(p):
    AUDIO_DIR.mkdir(exist_ok=True)
    m = {}
    for key, text, speed in spoken_texts(p):
        name = clip_name(text, speed)
        if not (ROOT / name).exists():
            record(text, speed, ROOT / name)
            print("  recorded:", text if speed == SPEED else text + " (slow)")
        m[key] = name
    return m

tpl = (ROOT / "lesson.template.html").read_text()
for p in PAGES:
    words = set(p["spell"]) | set(p["game"]) | {o + r for o in p["onsets"] for r in p["rimes"] if o + r in PICS}
    for w in words:
        assert w in PICS, (p["slug"], w)
        assert any(w.endswith(r) for r in p["rimes"]), (p["slug"], w)
    for o in p["onsets"]:
        assert any(o + r in PICS for r in p["rimes"]), (p["slug"], o)
    config = {
        "rimes": p["rimes"], "onsets": p["onsets"], "pics": PICS,
        "spell": p["spell"], "spellExtra": p.get("spell_extra", []),
        "game": p["game"], "gameLen": p["game_len"], "story": p["story"],
        "sample1": p["sample"][0], "sample3": p["sample"][1],
        "audio": audio_map(p),
    }
    out = tpl
    for k, v in {
        "{{TITLE}}": p["title"], "{{H1}}": p["h1"], "{{LEAD}}": p["lead"],
        "{{HOUSETITLE}}": p["house_title"], "{{HOUSEHINT}}": p["house_hint"],
        "{{STORYTITLE}}": p["story_title"], "{{GROWNUP}}": p["grownup"], "{{CONFIG}}": js(config),
    }.items():
        out = out.replace(k, v)
    assert "{{" not in out, p["slug"]
    (ROOT / f'{p["slug"]}.html').write_text(out)

# Menu page: reuse the template's head and styles
head = tpl[: tpl.index("\n/* two houses")] + "\n</style>\n"
head = head.replace("<title>{{TITLE}}</title>", "<title>Word Families</title>")
assert "{{" not in head
def card(p):
    house = "+".join(p["rimes"])
    words = ", ".join((p["spell"])[:4])
    return f'''    <a class="fam{' mixcard' if len(p["rimes"]) > 1 else ''}" href="{p["slug"]}.html">
      <span class="mini" aria-hidden="true"><span class="mroof"></span><span class="mwalls">{house}</span></span>
      <span class="ftext"><span class="fname">{p["menu_name"]}</span>
      <span class="fwords">{words}…</span></span>
    </a>'''
cards = "\n".join(card(p) for p in PAGES)
menu = head + f'''<style>
.fam{{display:flex;align-items:center;gap:20px;background:var(--panel);border:3px solid var(--line);border-radius:28px;padding:16px 20px;color:var(--ink);text-decoration:none}}
.fam:focus-visible{{outline:4px solid var(--butter);outline-offset:3px}}
.fam:active{{transform:scale(.98)}}
.mixcard{{border-color:var(--jam)}}
.mini{{display:flex;flex-direction:column;align-items:center;flex:none}}
.mroof{{width:0;height:0;border-left:52px solid transparent;border-right:52px solid transparent;border-bottom:28px solid var(--jam)}}
.mwalls{{background:var(--butter);color:#1D2742;width:88px;border-radius:0 0 10px 10px;padding:6px 0;text-align:center;font-family:var(--read);font-weight:700;font-size:1.8rem;line-height:1.1}}
.mixcard .mwalls{{font-size:1.25rem;padding:12px 0}}
.ftext{{display:flex;flex-direction:column;gap:2px;min-width:0}}
.fname{{font-family:var(--display);font-weight:800;font-size:1.6rem;line-height:1.15}}
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
assets = ["index.html", "manifest.webmanifest"] + [f'{p["slug"]}.html' for p in PAGES] \
    + sorted(str(x.relative_to(ROOT)) for x in (ROOT / "icons").glob("*.png")) \
    + sorted(str(x.relative_to(ROOT)) for x in (ROOT / "fonts").glob("*.woff2")) \
    + sorted(str(x.relative_to(ROOT)) for x in AUDIO_DIR.glob("*.mp3"))
h = hashlib.sha256()
for a in assets:
    h.update((ROOT / a).read_bytes())
sw = (ROOT / "sw.js").read_text()
sw = re.sub(r'const VERSION = "[^"]*";', f'const VERSION = "wf-{h.hexdigest()[:10]}";', sw)
files = ",\n".join(f'  "{a}"' for a in ["./"] + assets)
sw = re.sub(r"const FILES = \[[\s\S]*?\];", "const FILES = [\n" + files + "\n];", sw)
(ROOT / "sw.js").write_text(sw)
print("built:", ", ".join(f'{p["slug"]}.html' for p in PAGES), "+ index.html, sw.js")
