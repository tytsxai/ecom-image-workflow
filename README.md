---
title: 电商商品图片生成工作流（Phase 1：图片）
topic: AI 驱动的商品图片再创作工作流文档库入口
tags:
  - 主题/AI与智能体
  - 主题/电商
  - 形态/索引
  - 状态/进行中
summary: >
  面向网店的“供应商图→可商用、品牌化、明显不同但产品一致”的图片资产生成项目（Phase 1：图片）的文档入口、规范与交付清单。
created: 2025-12-22
updated: 2025-12-26
stage: draft
visibility: public
owner: me
ai_include: true
source: ""
---

# 电商商品图片生成工作流（Phase 1：图片）

## What this is (Open Source)
This repository documents an e-commerce product image re-composition workflow (Phase 1: images) and provides a small, runnable Python MVP that generates per-product “prompt + text sources + manifest” packages.

Not included (yet): the actual image generation pipeline (product segmentation, background rebuild/compositing, OCR, deterministic text rendering, etc.). Those parts are described in the docs (starting from `03-工作流方案-端到端.md`).

## MVP CLI (Python)
Generate a per-product package from a CSV:

```bash
python3 -m mvp_image_workflow generate \
  --input examples/products_minimum.csv \
  --out out_mvp \
  --batch-id 2025-12-26A
```

Validate generated packages:

```bash
python3 -m mvp_image_workflow validate --out out_mvp
```

Validate and also require expected `.png` files to exist:

```bash
python3 -m mvp_image_workflow validate --out out_mvp --require-images
```

## Repository layout
- Docs (workflow/specs/QC/compliance): `*.md` in the repository root.
- MVP packager (Python): `mvp_image_workflow/`
- Example input CSV: `examples/products_minimum.csv`
- Minimal tests: `tests/`

## Open source
- License: see `LICENSE`
- Contributing: see `CONTRIBUTING.md`
- Code of Conduct: see `CODE_OF_CONDUCT.md`

## 快速开始（经理视角）
- 一页操作卡：[14-经理一键生成-操作卡片.md](14-经理一键生成-操作卡片.md)
- 先看：[00-项目概览.md](00-项目概览.md)
- 再看：[07-经理操作手册-EN.md](07-经理操作手册-EN.md) / [08-经理操作手册-RU.md](08-经理操作手册-RU.md)
- 填表：[09-输入采集表单-经理填写.md](09-输入采集表单-经理填写.md)
- 默认配置（推荐）：[16-默认配置-一键生成.md](16-默认配置-一键生成.md)

## 需求与规范
- [01-需求与范围-Phase1图片.md](01-需求与范围-Phase1图片.md)
- [02-输出清单与版式规范.md](02-输出清单与版式规范.md)
- [05-质检与验收清单.md](05-质检与验收清单.md)

## 方案与模板
- [03-工作流方案-端到端.md](03-工作流方案-端到端.md)
- [04-模板-规格图与说明图.md](04-模板-规格图与说明图.md)
- [06-风险与合规.md](06-风险与合规.md)

## 资料与配置
- [10-样例集与素材索引.md](10-样例集与素材索引.md)
- [11-风格包-StylePacks.md](11-风格包-StylePacks.md)
- [12-经理指令模板-EN-RU.md](12-经理指令模板-EN-RU.md)
- [13-版本与变更记录.md](13-版本与变更记录.md)
- [AGENTS.md](AGENTS.md)
- [15-常见问题与退回处理.md](15-常见问题与退回处理.md)
- [17-供应商图最小要求.md](17-供应商图最小要求.md)
- [18-导出与交付-经理版.md](18-导出与交付-经理版.md)
- [19-生成批次记录-经理填写.md](19-生成批次记录-经理填写.md)

## 约定
- 所有生成图上的文案必须为英文；经理输入指令可为英文或俄语。
- 不删除既有内容；变更路径/导航需同步更新入口 README 与内部链接。
