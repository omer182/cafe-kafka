# Café Kafka: ChatGPT image prompts

These prompts give one consistent anime cast for Café Kafka. Paste them into ChatGPT (image generation) **in order**: one character at a time, starting with their reference sheet.

## How to get consistent characters

1. **Use one chat per character.** Start with the **reference sheet** prompt. When you like it, keep using that same chat for the rest of that character's images.
2. **If a new chat is needed, attach the reference sheet** and start your prompt with: *"Same character as the attached reference sheet, same face, hair, outfit and colours."*
3. **Regenerate rather than fix.** If a detail is wrong (buttons, apron colour, hair length), regenerate or say *"Keep everything the same, but fix: …"*
4. **Ask for a transparent background.** Every prompt asks for one. If ChatGPT gives a solid background instead, that's fine. I'll cut it out.
5. **Save each image with the file name shown next to its prompt.** That way I can process the whole folder automatically.

When you have a batch, copy the folder to the server:

```bash
scp -r D:\Downloads\cafe-art rio@192.168.0.147:~/cafe-art-inbox/
```

Then tell me, and I'll remove the backgrounds, crop, size, build sprite sheets and wire everything into the game.

---

## The style line (already inside every prompt below)

> **STYLE:** modern Japanese anime illustration, clean confident line art in dark brown ink, two-tone cel shading (base colour plus one crisp shadow), soft warm rim light, vibrant but warm palette, large expressive eyes with bright highlights, polished anime key-visual quality. Character only, centred, transparent background, no scenery, no text, no logo, no watermark.

> **CHIBI STYLE:** chibi / super-deformed version, about 2.5 heads tall, big head and eyes, small body, same outfit and colours as the full-size character, thick clean outline, simple two-tone cel shading, game sprite, centred, transparent background, no ground shadow, no text.

## The kitchen uniform (shared by all six chefs)

> white double-breasted chef jacket with two rows of silver buttons and a stand collar, collar edge and cuffs piped in **{TEAM COLOUR}**, long white waist apron with a **{TEAM COLOUR}** waistband, dark charcoal trousers, black kitchen clogs, tall white pleated chef toque

Each chef has their own team colour. In the game it's the colour of the rail they work, so keep it exact.

| Chef | Team colour | Hex |
|---|---|---|
| Marco | tomato red | `#E4573D` |
| Yuki | steel blue | `#5B8DB8` |
| Kofi | herb green | `#7FB069` |
| Elena | lilac | `#C9A0DC` |
| Priya | brass gold | `#D9A441` |
| Sam | teal | `#4FB6A8` |

---

## 1. The chefs

Each chef has the same six prompts. Yuki's are written out in full. For the others, copy Yuki's prompts and swap in that chef's **look** and **team colour** from the cast list below.

### Yuki: the calm, precise one (steel blue)

**Look:** young Japanese woman, short glossy black bob with straight bangs, warm amber eyes, small beauty mark under her left eye, slim, calm and confident, a slight knowing smile.

**`yuki_sheet.png`**: reference sheet (landscape)
```
Character reference sheet of an original anime character, "Chef Yuki". Young Japanese woman, short glossy black bob with straight bangs, warm amber eyes, small beauty mark under her left eye, slim, calm and confident, a slight knowing smile. Outfit: white double-breasted chef jacket with two rows of silver buttons and a stand collar, collar edge and cuffs piped in steel blue (#5B8DB8), long white waist apron with a steel blue waistband, dark charcoal trousers, black kitchen clogs, tall white pleated chef toque. Show full body front view, three-quarter view and back view side by side, plus a row of four small head close-ups: neutral, laughing, shocked, determined. STYLE: modern Japanese anime illustration, clean confident line art in dark brown ink, two-tone cel shading, soft warm rim light, vibrant but warm palette, large expressive eyes with bright highlights, polished anime key-visual quality. Plain transparent background, no scenery, no text labels, no logo, no watermark.
```

**`yuki_portrait.png`**: hero portrait (portrait 2:3)
```
Same character as the reference sheet. Chef Yuki standing in a confident pose with arms crossed, knees-up framing, three-quarter view, a slight knowing smile, looking at the viewer. STYLE: modern Japanese anime illustration, clean confident line art in dark brown ink, two-tone cel shading, soft warm rim light, polished anime key-visual quality. Character only, transparent background, no scenery, no text, no watermark.
```

**`yuki_bust_happy.png`, `yuki_bust_shocked.png`, `yuki_bust_fired.png`**: busts for the manga cut-ins (square 1:1). Run the prompt three times, changing only the last part:
```
Same character as the reference sheet. Chest-up bust of Chef Yuki, three-quarter view facing right, dynamic anime cut-in pose, holding a sauté pan. Expression: [happy: bright open smile, eyes sparkling] / [shocked: wide eyes, sweat drop, mouth open in panic] / [fired up: determined grin, intense eyes, a small flame glint in her eyes]. STYLE: modern Japanese anime illustration, clean confident line art in dark brown ink, two-tone cel shading, strong rim light, polished anime key-visual quality. Character only, transparent background, no text, no watermark.
```

