"""
Quantus Miner on Modal.com — Serverless H100 Mining (Kryptex Pool)
Deploy: modal deploy quantus_modal.py
Run:    modal run quantus_modal.py
"""

import modal

app = modal.App("quantus-miner")

WALLET = "qzodqEtdBhugS8bVkDjsxcUToZ44ibTsFaeA1985QjTx4XfGe"
WORKER = "modal-h100"
GPU = "H100"
TIMEOUT = 86400

quantus_image = (
    modal.Image.from_registry(
        "registry.kryptex.network/quantus-miner:latest",
        add_python="3.11",
    )
    .dockerfile_commands([
        "ENTRYPOINT []",
        "CMD []",
    ])
)


@app.function(
    gpu=GPU,
    image=quantus_image,
    timeout=TIMEOUT,
    scaledown_window=300,
)
def mine():
    import subprocess
    import os

    # Konfigurasi environment untuk pool.kryptex.com dan coin Quantus
    os.environ["POOL_WALLET"]      = WALLET
    os.environ["POOL_WORKER"]      = WORKER
    os.environ["POOL_HOST"]        = "pool.kryptex.com"
    os.environ["POOL_PORT"]        = "7777"
    os.environ["POOL_USE_TLS"]     = "1"
    os.environ["GPU_INDICES"]      = "all"
    os.environ["METRICS_PORT"]     = "9100"

    # Seleksi kernel GPU otomatis
    cc = subprocess.run(
        ["nvidia-smi", "--query-gpu=compute_cap", "--format=csv,noheader"],
        capture_output=True, text=True
    ).stdout.strip().split("\n")[0]
    major, minor = cc.split(".")
    print(f"[Modal] GPU compute: {major}.{minor}")

    os.makedirs("/var/lib/quantus-miner", exist_ok=True)
    
    # Jalankan miner dengan parameter wallet Anda
    os.execv("/app/quantus-miner", ["/app/quantus-miner", "--wallet", WALLET, "--pool", "pool.kryptex.com:7777"])


@app.local_entrypoint()
def main():
    mine.remote()
