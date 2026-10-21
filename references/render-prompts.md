# 逼真效果图生成手册

把"改造后的样子"渲染出来，让用户一眼看到结果。

## 一、什么时候生成

- 用户明确想"一眼看到改造后长什么样"。
- 给方案配「改造前 → 改造后」同机位对比图。

## 二、工具与成本

- 用图像生成工具（ImageGen）。
- **每次生成约消耗 5–10 积分，生成前必须告知用户。**
- 两条路线：
  - **图生图**：`prompt` + `image`（1–3 张，本地路径或 URL），用 `input_fidelity` 控制与原图相似度。
  - **文生图**：只给 `prompt`。
- 尺寸：竖构图 `1024x1536` 最贴房间（竖拍空间感强），方形 `1024x1024` 通用。
- 质量：默认 high。

## 三、两条路线怎么选

### 路线 A：有照片 → 图生图（首选，最贴实际格局）

- 从用户照片里挑 1 张最能代表房间的做底图（推荐「门口往里拍」或「对角全景」）。
- `input_fidelity` 从**中等**试起：软装没改到位就调高，格局被重画了就调低。太高改不动软装，太低连墙/窗一起重画。
- 固定五段式 prompt（见下），第 2 段「保持格局」最要紧。

### 路线 B：无照片 → 文生图（风格示意）

- 必须声明："这是风格示意，不是你家实际格局。"
- 用五段式文生图模板（见下），把面积、朝向、风格填进去。

## 四、提示词模板

### 图生图模板（英文更稳，复制后替换 [ ] 内容）

```
A photorealistic interior design rendering of a small rental bedroom in China.
KEEP the exact same room layout: same window position, same door, same wall, same floor, same ceiling height. Do NOT change the structure, do NOT add or remove windows or doors, do NOT change room dimensions.
RESTYLE into a warm [cream minimal] style.
CHANGE ONLY the soft furnishings: [cream washed-cotton bedding with linen pillows] / [2700K warm bedside lamp] / [beige short-pile rug] / [light-filtering curtains] / [a small potted plant on the windowsill] / [a photo wall above the desk]. Tidy up and hide all clutter.
MOOD: cozy, warm, lived-in, tidy, soft natural light, high-end interior magazine style.
CAMERA: shot at eye level, 24mm wide angle, realistic photography, high detail, natural color.
```

- 第 3 段风格词参考第六节速查表，从 `style-recipes.md` 选定的风格对应填。
- 第 4 段改动项直接照抄采购清单里的大件（床品/窗帘/地毯/灯光/绿植/装饰），别写墙、别写门窗。
- 若原图里有明确的固定元素，补一句帮模型稳住格局，例如 `white wall, beige floor tiles, 1.5m bed, wooden wardrobe`（照原图实际情况写，不编）。

### 文生图模板

```
A photorealistic interior design render of a [8sqm] small bedroom, [north-facing with soft daylight], [cream minimal] style.
Layout: bed against a solid wall, headboard not under the window and not facing the door; desk by the window facing the door; a cozy corner with a chair and a floor lamp; closed storage under the bed.
Warm 2700K lighting, cream bedding, beige rug, light curtains, a green plant, a small photo wall.
Realistic, eye-level, 24mm wide angle, natural light, high detail.
```

## 五、批次与视角

- 一次出 2–3 张：睡眠区 / 工作区 / 治愈角落；或「改造前→改造后」同机位对比。
- 同机位对比技巧：before 直接用用户原图，after 用同一张底图 + 同一个 prompt 只改软装，两张并排放。
- **先出 1 张让用户确认风格方向**，满意了再批量，省积分也省返工。

## 六、风格关键词速查（配合 style-recipes.md 使用）

| 风格 | 英文关键词 |
|---|---|
| 奶油风 | cream minimal, warm beige, soft textures, rounded shapes |
| 原木日式 | Japanese wabi-sabi, natural wood, linen, paper lamp |
| 侘寂 / 新中式 | japandi, muted earth tones, raw ceramic, dried branches |
| 工业复古 | industrial loft, exposed bulb, black metal, leather |
| 北欧极简 | scandinavian, white, light wood, geometric pattern |
| 多巴胺 | colorful accents, playful, bright pops of color on a neutral base |
| 暖调电竞 | warm gaming setup, wood desk, warm LED strips, dark gray |

## 七、注意事项（必读）

1. **效果图是"预期示意"不是"承诺"**：材质纹理、商品实样、尺寸比例都可能与实际有出入。
2. **图生图会"美化"现实**：旧墙面可能被自动变新、杂物被抹掉、地板被换色。生成后要主动跟用户说清，别让他以为"买同样东西就能 100% 复原这张图"。
3. **格局以 SVG 平面图为准**，效果图只负责"氛围和观感"，两者冲突时以平面图为准。
4. **积分透明**：生成前告知消耗；多张批量前先 1 张确认方向。
5. **格局画错了就调**：若窗/门位置被画歪，降低 `input_fidelity`，或把"KEEP the exact same room layout"挪到 prompt 最前面并加重措辞，再重试。
