"""Render an original 30-second EDP motion-graphics concept film on macOS.

v2 (2026-09-11): copy follows the problem-type-entry positioning in
01 §5 — Jiangsu / Yangtze-delta context, three concrete questions (AI,
going global, organisation) and the verified programme categories from
the official EDP site. Visual system is unchanged from v1.

Requires Python 3, Pillow, NumPy, ffmpeg/ffprobe and the macOS Tingting voice.
Run: python3 assets/video/edp-brand-demo-v2/build_video.py
"""

from pathlib import Path
import json
import math
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "production"
WORK.mkdir(exist_ok=True)
W, H, FPS, DURATION = 1080, 1920, 30, 30
WHITE = (246, 242, 232)
GOLD = (225, 197, 141)
MUTED = (181, 173, 197)
FONT = "/System/Library/Fonts/STHeiti Light.ttc"
BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"
LATIN = "/System/Library/Fonts/Supplemental/Arial.ttf"
LATIN_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONTS = {}

# (start, end, TTS narration, subtitle lines). Letters are spaced in the
# narration so Tingting reads them out; subtitles use the normal spelling.
SCENES = [
    (0, 5, "变化更快了。江苏企业的经营，需要新答案。",
     ["变化来得更快", "江苏企业的经营，需要新的答案"]),
    (5, 11, "A I 先做哪个场景？出海先选哪个市场？组织如何跟上？",
     ["AI 先做哪个场景？出海先选哪个市场？", "组织如何跟上战略？"]),
    (11, 17, "走进南京大学，E D P。让学习，回应真实的经营问题。",
     ["走进南京大学 EDP", "让学习，回应真实的经营问题"]),
    (17, 23, "个人提升，或企业定制，都从真实的经营问题出发。",
     ["个人提升：AI 赋能 · 企业出海 · 卓越管理者", "企业定制：从组织的真实议题出发"]),
    (23, 30, "南京大学，E D P。了解项目详情，请通过官方渠道咨询。",
     ["南京大学 EDP", "了解项目详情，请通过官方渠道咨询"]),
]


def font(size, bold=False, latin=False):
    path = (LATIN_BOLD if bold else LATIN) if latin else (BOLD if bold else FONT)
    key = (path, size)
    if key not in FONTS:
        FONTS[key] = ImageFont.truetype(path, size)
    return FONTS[key]


def txt(draw, xy, text, size=40, fill=WHITE, bold=False, latin=False):
    draw.text(xy, text, font=font(size, bold, latin), fill=fill, stroke_width=0)


def center(draw, y, text, size=40, fill=WHITE, bold=False):
    f = font(size, bold)
    box = draw.textbbox((0, 0), text, font=f)
    draw.text(((W - box[2]) / 2, y), text, font=f, fill=fill)


def ease(x):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


def background():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.exp(-(((x - W * .82) / 700) ** 2 + ((y - H * .64) / 900) ** 2))
    top = np.exp(-(((x - W * .10) / 900) ** 2 + ((y - H * .04) / 620) ** 2))
    rng = np.random.default_rng(27)
    noise = rng.normal(0, .65, (H, W))
    base = np.empty((H, W, 3), dtype=np.uint8)
    for c, (start, a, b) in enumerate([(11, 31, 15), (9, 12, 8), (24, 47, 25)]):
        base[:, :, c] = np.clip(start + a * g + b * top + noise, 0, 255)
    return Image.fromarray(base)


BG = background()
rng = np.random.default_rng(15)
PARTICLES = [(float(rng.uniform(50, 1030)), float(rng.uniform(200, 1540)),
              float(rng.uniform(.7, 2)), float(rng.uniform(5, 17))) for _ in range(65)]


