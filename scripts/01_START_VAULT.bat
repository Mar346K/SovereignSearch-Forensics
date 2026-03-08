@echo off
title Sovereign Search: Universal Engine
echo 🕵️ Detecting Hardware Acceleration...

:: Navigate to the project root (since script is in scripts/)
cd /d "%~dp0\.."

:: --- NVIDIA SUPPORT ---
set CUDA_VISIBLE_DEVICES=0

:: --- AMD SUPPORT ---
set HSA_OVERRIDE_GFX_VERSION=10.3.0
set ROCR_VISIBLE_DEVICES=0

:: --- INTEL SUPPORT (Pre-optimized for Arc A770 16GB) ---
set OLLAMA_NUM_GPU=999
set ZES_ENABLE_SYSMAN=1

:: Start the Vault
echo [*] Activating Virtual Environment...
call .venv\Scripts\activate

echo [*] Initializing Local GPU and booting RAG Engine...
start /b "" python -m streamlit run vault.py --server.headless true --server.port 8501

echo [*] Waiting for Streamlit Server to spin up...
timeout /t 10 /nobreak >nul
start http://localhost:8501
exit