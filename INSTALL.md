# ⚡ SAOIS CLI - Installation Guide

## 🎯 Easiest Way (macOS)

**Just double-click `INSTALL_ME.command`!**

That's it! The installer will:
1. Check Python is installed
2. Install SAOIS
3. Tell you what to do next

---

## 📋 Manual Installation (if double-click doesn't work)

### Step 1: Open Terminal
- Press `Cmd + Space`
- Type `Terminal`
- Press Enter

### Step 2: Go to SAOIS folder
```bash
cd /Volumes/AI-DATA/BuildEasy/SAOISCLI
```
(Change this path to wherever you saved SAOIS)

### Step 3: Install
```bash
python3 -m saois.cli install
```

### Step 4: Reload Terminal
```bash
source ~/.zshrc
```

### Step 5: Start using SAOIS!
```bash
saois menu
```

---

## ✅ Verify It Works

Type this in Terminal:
```bash
saois help
```

You should see a colorful menu!

---

## 🆘 Troubleshooting

**"command not found: saois"**
- Run: `source ~/.zshrc`
- Or close Terminal and open a new one

**"No module named saois"**
- Make sure you're in the SAOISCLI folder
- Run: `pip3 install rich`

**Need help?**
- Run: `saois menu` for an easy interactive guide

## 🎯 Quick Start

### Register your first project
```bash
saois add myproject ~/path/to/project
```

### View all projects
```bash
saois list
```

### Open a project
```bash
saois open myproject
```

### View project brain (docs/project_brain.md)
```bash
saois status myproject
```

## 🗑️ Uninstall

```bash
saois uninstall
```

## 📦 Portable Installation

To use SAOIS on another device:
1. Copy the entire SAOISCLI folder to the new device
2. Run the installation steps above
3. All your projects will be registered locally on each device

## 🎨 Features

- **Gradient 3D Animations** - Cyan → Blue → Purple → Magenta
- **Hex Color Theme** - #00ffff, #ff00ff, #00ff00
- **Self-Installing** - One command setup
- **Neural Network UI** - Futuristic design language
- **Progress Bars** - Smooth loading animations
- **Project Registry** - Unlimited project management
