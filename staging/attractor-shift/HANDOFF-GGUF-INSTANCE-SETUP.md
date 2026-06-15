# Handoff: Vast Instance Setup and GGUF Download

This handoff is for a Codex agent taking over a fresh Vast.ai GPU instance and preparing it to download a GGUF model file from Hugging Face.

## Goal

Set up a rented Vast.ai box cleanly, stop any template process using VRAM, authenticate to Hugging Face without printing secrets, and download a known GGUF file into `/workspace/models/...`.

## Working Rules

- Use the Vast direct SSH endpoint from `vastai ssh-url` or the local wrapper. Do not guess ports from the UI.
- Do not use `apt` unless absolutely necessary. It has repeatedly stalled on fresh images.
- Do not print `HF_TOKEN`.
- Store the token on the box as `/workspace/.hf_token` with restrictive permissions.
- For a single GGUF file, `hf download <repo> <filename> --local-dir <dir>` works.
- Use `HF_XET_HIGH_PERFORMANCE=1`. The old `HF_HUB_ENABLE_HF_TRANSFER` path is deprecated.
- Prefer `/workspace` for models, cache, logs, and scripts.

## Local Inputs

Known local token source:

```bash
/Volumes/ExternalSSD/sae-tests/.env
```

Read it silently:

```bash
TOKEN="$(grep -E '^HF_TOKEN=' /Volumes/ExternalSSD/sae-tests/.env | cut -d= -f2- | tr -d '\"')"
test -n "$TOKEN"
```

## Resolve Vast Connection

Use the local Vast wrapper if available:

```bash
python3 ~/.codex/skills/vastai-cli-operator/scripts/run_vast.py show instances --raw
python3 ~/.codex/skills/vastai-cli-operator/scripts/run_vast.py ssh-url INSTANCE_ID
python3 ~/.codex/skills/vastai-cli-operator/scripts/run_vast.py scp-url INSTANCE_ID
```

Example output format:

```text
ssh://root@79.117.54.182:20563
scp://root@79.117.54.182:20563
```

Use the direct SSH endpoint:

```bash
ssh -i ~/.ssh/vast_gptoss_sl -o IdentitiesOnly=yes -p PORT root@HOST
```

## Preflight The Box

Run:

```bash
ssh -i ~/.ssh/vast_gptoss_sl -o IdentitiesOnly=yes -p PORT root@HOST '
set -euo pipefail
python3 --version
df -h /workspace
nvidia-smi
supervisorctl status || true
'
```

If the instance is a Llama.cpp template, it may start `llama-server` automatically and consume VRAM. Stop it:

```bash
ssh -i ~/.ssh/vast_gptoss_sl -o IdentitiesOnly=yes -p PORT root@HOST '
set -euo pipefail
supervisorctl stop llama || true
pkill -f "llama-server" || true
sleep 2
supervisorctl status llama || true
nvidia-smi
'
```

Expected clear GPU state is roughly:

```text
Memory-Usage: 2MiB / 97887MiB
No running processes found
```

## Push Hugging Face Token To Remote

Do not echo the token.

```bash
TOKEN="$(grep -E '^HF_TOKEN=' /Volumes/ExternalSSD/sae-tests/.env | cut -d= -f2- | tr -d '\"')"
printf '%s' "$TOKEN" | ssh -i ~/.ssh/vast_gptoss_sl -o IdentitiesOnly=yes -p PORT root@HOST \
  'umask 077; cat > /workspace/.hf_token; chmod 600 /workspace/.hf_token'
```

Verify only presence and length:

```bash
ssh -i ~/.ssh/vast_gptoss_sl -o IdentitiesOnly=yes -p PORT root@HOST \
  'test -s /workspace/.hf_token && wc -c /workspace/.hf_token'
```

## Install Minimal Hugging Face Stack

No `apt`.

