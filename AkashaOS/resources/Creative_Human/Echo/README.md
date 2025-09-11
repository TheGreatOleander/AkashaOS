
# 🧠 Autonomous YouTube Vlog Creator (FREE TIER ONLY)

This setup builds a **fully automated Bigfoot-style VLOG generator** using only FREE tools.
Everything runs locally or using free-tier cloud APIs.

---

## 🚀 What It Does

- Accepts a topic (e.g. "Bigfoot Sighting in Ohio")
- Auto-generates a YouTube script using a local LLM (LM Studio)
- Converts it to voice using a local TTS engine (Piper)
- Optionally adds stock image or background
- Assembles everything into an MP4 file
- Ready for upload to YouTube or Telegram

---

## 🧰 Tools Required

| Tool        | Use                          |
|-------------|------------------------------|
| **LM Studio** | Local LLM (e.g. Mistral, LLaMA) |
| **Piper TTS** | Local voice synthesis       |
| **n8n**       | Workflow automation          |
| **FFmpeg**    | Audio + video combining     |
| **Ubuntu**    | Base OS                     |

---

## 📁 Folder Layout

```bash
~/vlog_pipeline/
├── prompts/                 # Drop .txt files here (e.g., Bigfoot_Ohio.txt)
├── scripts/                 # Auto-generated scripts
├── audio/                   # Generated voice audio
├── output/                  # Final .mp4 videos
├── images/                  # Optional background JPG/PNG
├── generate.sh              # Main runner script
└── n8n_workflow.json        # (Optional) n8n version of automation
```

---

## ⚙️ How to Run

1. Start LM Studio with API mode enabled on port 1234
2. Run:
```bash
bash generate.sh prompts/Bigfoot_Ohio.txt
```
3. Output: `output/Bigfoot_Ohio.mp4`

---

## 🧠 generate.sh (core script)

- Reads topic from input `.txt`
- Sends prompt to LM Studio API
- Gets script and sends to Piper TTS
- Uses `ffmpeg` to combine audio + image
- Saves final `.mp4`

---

## 🆓 Fully Offline & Free

✅ No OpenAI key  
✅ No paid API  
✅ No root  
✅ No trackers  

---

## ✅ Next Steps

Would you like me to generate:

- [ ] `generate.sh` Linux script
- [ ] `n8n_workflow.json` to automate it visually
- [ ] `example_prompts/Bigfoot_Ohio.txt` starter pack