def architecture(draw, t, weight=1):
    # Original geometric perspective study; this does not depict a real campus.
    cx, cy = 615 + 32 * math.sin(t * .19), 1190
    for k in range(23):
        ang = t * .09 + k * .045
        rx, ry = 300 + k * 11, 160 + k * 7
        points = []
        for a in np.linspace(0, math.tau, 135):
            xx, yy = rx * math.cos(a), ry * math.sin(a)
            points.append((cx + xx * math.cos(ang) - yy * math.sin(ang),
                           cy + xx * math.sin(ang) + yy * math.cos(ang)))
        alpha = int((19 + 40 * (k / 22)) * weight)
        draw.line(points, fill=(*GOLD, alpha), width=2)
    for x, y, r, speed in PARTICLES:
        yy = 230 + (y - t * speed) % 1280
        a = int((35 + 50 * (.5 + .5 * math.sin(t * .6 + x))) * weight)
        draw.ellipse((x-r, yy-r, x+r, yy+r), fill=(*GOLD, a))
    for k in range(8):
        x = 115 + k * 121
        draw.line([(x, 1460), (540 + (x - 540) * .16, 1000)],
                  fill=(184, 168, 215, int(15 * weight)), width=1)


def scene_layer(i, local):
    layer = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(layer)
    rise = int(35 * (1 - ease(local / .85)))
    y = lambda v: v + rise
    tags = ["01 / JIANGSU IN TRANSITION", "02 / THREE REAL QUESTIONS", "03 / NANJING UNIVERSITY",
            "04 / YOUR NEXT CHAPTER", "05 / START A CONVERSATION"]
    txt(d, (90, y(255)), tags[i], 27, GOLD, latin=True)
    d.line([(92, y(317)), (92 + int(118 * ease(local)), y(317))], fill=GOLD, width=3)
    if i == 0:
        txt(d, (83, y(385)), "变化来得更快", 107, WHITE, True)
        txt(d, (83, y(530)), "经营需要新答案", 100, GOLD, True)
        txt(d, (93, y(745)), "长三角 · 制造与科技企业", 37, MUTED)
        txt(d, (93, y(807)), "下一阶段，企业需要怎样的管理者？", 43)
        txt(d, (94, 1395), "从一个真实的经营问题开始。", 34, MUTED)
    elif i == 1:
        txt(d, (85, y(378)), "三个真问题", 96, WHITE, True)
        txt(d, (85, y(514)), "先从哪个开始", 96, GOLD, True)
        for k, (a, b) in enumerate([("01", "AI，先做哪个场景？"), ("02", "出海，先选哪个市场？"),
                                     ("03", "组织，如何跟上战略？")]):
            progress = ease((local - .25 - k * .25) / .7)
            yy = 828 + k * 164 + int((1-progress) * 22)
            d.rounded_rectangle((90, yy, 990, yy+132), radius=18,
                                fill=(65, 43, 92, int(75*progress)),
                                outline=(218, 195, 151, int(45*progress)), width=1)
            txt(d, (125, yy+46), a, 29, (*GOLD, int(255*progress)), latin=True)
            txt(d, (215, yy+35), b, 48, (*WHITE, int(255*progress)))
    elif i == 2:
        txt(d, (85, y(390)), "南京大学", 111, WHITE, True)
        txt(d, (72, y(535)), "EDP", 292, GOLD, True, True)
        txt(d, (94, y(900)), "高层管理培训", 56, WHITE)
        txt(d, (94, y(1000)), "让学习，回应真实的经营问题。", 36, MUTED)
        txt(d, (95, 1398), "EXECUTIVE DEVELOPMENT PROGRAMS", 26, GOLD, latin=True)
    elif i == 3:
        txt(d, (85, y(378)), "带着真问题", 107, WHITE, True)
        txt(d, (85, y(526)), "开始下一段学习", 100, GOLD, True)
        for k, (title, sub, en) in enumerate([
            ("个人提升", "AI 赋能 · 企业出海 · 卓越管理者", "FOR INDIVIDUALS"),
            ("企业定制", "从组织的真实议题出发", "FOR ORGANIZATIONS")]):
            yy = 840 + 270 * k
            d.rounded_rectangle((90, yy, 990, yy+225), radius=22,
                                fill=(48, 30, 71, 200), outline=(195, 169, 124, 80), width=1)
            txt(d, (128, yy+27), en, 24, GOLD, latin=True)
            txt(d, (126, yy+77), title, 62, WHITE, True)
            txt(d, (130, yy+160), sub, 31, MUTED)
            txt(d, (875, yy+85), "+", 55, GOLD, latin=True)
    else:
        txt(d, (90, y(386)), "南京大学 EDP", 79, WHITE, True)
        txt(d, (85, y(565)), "下一段学习", 100, WHITE, True)
        txt(d, (85, y(706)), "从一个真问题开始", 92, GOLD, True)
        d.rounded_rectangle((90, 1020, 990, 1145), radius=16, fill=(*GOLD, 255))
        center(d, 1054, "了解项目 · 官方咨询", 46, (33, 21, 45), True)
        txt(d, (92, 1210), "edp.nju.edu.cn", 53, WHITE, latin=True)
        txt(d, (93, 1330), "非学历教育", 31, GOLD)
        txt(d, (93, 1390), "具体项目及招生信息以官方发布为准", 29, MUTED)
    return layer


