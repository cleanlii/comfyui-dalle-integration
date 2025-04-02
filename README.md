
# DalleImageNodes - ComfyUI OpenAI DALL·E 自定义节点插件

## 📌 简介 | Introduction | 紹介

**DalleImageNodes** 是适用于 [ComfyUI](https://github.com/comfyanonymous/ComfyUI) 的自定义节点插件，基于 OpenAI 官方 API 实现 **DALL·E 3 图像生成、编辑和变体功能**，支持 OpenAI SDK v1.x，自动处理图像尺寸和格式。

This is a **custom node plugin for ComfyUI**, using OpenAI's latest DALL·E 3 image generation APIs (via SDK v1.x), supporting image generation, inpainting (edit), and variation. It includes automatic resizing and format compatibility.

OpenAIの DALL·E 3 API を利用して、画像生成・編集・バリエーションを可能にする ComfyUI 用のカスタムノードです。OpenAI SDK v1.xに対応し、自動でサイズや形式も調整されます。

---

## 🖼️ 功能截图 | Screenshots | スクリーンショット

### 🧠 图像生成 | Image Generation | 画像生成
![generation-screenshot](./screenshots/generation.png)

### 🎨 图像编辑 | Image Editing | 画像編集
![edit-screenshot](./screenshots/edit.png)

### 🔁 图像变体 | Image Variation | バリエーション
![variation-screenshot](./screenshots/variation.png)

### 🔁 图像变体 | Image Variation | バリエーション
![variation-screenshot](./screenshots/variation.png)

---

## 📦 安装方式 | Installation | インストール

将 `DalleImageNodes_async_final.py` 文件复制到您的 `ComfyUI/custom_nodes/任意文件夹/` 目录下。

Copy `DalleImageNodes_async_final.py` into any folder under your `ComfyUI/custom_nodes/` directory.

`DalleImageNodes_async_final.py` を `ComfyUI/custom_nodes/任意のフォルダ/` に配置してください。

---

## 🛠️ 配置 OpenAI 密钥 | Configure API Key | APIキーの設定

请在同一目录下创建 `config.json`，内容如下：

Create a `config.json` in the same folder as the node file:

ノードと同じフォルダに `config.json` を作成してください：

```json
{
  "openAI_API_Key": "your-api-key"
}
```

---

## ✅ 支持功能 | Features | 機能一覧

- ✅ DALL·E 3 图像生成 / Image Generation / 画像生成
- ✅ 图像编辑（Inpainting）/ Editing / 編集
- ✅ 图像变体（Variation）/ Variation / バリエーション
- ✅ 自动转换为 RGBA + 固定尺寸
- ✅ 支持批量生成 + seed 输入
- ✅ 完全兼容 OpenAI Python SDK v1+

---

## 📄 License

MIT License.