**`yuki_chibi_idle.png`**: kitchen sprite (square 1:1)
```
Same character as the reference sheet. Chibi / super-deformed Chef Yuki, about 2.5 heads tall, standing idle with a small proud smile, hands on hips, full body, three-quarter view. Same outfit and colours: white double-breasted chef jacket with steel blue piping, white apron with steel blue waistband, pleated toque. CHIBI STYLE: thick clean outline, simple two-tone cel shading, game sprite, centred, transparent background, no ground shadow, no text.
```

**`yuki_chibi_cook.png`**: cooking sprite (square 1:1)
```
Same character as the reference sheet. Chibi Chef Yuki, about 2.5 heads tall, tossing noodles in a sauté pan with flames and a few sparkles, focused happy face, full body, three-quarter view. Same outfit and colours. CHIBI STYLE: thick clean outline, simple two-tone cel shading, game sprite, centred, transparent background, no ground shadow, no text.
```

**`yuki_chibi_down.png`**: tripped / crashed sprite (square 1:1)
```
Same character as the reference sheet. Chibi Chef Yuki, about 2.5 heads tall, has slipped and is sitting on the floor dazed, swirl eyes, little cartoon stars circling her head, toque tilted, an empty pan beside her, full body. Same outfit and colours. CHIBI STYLE: thick clean outline, simple two-tone cel shading, game sprite, centred, transparent background, no ground shadow, no text.
```

**`yuki_chibi_bye.png`**: clocking out (square 1:1)
```
Same character as the reference sheet. Chibi Chef Yuki, about 2.5 heads tall, toque off and held in one hand, waving goodbye with a tired happy smile, full body. Same outfit and colours. CHIBI STYLE: thick clean outline, simple two-tone cel shading, game sprite, centred, transparent background, no ground shadow, no text.
```

### The rest of the crew