```bash
ssh -i ~/.ssh/vast_gptoss_sl -o IdentitiesOnly=yes -p PORT root@HOST '
set -euo pipefail
python3 -m venv /workspace/venv
/workspace/venv/bin/python -m pip install -U pip wheel setuptools
/workspace/venv/bin/python -m pip install -U "huggingface_hub[cli]" hf-xet hf_transfer
/workspace/venv/bin/python - <<'"'"'PY'"'"'
import huggingface_hub
print("huggingface_hub", huggingface_hub.__version__)
PY
'
```

## Authenticate

```bash
ssh -i ~/.ssh/vast_gptoss_sl -o IdentitiesOnly=yes -p PORT root@HOST '
set -euo pipefail
export HF_HOME=/workspace/.hf_home
export HF_TOKEN="$(cat /workspace/.hf_token)"
export HF_XET_HIGH_PERFORMANCE=1
/workspace/venv/bin/hf auth whoami || /workspace/venv/bin/hf auth login --token "$HF_TOKEN"
'
```

## Download Known GGUF Files

Base Qwen 35B Q8 GGUF:

```bash
ssh -i ~/.ssh/vast_gptoss_sl -o IdentitiesOnly=yes -p PORT root@HOST '
set -euo pipefail
export HF_HOME=/workspace/.hf_home
export HF_TOKEN="$(cat /workspace/.hf_token)"
export HF_XET_HIGH_PERFORMANCE=1
mkdir -p /workspace/models/qwen35-base-q8
/workspace/venv/bin/hf download unsloth/Qwen3.5-35B-A3B-GGUF \
  Qwen3.5-35B-A3B-Q8_0.gguf \
  --local-dir /workspace/models/qwen35-base-q8
'
```

HauhauCS aggressive Q8 GGUF:

```bash
ssh -i ~/.ssh/vast_gptoss_sl -o IdentitiesOnly=yes -p PORT root@HOST '
set -euo pipefail
export HF_HOME=/workspace/.hf_home
export HF_TOKEN="$(cat /workspace/.hf_token)"
export HF_XET_HIGH_PERFORMANCE=1
mkdir -p /workspace/models/qwen35-hauhau-q8
/workspace/venv/bin/hf download HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive \
  Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-Q8_0.gguf \
  --local-dir /workspace/models/qwen35-hauhau-q8
'
```

## Verify Download

```bash
ssh -i ~/.ssh/vast_gptoss_sl -o IdentitiesOnly=yes -p PORT root@HOST '
set -euo pipefail
find /workspace/models -maxdepth 3 -type f -name "*.gguf" -printf "%p %s bytes\n"
du -sh /workspace/models /workspace/.hf_home 2>/dev/null || true
sha256sum /workspace/models/*/*.gguf
df -h /workspace
'
```

Known prior sizes:

```text
Qwen3.5-35B-A3B-Q8_0.gguf                                      ~36,903,139,968 bytes
Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-Q8_0.gguf        ~36,903,139,392 bytes
```

## Common Failure Modes

- `llama-server` keeps coming back: stop `supervisorctl stop llama`, not just `pkill`.
- SSH proxy flakes: use `ssh-url` direct IP/port from Vast.
- Token missing on remote: create `/workspace/.hf_token` via stdin, never by pasting into logs.
- Download grabs only config files: for GGUF, pass the exact filename after the repo id.
- Long install hangs: do not start `apt`; use the existing `python3`.
- Disk fills unexpectedly: check `df -h /workspace` before download; Q8 GGUF is about 37 GB plus cache.

## Minimal One-Box Checklist

```text
1. Resolve INSTANCE_ID -> direct ssh-url.
2. SSH preflight: df, nvidia-smi, python3.
3. Stop llama template service if present.
4. Push /workspace/.hf_token.
5. Create /workspace/venv and install huggingface_hub[cli] + hf-xet.
6. Auth with HF_TOKEN.
7. hf download exact GGUF filename.
8. Verify file size, sha256, and free disk.
```
