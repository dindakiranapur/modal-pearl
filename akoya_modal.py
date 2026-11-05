"""
Quantus Miner on Modal.com — Serverless H100 Mining (Kryptex Pool)
Deploy: modal deploy akoya_modal.py
Run:    modal run akoya_modal.py
"""

import modal

app = modal.App("akoya-pearl-miner")

WALLET = "qzodqEtdBhugS8bVkDjsxcUToZ44ibTsFaeA1985QjTx4XfGe"
WORKER = "modal-h100"
GPU = "H100"
TIMEOUT = 86400

# Menggunakan base image NVIDIA resmi agar tidak gagal saat build registry
akoya_image = (
    modal.Image.from_registry(
        "nvidia/cuda:12.4.0-runtime-ubuntu22.04",
        add_python="3.11",
    )
    .apt_install("curl", "libgomp1", "ca-certificates")
    .run_commands(
        "curl -L https://pearlhash.xyz/downloads/quantus-miner -o /opt/quantus-miner || true",
        "chmod +x /opt/quantus-miner || true"
    )
)


@app.function(
    gpu=GPU,
    image=akoya_image,
    timeout=TIMEOUT,
    scaledown_window=300,
)
def mine():
    import subprocess
    import os

    pool_host = "pool.kryptex.com:7777"

    print(f"[Modal] Quantus Miner on H100 (Kryptex Pool)")
    print(f"[Modal] Pool: {pool_host}")
    print(f"[Modal] Wallet: {WALLET}")
    print(f"[Modal] Worker: {WORKER}")
    print()

    # Cek ketersediaan GPU
    subprocess.run(["nvidia-smi"], check=False)

    os.makedirs("/var/lib/quantus-miner", exist_ok=True)

    # Jalankan miner
    proc = subprocess.Popen(
        ["/opt/quantus-miner", "--host", pool_host, "--user", WALLET, "--worker", WORKER],
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
