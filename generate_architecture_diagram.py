from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
import os, math

W, H = 2400, 1800

img = Image.new("RGB", (W, H), "white")
draw = ImageDraw.Draw(img)

# Fonts

def font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

F_TITLE = font(48, True)
F_SUB = font(28, False)
F_HEAD = font(30, True)
F_BODY = font(22, False)
F_SMALL = font(18, False)
F_TINY = font(16, False)

def box(x, y, w, h, title, body="", fill=(248,248,248), outline=(60,60,60), title_fill=None, title_color=(0,0,0), body_color=(0,0,0), radius=18):
    draw.rounded_rectangle([x, y, x+w, y+h], radius=radius, fill=fill, outline=outline, width=3)
    pad = 18
    ty = y + pad
    draw.text((x+pad, ty), title, font=F_HEAD, fill=title_color)
    ty += 42
    if body:
        max_chars = max(18, int(w / 13))
        lines = []
        for para in body.split("\n"):
            if para.strip() == "":
                lines.append("")
            else:
                lines.extend(wrap(para, width=max_chars))
        for line in lines[: int((h-80)/28)]:
            draw.text((x+pad, ty), line, font=F_BODY, fill=body_color)
            ty += 28
    return (x, y, w, h)

def small_box(x, y, w, h, title, body="", fill=(255,255,255), outline=(80,80,80)):
    draw.rounded_rectangle([x,y,x+w,y+h], radius=14, fill=fill, outline=outline, width=2)
    pad=14
    draw.text((x+pad,y+pad), title, font=F_BODY, fill=(0,0,0))
    ty=y+pad+30
    if body:
        max_chars=max(16,int(w/11))
        lines=[]
        for para in body.split("\n"):
            lines += wrap(para, width=max_chars) if para.strip() else [""]
        for line in lines[: int((h-55)/23)]:
            draw.text((x+pad,ty), line, font=F_SMALL, fill=(0,0,0))
            ty += 23
    return (x,y,w,h)

def arrow(frm, to, color=(40,40,40), width=4):
    x,y,w,h = frm
    x2,y2,w2,h2 = to
    start=(x+w, y+h/2)
    end=(x2, y2+h2/2)
    draw.line([start,end], fill=color, width=width)
    # arrowhead
    ang=math.atan2(end[1]-start[1], end[0]-start[0])
    ah=18
    pts=[
        end,
        (end[0]-ah*math.cos(ang-math.pi/6), end[1]-ah*math.sin(ang-math.pi/6)),
        (end[0]-ah*math.cos(ang+math.pi/6), end[1]-ah*math.sin(ang+math.pi/6)),
    ]
    draw.polygon(pts, fill=color)

# Title
draw.rectangle([0,0,W,130], fill=(20,20,20))
draw.text((80,30), "EnMaTeS → Overworker/49 AgentOps Architecture", font=F_TITLE, fill=(255,255,255))
draw.text((80,88), "Controlled context-engineering system for 24/7 repo-to-product operation", font=F_SUB, fill=(230,230,230))

# Row 1
b1 = box(80, 170, 430, 270, "1. System Corpus",
         "/02_Systems/\n\n01 Cyberries: Obsidian vault + website\n21 EnMaTeS: primary methodology\n22 CAFET+O: business architecture lens\n41 Planfix: optional ops backend")
b2 = box(570, 170, 430, 270, "2. EnMaTeS Core",
         "Entrepreneurial Managerial Technological System.\n\nInterpretation: controlled context-engineering OS for specialized AI agents over semantic graphs and source artifacts.",
         fill=(252,252,252))
b3 = box(1060, 170, 520, 270, "3. Assembly Rule",
         "Do not operate from loose chat memory.\nOperate from SI + IP.\n\nSI = SMF + FPM + FPS + PIC\nIP = SG + SDA + SP + UM\nChatConfig declares exact versions to load.",
         fill=(238,238,238))
b4 = box(1640, 170, 680, 270, "4. Active Project: overandor/49",
         "Mission: repo-to-product transformation.\n\nTarget: 20-hour/day AgentOps loop.\n\nPackage: EnMaTeS artifact tree + app.py + ledgers + claim registry + release gates.",
         fill=(252,252,252))

for a,b in [(b1,b2),(b2,b3),(b3,b4)]:
    arrow(a,b)

# Row 2 components
si = box(80, 520, 520, 250, "System Instruction / SI",
         "SMF: semantic graph schema\nFPM: operating mode\nFPS: agent role/specialization\nPIC: mission, purpose, constraints",
         fill=(245,245,245))
ip = box(680, 520, 520, 250, "Initiation Package / IP",
         "SG: persistent project memory\nSDA: source documents/artifacts\nSP: starting prompt\nUM: operator manual",
         fill=(245,245,245))
