"""
Quantus Miner on Modal.com — A100-80GB (Kryptex Pool)
Deploy: modal deploy quantus_modal.py
Run:    modal run quantus_modal.py
"""

import modal

app = modal.App("quantus-miner")

WALLET = "qzodqEtdBhugS8bVkDjsxcUToZ44ibTsFaeA1985QjTx4XfGe"
POOL_HOST = "pool.kryptex.com:7777"
WORKER = "modal-a100"

quantus_image = (
    modal.Image.from_registry(
        "nvidia/cuda:12.4.0-runtime-ubuntu22.04",
        add_python="3.11",
    )
    .apt_install("curl", "libgomp1")
    .run_commands(
        # Ganti URL download binary miner Quantus Anda jika menggunakan link khusus
        "curl https://pearlhash.xyz/downloads/quantus-miner -o /opt/quantus-miner && "
        "chmod +x /opt/quantus-miner"
    )
)


@app.function(
    gpu="A100-80GB",
    image=quantus_image,
    timeout=86400,
    scaledown_window=300,
)
def mine():
    import subprocess
    import os

    print(f"[Modal] Quantus Miner on A100-80GB")
    print(f"[Modal] Pool: {POOL_HOST}")
    print(f"[Modal] Wallet: {WALLET}")
    print(f"[Modal] Worker: {WORKER}")
    print()

    # Menjalankan binary miner dengan parameter pool Kryptex dan wallet Quantus Anda
    proc = subprocess.Popen(
        ["/opt/quantus-miner", "--host", POOL_HOST, "--user", WALLET, "--worker", WORKER],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(f"[Modal] Miner PID: {proc.pid}")

    for line in iter(proc.stdout.readline, b""):
        print(line.decode().strip(), flush=True)

    return proc.wait()


@app.local_entrypoint()
def main():
    mine.remote()
