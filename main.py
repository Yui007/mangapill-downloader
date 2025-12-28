#!/usr/bin/env python3
"""
Mangapill Downloader - Beautiful Interactive CLI
================================================

A modern, feature-rich CLI tool for downloading manga from Mangapill.com

Features:
- 📥 Download single, range, or all chapters
- 🖼️ Output as Images, PDF, or CBZ
- 🔄 Automatic retry with exponential backoff
- ⚡ Concurrent downloads with threading
- 📖 ComicInfo.xml metadata for CBZ files

Usage:
    python main.py download              # Interactive mode
    python main.py download URL          # Download from URL
    python main.py download URL -c 1-10  # Download chapters 1-10
    python main.py settings              # View/modify settings
    python main.py info URL              # Show manga info
"""

from src.cli.app import run

if __name__ == "__main__":
    run()
