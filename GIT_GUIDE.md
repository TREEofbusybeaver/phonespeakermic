# How to Use Git with This Project

## What is .gitignore?

The `.gitignore` file tells Git which files to **ignore** (not track). This prevents unnecessary files like:
- Build files
- Temporary files
- IDE configuration files
- Compiled code
from cluttering your repository.

## Quick Git Setup (5 minutes)

### 1. Install Git
- **Windows**: Download from https://git-scm.com/download/win
- **Mac**: Already installed, or use `brew install git`
- **Linux**: `sudo apt-get install git`

### 2. Initialize Git in Your Project

```bash
# Navigate to your project folder
cd PhoneSpeakerMic

# Initialize Git repository
git init

# The .gitignore file is already there - it will work automatically!
```

### 3. Make Your First Commit

```bash
# Add all files (gitignore will exclude the unwanted ones)
git add .

# Commit with a message
git commit -m "Initial commit - Phone Speaker Mic app"
```

**That's it!** Git is now tracking your project.

## Common Git Commands You'll Use

### Daily Workflow:

```bash
# Check what files changed
git status

# Add files to staging
git add .                    # Add all files
git add MainActivity.java    # Add specific file

# Commit your changes
git commit -m "Fixed audio bug"

# View commit history
git log
```

### Connecting to GitHub (Optional):

```bash
# Create a repository on GitHub first, then:
git remote add origin https://github.com/yourusername/PhoneSpeakerMic.git
git branch -M main
git push -u origin main
```

## What Gets Ignored?

With the provided `.gitignore`, these files **won't** be tracked:

❌ **Build outputs**: `build/`, `*.apk`, `*.class`
❌ **IDE files**: `.idea/`, `*.iml`
❌ **OS files**: `.DS_Store`, `Thumbs.db`
❌ **Python cache**: `__pycache__/`, `*.pyc`
❌ **Temporary**: `*.tmp`, `*.log`

✅ **What WILL be tracked**:
- Source code (`.java`, `.py`)
- Resources (`.xml`, drawables)
- Documentation (`.md`)
- Build configs (`build.gradle`, `settings.gradle`)

## Useful Tips

### Check if a file is ignored:
```bash
git check-ignore -v path/to/file
```

### Temporarily see all files (including ignored):
```bash
git status --ignored
```

### If you accidentally committed files that should be ignored:
```bash
# Remove from Git but keep locally
git rm --cached filename

# Or for a folder
git rm -r --cached foldername/

# Then commit
git commit -m "Removed ignored files"
```

## Branching (For Features)

```bash
# Create a new branch for a feature
git checkout -b new-feature

# Make changes, commit them
git add .
git commit -m "Added new feature"

# Switch back to main
git checkout main

# Merge your feature
git merge new-feature
```

## Example Workflow

```bash
# Day 1: Start project
git init
git add .
git commit -m "Initial commit"

# Day 2: Made changes
git status                    # See what changed
git add MainActivity.java     # Stage specific file
git commit -m "Improved audio quality"

# Day 3: Bug fix
git add .
git commit -m "Fixed connection bug"

# Push to GitHub
git push origin main
```

## Why Use Git?

✅ **Track changes**: See what you changed and when
✅ **Undo mistakes**: Revert to previous versions
✅ **Backup**: Your code is safe on GitHub
✅ **Collaboration**: Work with others easily
✅ **Branching**: Try new features without breaking main code

## Quick Reference Card

```bash
# Setup
git init                      # Start Git in folder
git clone <url>               # Download from GitHub

# Basic commands
git status                    # See changes
git add .                     # Stage all files
git commit -m "message"       # Save changes
git log                       # View history

# Remote (GitHub)
git remote add origin <url>   # Connect to GitHub
git push origin main          # Upload to GitHub
git pull origin main          # Download from GitHub

# Branches
git branch                    # List branches
git checkout -b new-branch    # Create & switch branch
git merge branch-name         # Merge branch
```

## Your .gitignore is Ready!

The `.gitignore` file is already created and configured for your project. Just start using Git:

```bash
cd PhoneSpeakerMic
git init
git add .
git commit -m "Initial commit"
```

Done! Git will automatically ignore all the files listed in `.gitignore`.

---

**Need more help?** Check out:
- Git basics: https://git-scm.com/book/en/v2/Getting-Started-Git-Basics
- GitHub guide: https://guides.github.com/activities/hello-world/
