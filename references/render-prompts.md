# 逼真效果图生成手册（多模型通用）

把"改造后的样子"渲染出来，让用户一眼看到结果。

## 一、什么时候生成

- 用户明确想"一眼看到改造后长什么样"。
- 给方案配「改造前 → 改造后」同机位对比图。

## 二、模型选择：一条提示词，多平台可用

提示词分两层，一次写清、处处可用：

- **语义层（核心资产，平台无关）**：要改什么软装、什么风格、什么氛围、必须保持什么格局。写一遍，永久复用。
- **方言层（平台适配）**：把语义层翻译成各模型的语法（英文关键词堆叠 / 中文自然语言 / 正负面提示词 / 参数名）。

决策顺序：

1. **默认**：用环境里当前可用的图像生成工具直接出图（见第三节）。
2. **用户指定平台**（Midjourney、即梦、通义万相、可灵、SD 等）：不生成，改为**输出该平台可直接粘贴的完整提示词 + 参数建议**，让用户在自己 App 里出图。
3. **用户没指定但想对比**：给 1 份通用英文语义模板 + 按需转成 2–3 个平台的方言版。

## 三、内置生成工具（ImageGen）

- **每次生成约消耗 5–10 积分，生成前必须告知用户。**
- 两条路线：图生图（`prompt` + `image` 1–3 张，本地路径或 URL，`input_fidelity` 控相似度）；文生图（只 `prompt`）。
- 尺寸：竖构图 `1024x1536` 最贴房间，方形 `1024x1024` 通用。质量默认 high。

## 四、两条路线怎么选

### 路线 A：有照片 → 图生图（首选，最贴实际格局）

- 挑 1 张最能代表房间的照片做底图（「门口往里拍」或「对角全景」）。
- ImageGen 的 `input_fidelity` 从**中等**试起：软装没改到位就调高，格局被重画了就调低。
- 五段式 prompt（见第五节），第 2 段「保持格局」最要紧。

### 路线 B：无照片 → 文生图（风格示意）

- 必须声明："这是风格示意，不是你家实际格局。"
- 用第五节模板，填面积、朝向、风格。

## 五、语义层：五段式提示词模板

> 这是平台无关的核心。英文表述模型普遍更稳；中文模型（即梦/通义万相/文心一格/可灵）按第六节转译。

```
A photorealistic interior design rendering of a small rental bedroom in China.
KEEP the exact same room layout: same window position, same door, same wall, same floor, same ceiling height. Do NOT change the structure, do NOT add or remove windows or doors, do NOT change room dimensions.
RESTYLE into a warm [cream minimal] style.
CHANGE ONLY the soft furnishings: [cream washed-cotton bedding with linen pillows] / [2700K warm bedside lamp] / [beige short-pile rug] / [light-filtering curtains] / [a small potted plant on the windowsill] / [a photo wall above the desk]. Tidy up and hide all clutter.
MOOD: cozy, warm, lived-in, tidy, soft natural light, high-end interior magazine style.
CAMERA: shot at eye level, 24mm wide angle, realistic photography, high detail, natural color.
```

五段的职责：① 主体+逼真基调 ② **保持格局（最重要）** ③ 风格 ④ 具体改动（照抄采购清单大件） ⑤ 氛围+相机。
若原图有明确固定元素，补一句帮模型稳住格局：`white wall, beige floor tiles, 1.5m bed, wooden wardrobe`（照实写，不编）。

## 六、方言层：多平台适配表

| 平台 | 语言 | 提示词习惯 | 图生图关键参数 | 画幅/比例 | 负面提示词 | 备注 |
|---|---|---|---|---|---|---|
| **内置 ImageGen** | 中英皆可 | 自然语言段落 | `image` + `input_fidelity`（高=更像原图） | 1024x1536 | 一般不需要 | 本环境直接出图 |
| **Midjourney** | 英文 | 逗号分隔短语堆叠，主体→风格→参数 | 垫图链接 + `--iw 0.5–2`（高=更像原图） | `--ar 2:3` | `--no clutter, text, watermark, furniture-distortion` | `--style raw` 减少自带美化更真实 |
| **Stable Diffusion / SDXL / Flux** | 英文 | 标签式，逗号分隔 | img2img，`denoising 0.4–0.7`（低=更像原图） | 1024x1536 | 需要：`lowres, bad anatomy, blurry, watermark, text, deformed` | Flux 对自然语言长句更友好 |
| **即梦 / 豆包（字节）** | 中文 | 中文自然语言 | 图生图，相似度/参考强度滑杆 | 3:4 或 9:16 | 可加"不要文字、不要水印" | 中文用户最顺手 |
| **通义万相（阿里）** | 中文 | 中文自然语言 | 图生图 | 竖版 3:4 | 可加 | — |
| **文心一格（百度）** | 中文 | 中文自然语言 | 图生图 | 竖版 | 可加 | — |
| **可灵（快手）** | 中文 | 中文自然语言 | 图生图（参考图） | 3:4 | 可加 | 视频强，出图也稳 |
| **DALL·E 3** | 英文 | 自然语言长句 | 无公开图生图（可用 ChatGPT 内） | 1024x1536 | 一般不需要 | 长句细节理解强 |
| **ComfyUI / LiblibAI 等** | 英文 | 同 SD，正/负两段 | 同 SD | 视模型 | 同 SD | 底层是 SD/Flux |

