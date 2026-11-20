# Card Vault: TRAPWORKS and STARFALL ARMADA

Two original card game sets with **300 cards each**. Every card has the full card info: cost, name, type line, rarity, set symbol, collector number, keyword abilities with reminder text, flavor text, stats, and an artist/copyright line. Every card also has its own professional **art prompt**.

| Set | Theme | Groups |
|---|---|---|
| **TRAPWORKS: The Lower Floors** (TW) | Horror escape game | Crimson, Brass, Drowned, Ash, Lantern wings |
| **STARFALL ARMADA: Battle for the Helios Belt** (SFA) | Space mechs and battleships | United Navy, Helios Syndicate, Red Talon, Void Choir, Frontier Union |

Each set has 30 Legendary, 60 Rare, 90 Uncommon and 120 Common cards. This is **draft v0.1**: the rules text and stats were generated to a cost curve and still need playtesting.

## Look at the cards
Open `index.html` in Chrome. Use the set tabs, filters and search. Click a card to see it large, along with its art prompt and the file name its painting should use.

## Get high-end art: option A, free and unlimited on your PC (recommended)
This option uses ComfyUI and Stable Diffusion XL on your GTX 1660 Super. A painting takes about 30–90 seconds, so you can leave it running overnight.

1. Download **ComfyUI portable for Windows (NVIDIA)** from github.com/comfyanonymous/ComfyUI → Releases. Unzip it onto your **D:** drive.
2. Download the model `sd_xl_base_1.0.safetensors` (free) from huggingface.co/stabilityai/stable-diffusion-xl-base-1.0. Put it in `ComfyUI\models\checkpoints\`.
3. Double-click `run_nvidia_gpu.bat` and leave that window open.
4. In a terminal inside this `card-game` folder, run:
   ```
   D:\ComfyUI_windows_portable\python_embeded\python.exe tools\paint_cards.py --set TW --limit 5
   ```
   Check the 5 test cards in `index.html`. Then run the same command without `--limit 5` to paint everything. Legendaries and rares go first. You can stop with Ctrl+C at any time; running it again picks up where it left off.

Tips:
- **Black or green images on a GTX 16-series card:** edit `run_nvidia_gpu.bat` and add `--fp32-vae` to the end of the python line.
- **Two GPUs in the PC:** the Quadro K6000 is too old for current Stable Diffusion builds, so use the 1660 Super. If ComfyUI grabs the wrong card, add `--cuda-device 1` (or `0`) to that same line.
- **Other SDXL models:** you can use a different model from civitai.com or Hugging Face with `--ckpt filename.safetensors`. If you plan to sell the cards, check that model's license allows commercial use. SDXL base 1.0 does.
- **Redo one card:** `python tools\paint_cards.py --only TW-014 --force`

## Get high-end art: option B, Gemini / Nano Banana (free with a daily limit)
1. Open the card in `index.html` and click **Copy prompt**. You can also find every prompt in `data/art_prompts_tw.csv` and `data/art_prompts_sfa.csv`.
2. Paste the prompt into gemini.google.com and download the image.
3. Save it as `art/TW/TW-014.png`. Use the card's ID as the name; jpg and webp also work.
4. Run `python tools\paint_cards.py --manifest-only`. The gallery will show the new art.

## Files
- `index.html`: the card gallery (self-contained)
- `data/cards_tw.json`, `data/cards_sfa.json`: the full card databases
- `data/art_prompts_*.csv`: one art prompt per card, with the file name to save it as
- `tools/gen_cards.py`: regenerates the card sets
- `tools/paint_cards.py`: paints the art with local ComfyUI and updates `art/manifest.js`
- `tools/build_gallery.py`: rebuilds `index.html` after card data changes
- `art/concept/`: the first 12 concept paintings (vector)
- `concept-boards/`: the design canvas boards