def frame(t):
    img = BG.copy().convert("RGBA")
    geom = Image.new("RGBA", (W, H))
    architecture(ImageDraw.Draw(geom), t, .65 if t >= 5 else 1)
    img = Image.alpha_composite(img, geom)
    active = max(i for i, (a, _, _, _) in enumerate(SCENES) if a <= t)
    start = SCENES[active][0]
    local = t-start
    foreground = scene_layer(active, local)
    if active > 0 and local < .45:
        prev = scene_layer(active-1, t-SCENES[active-1][0])
        foreground = Image.blend(prev, foreground, ease(local/.45))
    img = Image.alpha_composite(img, foreground)
    d = ImageDraw.Draw(img)
    txt(d, (90, 101), "南京大学 EDP", 35, WHITE)
    d.rounded_rectangle((820, 92, 990, 144), radius=26, outline=(156, 142, 174), width=1)
    txt(d, (852, 103), "创意提案", 27, MUTED)
    d.line((90, 174, 990, 174), fill=(74, 58, 96), width=1)
    # Two-line subtitles stay above social app controls and below main content.
    for k, sub in enumerate(SCENES[active][3]):
        center(d, 1588 + k*59, sub, 36, WHITE)
    d.line((90, 1740, 990, 1740), fill=(79, 61, 99), width=2)
    d.line((90, 1740, 90+900*t/DURATION, 1740), fill=GOLD, width=3)
    txt(d, (90, 1790), "品牌招生创意样片 · 非正式招生发布", 25, MUTED)
    txt(d, (857, 1790), f"{active+1:02d} / 05", 24, GOLD, latin=True)
    # Only the final half second fades to black; CTA remains on screen for 6s.
    if t > 29.5:
        img = Image.blend(img, Image.new("RGBA", (W,H), (8,6,15,255)), (t-29.5)/.5)
    return img.convert("RGB")


def run(args):
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL)


