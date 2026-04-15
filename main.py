
import os, hashlib

print("Running system")

# =========================
# LARGE FILES
# =========================
print("\n=== LARGE FILES ===")
for root, dirs, files in os.walk("."):
    for f in files:
        fp=os.path.join(root,f)
        try:
            if os.path.getsize(fp) > 10*1024*1024:
                print("LARGE:", fp)
        except:
            pass

# =========================
# DUPLICATES
# =========================
print("\n=== DUPLICATES ===")
hashes = {}
for root, dirs, files in os.walk("."):
    for f in files:
        fp=os.path.join(root,f)
        try:
            h=hashlib.md5(open(fp,'rb').read(1024)).hexdigest()
            if h in hashes:
                print("DUPLICATE:", fp)
            else:
                hashes[h]=fp
        except:
            pass

# =========================
# DATASETS
# =========================
print("\n=== DATASETS ===")
for root, dirs, files in os.walk("."):
    for f in files:
        if f.endswith(".csv") or f.endswith(".json"):
            print("DATA:", os.path.join(root,f))

# =========================
# ERROR LOGS
# =========================
print("\n=== ERROR LOGS ===")
for root, dirs, files in os.walk("."):
    for f in files:
        if f.endswith(".log"):
            try:
                content=open(os.path.join(root,f),errors="ignore").read(300).lower()
                if "error" in content:
                    print("ERROR LOG:", f)
            except:
                pass

# =========================
# UI FILES
# =========================
print("\n=== UI FILES ===")
for root, dirs, files in os.walk("."):
    for f in files:
        if f.endswith(".html"):
            print("UI:", os.path.join(root,f))
