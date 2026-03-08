# 🚀 SAOIS CLI - Quick Start Guide

## Installation (Choose One)

### ⚡ Fastest Way
```bash
cd /Volumes/AI-DATA/BuildEasy/SAOISCLI
./install.sh
source ~/.zshrc
saois list
```

### 🔧 Manual Way
```bash
cd /Volumes/AI-DATA/BuildEasy/SAOISCLI
pip3 install -e .
python3 -m saois.cli install
source ~/.zshrc
saois list
```

### 🧪 Try Without Installing
```bash
cd /Volumes/AI-DATA/BuildEasy/SAOISCLI
source activate.sh
saois list
```

## Common Tasks

### Add Your First Project
```bash
saois add myproject ~/path/to/project
```

### Import All Projects from a Folder
```bash
saois import
# Then enter: ~/projects
```

### View All Projects
```bash
saois list
```

### Open a Project
```bash
saois open myproject
```

### Remove a Project
```bash
saois remove myproject
```

## Features

✅ **Simple Commands** - No complex syntax
✅ **Bulk Import** - Add many projects at once
✅ **Clean UI** - Easy to read, colorful output
✅ **Smart Prompts** - Confirms before changes
✅ **Helpful Tips** - Guides you along the way

## Troubleshooting

**Command not found?**
```bash
source ~/.zshrc
```

**Still not working?**
```bash
python3 -m saois.cli list
```

**Want to start fresh?**
```bash
saois uninstall
./install.sh
source ~/.zshrc
```