Use Yuki's six prompts. In each one, replace **"Chef Yuki"** with the chef's name, her **look** sentence with theirs, and **steel blue (#5B8DB8)** with their colour.

| Chef | Look (paste in place of Yuki's) | Colour |
|---|---|---|
| **Marco** (the hothead) | young Italian man in his mid-20s, messy wavy dark brown hair, light stubble, thick expressive eyebrows, warm brown eyes, tall, big cheerful energy | tomato red (#E4573D) |
| **Kofi** (the gentle giant) | young Ghanaian man, deep brown skin, short twists, round wire glasses, broad shoulders, big friendly grin | herb green (#7FB069) |
| **Elena** (the fast one) | young Spanish woman, long auburn braid over her shoulder, freckles, green eyes, energetic and quick | lilac (#C9A0DC) |
| **Priya** (the perfectionist) | young Indian woman, warm brown skin, long black hair in a high ponytail, small gold stud earrings, sharp focused eyes | brass gold (#D9A441) |
| **Sam** (the spare chef) | young cook, short bleached blond undercut, light skin, sleepy half-lidded eyes, relaxed playful grin, a pencil tucked behind one ear | teal (#4FB6A8) |

---

## 2. The waiter (the producer)

**Look:** elegant older Prague café waiter, tall and slim, slicked-back silver hair, a big curled handlebar moustache, bright blue eyes, black waistcoat, white shirt with rolled sleeves, tomato-red bow tie, long black waist apron, white cloth over one forearm.

**`waiter_sheet.png`**
```
Character reference sheet of an original anime character, "Henrik the waiter". Elegant older Prague café waiter, tall and slim, slicked-back silver hair, a big curled handlebar moustache, bright blue eyes, black waistcoat, white shirt with rolled sleeves, tomato-red bow tie, long black waist apron, white cloth over one forearm. Show full body front view, three-quarter view and back view, plus four small head close-ups: polite smile, proud, alarmed, winking. STYLE: modern Japanese anime illustration, clean confident line art in dark brown ink, two-tone cel shading, soft warm rim light, polished anime key-visual quality. Transparent background, no scenery, no text labels, no watermark.
```

**`waiter_bust.png`**
```
Same character as the reference sheet. Chest-up bust of Henrik the waiter, three-quarter view facing right, one hand raised holding a silver cloche on a tray, proud smile, moustache curled, dramatic anime cut-in pose. STYLE: modern Japanese anime illustration, clean line art, two-tone cel shading, strong rim light. Character only, transparent background, no text, no watermark.
```

**`waiter_chibi_walk.png`**
```
Same character as the reference sheet. Chibi Henrik the waiter, about 2.5 heads tall, walking briskly carrying a plated dish on a tray held high, cloth over his arm, full body, side three-quarter view facing right. CHIBI STYLE: thick clean outline, simple two-tone cel shading, game sprite, centred, transparent background, no ground shadow, no text.
```

**`waiter_chibi_dash.png`**
```
Same character as the reference sheet. Chibi Henrik the waiter, about 2.5 heads tall, sprinting dramatically to the right in an action pose, tray held perfectly level, moustache flying, determined face, full body. CHIBI STYLE: thick clean outline, simple two-tone cel shading, game sprite, centred, transparent background, no ground shadow, no speed lines, no text.
```

---

## 3. The auditor (a second consumer group)

**Look:** sharp young detective-style woman, short wavy dark-red hair, green eyes, tan trench coat, a round **blue** clip pinned to her lapel, holding a clipboard and a magnifying glass, sly confident smirk.

**`auditor_sheet.png`**
```
Character reference sheet of an original anime character, "The Auditor". Sharp young detective-style woman, short wavy dark-red hair, green eyes, tan trench coat, a round blue clip pinned to her lapel, holding a clipboard and a magnifying glass, sly confident smirk. Show full body front, three-quarter and back views, plus four head close-ups: smirk, suspicious squint, surprised, satisfied. STYLE: modern Japanese anime illustration, clean confident line art in dark brown ink, two-tone cel shading, soft warm rim light. Transparent background, no text labels, no watermark.
```

**`auditor_chibi.png`**
```
Same character as the reference sheet. Chibi Auditor, about 2.5 heads tall, peering through her magnifying glass while writing on her clipboard, full body, three-quarter view. CHIBI STYLE: thick clean outline, simple two-tone cel shading, game sprite, centred, transparent background, no ground shadow, no text.
```

---

## 4. The diners

Diners only need chibi sprites, seated as if at a table, in four moods. Make the **happy** one first, then attach it and ask for the other three moods.

| Diner | Look |
|---|---|
| `diner1` | teenager with messy bright red hair, freckles, oversized yellow hoodie |
| `diner2` | sweet grandmother with a silver bun, round glasses, pearl necklace, lilac cardigan |
| `diner3` | big bearded man, brown beard, red flannel shirt |
| `diner4` | young woman with dark curly hair, warm brown skin, green knit sweater, hoop earrings |

**`diner1_happy.png`** (then `_waiting`, `_upset`, `_angry`)
```
Original anime character, chibi / super-deformed, about 2.5 heads tall: a teenager with messy bright red hair, freckles, oversized yellow hoodie. Seated, upper body visible above a table edge, holding a fork. Mood: [happy: eating with delight, sparkles, rosy cheeks] / [waiting: patient, looking around, chin on hand] / [upset: frowning, tapping fork, a sweat drop] / [angry: furious red face, steam puffing from head, an anime anger vein mark]. CHIBI STYLE: thick clean outline, simple two-tone cel shading, modern anime, game sprite, centred, transparent background, no table drawn, no text.
```

---

## 5. The dishes (square 1:1, one per image)

Make `food_pizza.png` first. For each next dish, attach the pizza and say *"same style as attached"*.

```
A single [DISH] on a round white plate with a thin brass rim, three-quarter top-down view, anime food illustration in the style of cooking anime: glossy, juicy, exaggerated highlights, small sparkles and a little steam, clean dark brown line art, two-tone cel shading, vibrant warm colours. Centred, transparent background, no table, no text, no watermark.
```

| File | [DISH] |
|---|---|
| `food_pizza.png` | margherita pizza with pepperoni and basil |
| `food_steak.png` | sliced grilled steak with herb butter |
| `food_pasta.png` | spaghetti with tomato sauce and basil |
| `food_paella.png` | seafood paella in a small black pan |
| `food_burger.png` | tall cheeseburger with lettuce, tomato and a sesame bun |
| `food_cake.png` | slice of strawberry shortcake |
| `food_cupcake.png` | cupcake with pink frosting and a cherry |
| `food_flan.png` | Japanese caramel custard pudding (purin) |
| `food_sundae.png` | ice cream sundae in a glass with a wafer |

---

## What I do with them

- **Cleanup:** cut out backgrounds, trim, and normalise sizes so every chibi stands on the same baseline.
- **Kitchen scene:** chibis replace the emoji. Each chef keeps their team colour, which matches their rail.
- **Manga cut-ins:** the busts go in the "ORDER UP!" / "SERVED!" panels with speed lines, screentone and katakana sound effects.
- **Food:** the dishes replace the food emoji on tickets and plates.

The manga effects themselves (impact frames, speed lines, sound-effect lettering) are drawn in code, so you don't need to generate those.
