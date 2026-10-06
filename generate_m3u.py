import json
import subprocess
import sys

def get_stream_url(url):
    try:
        cmd = [
            sys.executable, "-m", "yt_dlp",
            "-g",
            "-f", "b/best",  # Verhindert getrennte Audio/Video-Links
            "--no-warnings",
            url
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and result.stdout.strip():
            lines = [l.strip() for l in result.stdout.strip().split("\n") if l.strip()]
            # Bevorzuge .m3u8 Stream-URLs, falls mehrere Zeilen ausgegeben werden
            m3u8_lines = [l for l in lines if ".m3u8" in l]
            return m3u8_lines[0] if m3u8_lines else lines[0]
    except Exception as e:
        print(f"Fehler bei {url}: {e}")
    return None

def main():
    with open("channels.json", "r", encoding="utf-8") as f:
        channels = json.load(f)

    m3u_lines = ["#EXTM3U"]
    success_count = 0

    for ch in channels:
        name = ch["name"]
        cat = ch.get("category", "General")
        tvg_id = ch.get("tvg_id", "")
        url = ch["url"]

        print(f"Lese Stream aus: {name} ({url})...")
        stream_url = get_stream_url(url)

        if stream_url:
            extinf = f'#EXTINF:-1 tvg-id="{tvg_id}" group-title="{cat}",{name}'
            m3u_lines.append(extinf)
            m3u_lines.append(stream_url)
            m3u_lines.append("")
            success_count += 1
            print("  -> ERFOLGREICH")
        else:
            print("  -> FEHLER: Stream konnte nicht extrahiert werden")

    # Schutz: Überschreibe die alte Datei nur, wenn mindestens ein Stream funktioniert hat
    if success_count > 0:
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(m3u_lines))
        print(f"Erfolg: {success_count} Sender in 'playlist.m3u' gespeichert.")
    else:
        print("WARNUNG: Keine Streams extrahiert. Alte 'playlist.m3u' bleibt unberührt.")

if __name__ == "__main__":
    main()
