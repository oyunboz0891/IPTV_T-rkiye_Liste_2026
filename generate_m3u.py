import json
import subprocess
import sys

def get_stream_url(url):
    try:
        cmd = [
            sys.executable, "-m", "yt_dlp",
            "-g",
            "--format", "best",
            "--no-warnings",
            url
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip().split("\n")[0]
    except Exception as e:
        print(f"Fehler bei {url}: {e}")
    return None

def main():
    with open("channels.json", "r", encoding="utf-8") as f:
        channels = json.load(f)

    m3u_lines = ["#EXTM3U\n"]

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
            print("  -> ERFOLGREICH")
        else:
            print("  -> FEHLER: Stream konnte nicht extrahiert werden")

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))

    print("Playlist 'playlist.m3u' wurde erfolgreich erstellt.")

if __name__ == "__main__":
    main()
