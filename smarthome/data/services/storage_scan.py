import subprocess, shutil, json, re
from datetime import datetime

def _kv_pairs_lsblk():
    try:
        out = subprocess.check_output(
            ["lsblk", "-P", "-o", "NAME,SIZE,MOUNTPOINT,FSTYPE"],
            text=True, stderr=subprocess.STDOUT
        )
    except Exception:
        return []
    rows = []
    for line in out.strip().splitlines():
        pairs = dict(re.findall(r'(\w+)="([^"]*)"', line))
        if not pairs:
            continue
        rows.append({
            "NAME": pairs.get("NAME", ""),
            "SIZE": pairs.get("SIZE", ""),
            "MOUNTPOINT": pairs.get("MOUNTPOINT", ""),
            "FSTYPE": pairs.get("FSTYPE", ""),
        })
    return rows

def _json_lsblk():
    try:
        out = subprocess.check_output(
            ["lsblk", "-J", "-o", "NAME,SIZE,MOUNTPOINT,FSTYPE"],
            text=True, stderr=subprocess.STDOUT
        )
        data = json.loads(out)
    except Exception:
        return []
    rows = []
    def walk(devs):
        for d in devs:
            rows.append({
                "NAME": d.get("name",""),
                "SIZE": d.get("size",""),
                "MOUNTPOINT": d.get("mountpoint") or "",
                "FSTYPE": d.get("fstype") or "",
            })
            if "children" in d and d["children"]:
                walk(d["children"])
    walk(data.get("blockdevices", []))
    return rows

def _list_lsblk():
    try:
        out = subprocess.check_output(
            ["lsblk", "-L", "-o", "NAME,SIZE,MOUNTPOINT,FSTYPE"],
            text=True, stderr=subprocess.STDOUT
        )
    except Exception:
        return []
    lines = [ln for ln in out.strip().splitlines() if ln.strip()]
    if not lines:
        return []
    headers = lines[0].split()
    rows = []
    for line in lines[1:]:
        parts = line.split(None, len(headers) - 1)
        if not parts: 
            continue
        row = dict(zip(headers, parts))
        for k in ("SIZE","MOUNTPOINT","FSTYPE"):
            if row.get(k) in ("-", None):
                row[k] = ""
        rows.append(row)
    return rows

def _fdisk_list():
    try:
        out = subprocess.check_output(["fdisk", "-l"], text=True, stderr=subprocess.STDOUT)
    except Exception:
        return []
    rows = []
    part_re = re.compile(r"^/dev/(\w+\d+)\s+(\d+(\.\d+)?[MGTP]?)", re.IGNORECASE)
    for line in out.splitlines():
        m = part_re.match(line.strip())
        if not m:
            continue
        name = m.group(1)
        size = m.group(2)
        rows.append({"NAME": name, "SIZE": size, "MOUNTPOINT": "", "FSTYPE": ""})
    return rows

def scan_storage_devices():
    rows = _json_lsblk() or _kv_pairs_lsblk() or _list_lsblk() or _fdisk_list()
    devices = []
    for r in rows:
        name = r.get("NAME", "")
        if not re.search(r"\d+$", name):  
            continue  # skip whole disks (sda, sdb, etc.)
        size = r.get("SIZE", "")
        mountpoint = r.get("MOUNTPOINT", "")
        fstype = r.get("FSTYPE", "")
        percent = 0.0
        if mountpoint:
            try:
                usage = shutil.disk_usage(mountpoint)
                percent = round(usage.used / usage.total * 100.0, 2)
            except Exception:
                pass
        devices.append({
            "name": name,
            "size": size,
            "mountpoint": mountpoint,
            "fstype": fstype,
            "percent_used": percent,
            "scanned_at": datetime.now(),
        })
    return devices