def sound():
    sr = 48000
    length = DURATION*sr
    stereo = np.zeros((length,2), dtype=np.float32)
    # Original restrained ambient score: no third-party music samples.
    chords = [(130.8128,155.5635,195.9977,261.6256),
              (103.8262,130.8128,155.5635,207.6523),
              (155.5635,195.9977,233.0819,311.1270),
              (116.5409,146.8324,174.6141,233.0819),
              (130.8128,155.5635,195.9977,261.6256)]
    for j, chord in enumerate(chords):
        start = j*6
        n = min(8*sr,length-start*sr)
        tt = np.arange(n)/sr
        env = np.minimum(tt/1.2,1)*np.minimum((n/sr-tt)/2,1)
        for k, freq in enumerate(chord):
            pad = np.sin(2*np.pi*freq*tt + .12*np.sin(2*np.pi*.17*tt))
            pad += .15*np.sin(2*np.pi*freq*2*tt)
            stereo[start*sr:start*sr+n,0] += .007*env*pad
            stereo[start*sr:start*sr+n,1] += .007*env*np.sin(2*np.pi*(freq+.13)*tt)
        for beat in range(6):
            begin = int((start+beat*.82+.2)*sr)
            count=min(int(2.6*sr), length-begin)
            tt=np.arange(count)/sr
            f=chord[beat%4]*4
            note=(np.sin(2*np.pi*f*tt)+.28*np.sin(2*np.pi*f*2*tt))*np.exp(-tt*2.3)
            note*=np.minimum(tt/.015,1)*.032
            stereo[begin:begin+count,beat%2]+=note
            stereo[begin:begin+count,1-beat%2]+=.55*note
    narration_meta=[]
    for i,(start,end,line,_) in enumerate(SCENES):
        aiff=WORK/f"voice-{i}.aiff"
        wav=WORK/f"voice-{i}.wav"
        run(["say","-v","Tingting","-r","165","-o",str(aiff),line])
        duration=float(subprocess.check_output(["ffprobe","-v","error","-show_entries",
                         "format=duration","-of","default=noprint_wrappers=1:nokey=1",str(aiff)]))
        available=end-start-1.15
        tempo=max(1.,duration/available)
        run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(aiff),
             "-af",f"atempo={tempo:.6f},highpass=f=85,lowpass=f=10000,loudnorm=I=-18:TP=-2:LRA=7",
             "-ar",str(sr),"-ac","1","-c:a","pcm_s16le",str(wav)])
        with wave.open(str(wav)) as wf:
            voice=np.frombuffer(wf.readframes(wf.getnframes()),dtype='<i2').astype(np.float32)/32768
        offset=int((start+.6)*sr)
        count=min(len(voice),length-offset)
        stereo[offset:offset+count,:]+=voice[:count,None]*.88
        narration_meta.append({"scene":i+1,"start":start+.6,"duration":len(voice)/sr,
                               "tempo":round(tempo,3),"text":line})
    # Fade only music lead-in and whole audio tail.
    stereo[:int(.4*sr)]*=np.linspace(0,1,int(.4*sr))[:,None]
    stereo[-sr:]*=np.linspace(1,0,sr)[:,None]
    peak=float(np.max(np.abs(stereo)))
    if peak>.94:
        stereo*=.94/peak
    out=WORK/"soundtrack.wav"
    with wave.open(str(out),'wb') as wf:
        wf.setnchannels(2);wf.setsampwidth(2);wf.setframerate(sr)
        wf.writeframes((stereo*32767).astype('<i2').tobytes())
    (WORK/'narration.json').write_text(json.dumps(narration_meta,ensure_ascii=False,indent=2))
    return out


def main():
    for i,t in enumerate([2,7.5,13.5,19.5,26]):
        frame(t).save(WORK/f"scene-{i+1}.jpg",quality=93)
    frame(13.5).save(ROOT/"招生视频封面.jpg",quality=96)
    print("Rendering soundtrack",flush=True)
    audio=sound()
    output=ROOT/"南京大学EDP-招生创意样片-30秒-v2.mp4"
    args=["ffmpeg","-hide_banner","-loglevel","error","-y","-f","rawvideo","-vcodec","rawvideo",
          "-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i",str(audio),
          "-map","0:v","-map","1:a","-c:v","libx264","-preset","fast","-crf","19",
          "-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-ar","48000",
          "-t",str(DURATION),"-movflags","+faststart",str(output)]
    proc=subprocess.Popen(args,stdin=subprocess.PIPE)
    try:
        for f in range(FPS*DURATION):
            proc.stdin.write(frame(f/FPS).tobytes())
            if f%150==0:print(f"Rendered {f//FPS}/{DURATION} seconds",flush=True)
    finally:
        proc.stdin.close()
    if proc.wait()!=0:raise RuntimeError("ffmpeg failed")
    print(f"Saved {output}",flush=True)


if __name__ == '__main__':
    main()
