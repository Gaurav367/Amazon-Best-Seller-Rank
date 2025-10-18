# 📊 Amazon Best Seller Rank (BSR) Tracker

**For Amazon Sellers, PPC Managers & E-commerce Professionals**

Track your product rankings automatically and get instant alerts when they drop - **NO CODING EXPERIENCE NEEDED!**

---

## 🎯 What Does This Tool Do?

- ✅ **Check Best Seller Rank** for 20+ products in 2 minutes
- ✅ **Export to CSV** for tracking rank changes over time
- ✅ **Simple Daily Workflow** - Check once, export, compare
- ✅ **100% Free** - No monthly subscriptions
- ✅ **Runs on Your Computer** - Your data stays private
- ✅ **No Coding Required** - Just follow the steps

---

## 🖥️ System Requirements

- **Windows 10/11** or **Mac OS**
- **Internet Connection**
- **10 minutes of setup time**

---

## 📥 STEP-BY-STEP SETUP GUIDE

### ⚠️ FOLLOW EVERY STEP EXACTLY - DON'T SKIP ANYTHING!

---

## STEP 1: Install Python (5 minutes)

### For Windows Users:

1. **Go to:** https://www.python.org/downloads/ and download PYTHON
2. **⚠️ CRITICAL:** Check the box that says **"Add Python to PATH"** (at the bottom)
3. Click **"Install Now"**
4. Wait for installation to complete

### ✅ Verify Python is Installed:

**Windows:** 
1. Press `Windows Key + R`
2. Type `cmd` and press Enter
3. Type `python --version` and press Enter
4. You should see: `Python your version you installed

## STEP 2: Download This Project (2 minutes)

### Download ZIP (Easier)

1. **Click the green "Code" button** on this page
2. **Click "Download ZIP"**
3. **Extract the ZIP file** to your Desktop
4. You should now have a folder called `amazon-bsr-tracker` on your Desktop

## STEP 3: Install Required Libraries (2 minutes)

### Windows:

1. **Press `Windows Key + R`**
2. **Type `cmd`** and press Enter
3. **Type this command** and press Enter:
   ```bash
   cd Desktop\amazon-bsr-tracker
   ```
4. **Copy and paste this** and press Enter:
   ```bash
   pip install flask requests beautifulsoup4 flask-cors
   ```
5. Wait for green "Successfully installed" messages


## STEP 4: Start the Tracker (1 minute)

### Windows:

1. **Make sure you're still in the Command Prompt** from Step 3
2. **Type this command** and press Enter:
   ```bash
   python tracker.py
   ```
3. You should see:
   ```
   🚀 Amazon Rank Tracker Server Starting...
   📡 Server running on http://localhost:5000
   ```
4. **✅ SUCCESS! Keep this window open!** (Minimizing is fine, but DON'T close it)
---

## STEP 5: Open the Tracker Interface

### For Bulk ASIN Checking:

1. **Go to the project folder**
2. **Double-click** the file named **`bulk-checker.html`**
3. It will open in your web browser
4. **✅ You're ready to check multiple ASINs!**

---

## 📖 HOW TO USE

### 📦 Daily Rank Checking Routine (RECOMMENDED)

**Every Morning (Takes 2 minutes):**

1. **Open `bulk-checker.html`** (double-click the file)

2. **Paste your ASINs** (one per line):
   ```
   B08N5WRWNW
   B07XJ8C8F5
   B09G9FPHY6
   ```

3. **Click "Check All Ranks"** and wait (3-5 seconds per ASIN)

4. **Click "Export CSV"** - Save as `ranks_oct_18_2024.csv`

5. **Compare with yesterday's file** in Excel:
   - Open both CSVs
   - See which ranks went up (worse) or down (better)

**That's it!** Simple daily routine. ✅

---


## 📊 UNDERSTANDING THE RESULTS

### Best Seller Rank (BSR) Explained:

- **Lower number = BETTER** 
  - Rank #100 is BETTER than #1,000
  - Rank #1 is the BEST possible
- **Higher number = WORSE**
  - If rank goes from #500 to #1,000, that's BAD (you dropped)
  - If rank goes from #1,000 to #500, that's GOOD (you improved)


## ❓ TROUBLESHOOTING

### Problem: "Command not found" when typing Python

**Solution:**
- Windows: You didn't check "Add Python to PATH" during installation
  - Uninstall Python
  - Reinstall and CHECK that box!
- Mac: Use `python3` instead of `python`

---

### Problem: "pip: command not found"

**Solution:**
- Windows: Use `py -m pip install` instead of `pip install`
- Mac: Use `pip3` instead of `pip`

---

### Problem: Server says "Address already in use"

**Solution:**
- Another program is using port 5000
- Close the existing Command Prompt/Terminal window
- Open a new one and start again

---

### Problem: Browser shows "Connection Refused"

**Solution:**
- The Python server isn't running
- Go back to Step 4 and start the server
- Keep that window open!

---

### Problem: "Rank Not Found" for all products

**Solution:**
- Some products don't have BSR (brand new products)
- Amazon might be blocking requests (check too frequently)
- Try waiting 5 minutes and checking again
- Increase check interval to 60 minutes

---

### Problem: CSV won't download

**Solution:**
- Check your Downloads folder (it's there!)
- Try a different browser (Chrome works best)
- Right-click Export button → "Save link as"

---

## 🔄 HOW TO STOP THE TRACKER

1. **Go to the Command Prompt/Terminal window** (where the server is running)
2. **Press `Ctrl + C`** (Windows) or **`Control + C`** (Mac)
3. **Close the window**

---

## ⚠️ IMPORTANT NOTES

### Amazon's Rules:
- ✅ Check every 30-60 minutes (SAFE)
- ❌ Don't check every 1-2 minutes (will get BLOCKED)
- ✅ Track 5-20 products (SAFE)
- ❌ Don't track 100+ products (will get BLOCKED)

### Best Practices:
- Check during business hours (Amazon's servers are more stable)
- Keep checking intervals at 30+ minutes
- Export your data regularly to CSV
- Don't leave the tracker running 24/7 (your computer needs breaks!)

---
