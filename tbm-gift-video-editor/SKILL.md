---
name: tbm-gift-video-editor
description: TBM Gift video editor, a free gift from Sagar Sangam Sahu (Tribe Building Mastermind). Turns ONE short video (up to 3 minutes) into a finished vertical reel, YouTube Short or ad with brand captions, zooms, a hook headline and an optional call-to-action end card, plus a ready post caption. Short-form only, no long videos. Use when someone says "TBM gift", "edit my reel", "make this a reel", "make an ad from this clip", "add captions to my video", or shares a short video file.
---

# TBM Gift video editor (short-form only)

One short video in, one polished vertical video out. The heavy lifting is in `scripts/tbm.py`. Your job is judgment: cutting well and checking the result the way a viewer would.

**The person is a beginner who never uses Terminal.** Run every command yourself. Never ask them to open Terminal or type a command. Explain each step in one short, simple line. They will click "Allow" when Claude Code asks for permission.

`<skill-dir>` is the folder that contains this SKILL.md.
```
PY=~/.tbm-gift-work/.venv/bin/python                 # Mac
PY=~/.tbm-gift-work/.venv/Scripts/python.exe         # Windows
TBM=<skill-dir>/scripts/tbm.py
$PY $TBM <command> --project <project-folder>
```

## Short-form only (the gift's limit)
- Source video: **up to 3 minutes**. `fetch` refuses anything longer.
- If they bring a long video (podcast, webinar, Zoom call, YouTube video), say kindly: "This free TBM Gift edits short videos up to 3 minutes. Trim the part you want on your phone (Photos → Edit → drag the ends) and drop that in. Turning long videos into many reels is part of the TBM programme." Never cut a long source into clips yourself.
- Output: 9:16 vertical (Reels, Shorts, TikTok, Stories, ads). One video per request (an ad version of the same clip is fine).

## First use: setup (no Terminal)
If `~/.tbm-gift-work/.venv` does not exist, set up once. Tell them: "I'm installing your free editing tools. It takes 10-15 minutes. Keep your laptop plugged in."
- **Mac:** run `python3 <skill-dir>/scripts/setup.py`. If macOS shows a pop-up to install "Command Line Tools", tell them: "Click Install, then Agree, and wait until it says Done (5-15 minutes)." Then run setup again.
- **Windows:** check `py -3.12 --version`. If missing, run `winget install -e --id Python.Python.3.12 --scope user --accept-source-agreements --accept-package-agreements`, then `py -3.12 <skill-dir>/scripts/setup.py`. If `py` is still not found, ask them to quit Claude, open it again, and say "continue setup".
- Setup ends with `READY`. It needs no password and no Homebrew: ffmpeg comes bundled.
- Then make their folders if missing, inside the folder Claude Code is open in: `Raw Footage/`, `Reference/`, `Export/`. Tell them: "Drop your videos in Raw Footage. Finished videos appear in Export."

## 1. Intake (one AskUserQuestion call, short)
Find out the video type yourself from the frames; don't ask.
1. **What is it for?** Organic reel, paid ad, client testimonial, or promo/launch.
2. **Brand colour** for key words. If unsure, offer: yellow `#FFE14D`, lime `#C6F25E`, blue `#4DA3FF`, pink `#FF4D9D`, orange `#FF8A3D`, white only. Caption style: "brand" (small white line + big coloured keyword) or "bold" (big white words, the spoken word coloured).
3. **Language:** English, Hindi or Hinglish, and captions in Roman or Devanagari. For Hindi/Hinglish set `"language": "hi"` (uses the accurate "turbo" model, a one-time 1.5 GB download; it writes Devanagari, so convert captions to Roman if they chose Roman).
4. **Words to spell right:** their name, brand, programme and tool names ("Claude" is often heard as "cloud").
5. **End card / CTA?** e.g. comment a keyword, "book a free call", "register for my masterclass". Line 1 small, line 2 big, `|` for a line break.
6. **Ads only:** what goes at the top: an audience badge ("FOR COACHES"), a headline, or nothing.
Defaults: speed 1.0x, no music, no sound effects. Save answers in `<project>/config.json` (see `templates/config.example.json`; only what differs from `config.default.json`) and reuse them next time.

