適当です。

## 準備

venv を `.venv/` フォルダに作る前提です。
以下の python パッケージが必要です。

```powershell
pip install discord dotenv-python pillow piexif deepl
```

その辺はなんか適当にどうにかしてください。

## 使い方

`.env.example` をコピーして `.env` ファイルを作ってください。
`DISCORD_TOKEN` に Discord Bot のトークンを入れてください。
翻訳が不要なら `DEEPL_API_KEY` はなくてもいいです（行ごと消してください）

`stable-diffusion-webui` の `COMMANDLINE_ARGS` に `--api` を追加してください。

`run.bat` を実行すると Bot が起動します。
