# Modal Quantus Miner

Serverless Quantus mining on Modal.com (H100/A100) via Kryptex Pool.

## Quick Start

```bash
pip install modal
modal token set --token-id YOUR_ID --token-secret YOUR_SECRET

# Quantus Miner - Kryptex Pool (H100)
modal deploy quantus_h100_modal.py
nohup modal run quantus_h100_modal.py > quantus_h100.log 2>&1 &

# Quantus Miner - Kryptex Pool (A100)
modal deploy quantus_a100_modal.py
nohup modal run quantus_a100_modal.py > quantus_a100.log 2>&1 &