## 2. Style from reference reels (optional, once)
If they share 3-5 reels they like (links, or files in `Reference/`): ask before downloading, download with `yt-dlp` into `Reference/`, study frames, cuts and words (layout, fonts, colours, captions, zooms, pace) and write `style-guide.md` in their folder with exact colours and sizes. Inspire, don't copy: never reuse another creator's graphics or words. If Instagram blocks the download ("This content isn't available to everyone"), ask them to save the reel and drag it into `Reference/`.

## 3. Edit
1. `$PY $TBM fetch "<file in Raw Footage | link>" --project <project>` (project = `.work/<video-name>` in their folder). Then `transcribe`, then `words` on the whole video. One clip in `clips.json`: start 0, end = duration (see `templates/clips.example.json`). Set `"mode": "solo"`.
2. **Clean it:** cut retakes (keep the LAST clean take), false starts, "umm/uh", repeats and dead air. `"tighten_gaps": 0.45`. Start on the first strong sentence, end on the payoff.
3. **Hook headline** at the top: 2-3 curiosity options (an open loop, a number, a confession or a bold claim, 5-9 words, their own words). `"headline": "LINE ONE|*LINE TWO*"`, `*words*` in their colour.
4. **By type:**
   - Organic reel: headline + captions + zooms + optional CTA end card.
   - Ad: `"ad": true`, `"cold_open": [start, end]` = the single strongest line, plays first; CTA end card; 30-45 s works well.
   - Testimonial: keep the client's exact words, best 30-45 s, first name + one result line on screen. Remind them to get the client's OK to post (a WhatsApp "yes" is enough).
   - Promo/launch: lead with the offer's biggest promise, end on the CTA.
5. **Storyboard first:** show the cut list in plain words ("I'll remove the retakes at 0:12 and 0:40") + 2-3 headline options + one preview frame. Build only after they say go.
6. `$PY $TBM build all --project <project>` → copy the result to `Export/`.

## 4. Check (never skip)
Run `references/self-qa.md` and `$PY $TBM check all --project <project>`, then look at every contact sheet in `out/checks/`. The person must never be the one who finds a mistake. Fix, rebuild, re-check, then report what you checked.

## 5. Deliver
In `Export/`: the video, plus `<name>_caption.txt` with a post caption from what they actually said (hook in line 1, CTA by line 3, short lines, 5 hashtags). Never invent claims or numbers. Tell them: "Open Export, watch it with sound, then post."
Changes: they describe them like to a human editor ("at 0:12 the caption should say Claude"). Ask for all changes in one message and suggest a new chat for each new video; both save their Claude usage.

## Hard rules
1. Nothing ever covers the face. Captions sit below the face.
2. Eyes stay on one line through cuts and zooms; punch-in zooms hide jump cuts.
3. Seated speaker: head-and-chest crop. Standing or walking: full body is fine.
4. Fix every caption error: names, brands, numbers, currency (lakh, crore, ₹). Keep AI and brand names in capitals.
5. Hindi/Hinglish: rewrite captions in the script they chose; Whisper's spellings are often odd. If a stretch of speech is missing from the transcript, re-transcribe that time range on its own.
6. No music or whoosh sounds unless they ask. If they want music, they add a track they own and you keep it soft under the voice.
7. Final loudness -14 LUFS, 9:16, 1080x1920.
8. Ask before downloading anything from the internet.
9. Never ask them to use Terminal or type a password. If a step truly needs one, explain simply and let them decide.
10. Never edit more than 3 minutes of source, never cut a long video into clips.