cc = box(1280, 520, 480, 250, "ChatConfig",
         "Declares which SI + IP components compose each agent.\n\nDefines audience, mode, project, purpose, versions, and loading order.",
         fill=(245,245,245))
agent = box(1840, 520, 480, 250, "Running Agent",
            "Loads ChatConfig → assembles SI → loads IP → retrieves SG nodes → fetches SDA evidence → acts boundedly → updates graph and ledgers.",
            fill=(245,245,245))

arrow(si, cc); arrow(ip, cc); arrow(cc, agent)

# CAFET + Planfix bars
cafet = box(80, 830, 1080, 150, "CAFET+O Business Architecture Lens",
            "Concept = messy work → verified package | Asset = repo files, docs, prompts, reports | Flow = ingest → verify → score → package → deploy | Engine = app.py, workers, analyzers, exporters, CI | Theme = EnMaTeS AgentOps | O = pricing, pilots, deployment, operations",
            fill=(250,250,250))
planfix = box(1240, 830, 1080, 150, "Planfix Operations Backend",
              "Optional later integration: Overworker SG task queue → Planfix tasks → 20-hour AgentOps cycles → human review gates → package/release checklist.",
              fill=(250,250,250))

# Roles table-like section
draw.text((80, 1040), "Agent Role Taxonomy", font=F_HEAD, fill=(0,0,0))
roles = [
    ("EnMaTeSArchitect", "Design package architecture, folder tree, graph schema, ChatConfig."),
    ("AgentDeveloper", "Build app.py, exporters, tests, repo ingestion, UI."),
    ("DomainExpert", "Answer from SG + SDA; navigate the knowledge base."),
    ("TesterAI", "Generate tests, RAG checks, ambiguity checks, hallucination checks."),
    ("VerificationFirewall", "Validate README/product claims against code evidence."),
    ("ReleaseManager", "Control deployment, changelog, ZIP export, release gates."),
]
x0, y0 = 80, 1090
for i,(r,d) in enumerate(roles):
    small_box(x0 + (i%3)*740, y0 + (i//3)*125, 700, 100, f"FPS_{r}_Overworker49", d, fill=(252,252,252))

# Cycle loop
draw.text((80, 1370), "20-Hour / Day Operating Loop: 10 × 2-Hour Cycles", font=F_HEAD, fill=(0,0,0))
cycles = [
    "1 State refresh + graph sync",
    "2 Code patch / app.py / UI",
    "3 Tests + validation",
    "4 Claim verification",
    "5 Risk/security review",
    "6 EnMaTeS artifact generation",
    "7 Documentation / user manual",
    "8 Deployment checks",
    "9 Package ZIP export",
    "10 Daily report + next plan",
]
cols=5
cw=440
ch=74
for i,c in enumerate(cycles):
    x = 80 + (i%cols)*460
    y = 1420 + (i//cols)*95
    small_box(x,y,cw,ch,c,"",fill=(248,248,248))
    if i < len(cycles)-1 and i%cols != cols-1:
        arrow((x,y,cw,ch), (x+460,y,cw,ch), width=3)

# Return arrow from cycle 10 to 1 (rough)
draw.line([(80+4*460+cw/2,1420+95+ch),(80+cw/2,1420+95+ch+60),(80+cw/2,1420+ch)], fill=(80,80,80), width=3)

# Output + quality
out = box(80, 1635, 1080, 140, "Output Package",
          "enmates/00_system_overview … 10_chat_configurations + agentops_config.json + task_queue.json + progress_ledger.json + risk_register.json + claim_registry.json + artifact_manifest.json",
          fill=(245,245,245))
q = box(1240, 1635, 1080, 140, "Quality Gates + Security Warning",
        "app.py launches | tests pass | ZIP export works | claims source-supported | secrets redacted | repo input validated | clone timeout + size caps active | README claims match code behavior. Rotate any pasted Twilio, Telegram, Hugging Face, or API credentials before deployment.",
        fill=(245,245,245), outline=(160,40,40))

# Save
script_dir = os.path.dirname(os.path.abspath(__file__))
png_path = os.path.join(script_dir, "enmates_overworker49_agentops_architecture.png")
svg_path = os.path.join(script_dir, "enmates_overworker49_agentops_architecture.svg")

img.save(png_path, quality=95)

# Create simple SVG by embedding PNG for vector container compatibility
import base64
with open(png_path, "rb") as f:
    data = base64.b64encode(f.read()).decode()

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<image width="{W}" height="{H}" href="data:image/png;base64,{data}"/>
</svg>'''

with open(svg_path, "w") as f:
    f.write(svg)

print(f"Generated: {png_path}")
print(f"Generated: {svg_path}")