**画幅换算**：竖构图 = MJ `--ar 2:3` ≈ SD/ImageGen `1024x1536` ≈ 各 App「3:4 或 9:16」。

## 七、各平台提示词示例（同一案例）

案例：8㎡ 朝北小次卧，改奶油风。语义层已定（第五节），下面是各平台方言版：

**Midjourney**
```
/imagine photorealistic interior of a small north-facing rental bedroom, cream minimal style, soft warm lighting --ar 2:3 --style raw --v 6
bed against solid wall, cream washed-cotton bedding, linen pillows, 2700K bedside lamp, beige short-pile rug, light-filtering curtains, small potted plant, tidy, cozy, lived-in, eye-level, 24mm, natural light, high detail --no clutter, text, watermark
```

**Stable Diffusion（正面 / 负面两段）**
```
正面: photorealistic interior, small north-facing bedroom, cream minimal, cream washed-cotton bedding, linen pillows, warm 2700K bedside lamp, beige rug, sheer light-filtering curtains, potted plant, tidy, cozy, soft natural light, eye level, 24mm wide angle, high detail
负面: lowres, bad anatomy, blurry, watermark, text, deformed, extra furniture, clutter, oversaturated
```

**即梦 / 通义万相 / 文心一格（中文，通用改写）**
```
照片级真实室内设计图：一间朝北的小合租卧室，奶油风，暖色灯光。
床靠实墙，床头不靠窗、不正对门；奶油色水洗棉床品配亚麻靠枕，2700K 暖光床头灯，米色短绒地毯，透光纱帘，窗台一盆绿植，书桌上方一面照片墙。整洁、温馨、有生活气息。
平视视角，24mm 广角，自然光，细节真实。保持房间原有格局与门窗位置不变，不要文字、不要水印。
```

## 八、风格关键词速查（配合 style-recipes.md）

| 风格 | 英文关键词 | 中文关键词 |
|---|---|---|
| 奶油风 | cream minimal, warm beige, soft textures, rounded shapes | 奶油风、米白、燕麦色、圆润、绒面 |
| 原木日式 | Japanese wabi-sabi, natural wood, linen, paper lamp | 原木、日式、棉麻、纸质灯 |
| 侘寂 / 新中式 | japandi, muted earth tones, raw ceramic, dried branches | 侘寂、新中式、粗陶、枯枝 |
| 工业复古 | industrial loft, exposed bulb, black metal, leather | 工业风、铁艺、爱迪生灯泡、皮质 |
| 北欧极简 | scandinavian, white, light wood, geometric pattern | 北欧、极简、白蜡木、几何 |
| 多巴胺 | colorful accents, playful, bright pops of color on neutral base | 多巴胺、撞色、活泼 |
| 暖调电竞 | warm gaming setup, wood desk, warm LED strips, dark gray | 暖调电竞、木桌、暖色灯带、深灰 |

## 九、注意事项（必读）

1. **效果图是"预期示意"不是"承诺"**：材质纹理、商品实样、尺寸比例都可能与实际有出入。
2. **图生图会"美化"现实**：旧墙可能被自动变新、杂物被抹掉、地板被换色。生成后主动跟用户说清。
3. **格局以 SVG 平面图为准**，效果图只负责"氛围和观感"，冲突时以平面图为准。
4. **积分透明**：用内置工具生成前告知消耗；多张批量前先 1 张确认方向。
5. **格局画错了就调**：内置工具降低 `input_fidelity`，或把「保持格局」挪到 prompt 最前加重措辞；MJ 调高 `--iw`，SD 调低 `denoising`。
6. **不同平台"图生图相似度"方向相反，别搞混**：ImageGen `input_fidelity` 和 MJ `--iw` 是「越高越像原图」，SD `denoising` 是「越高改动越大」。
