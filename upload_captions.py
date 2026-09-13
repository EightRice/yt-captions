"""Upload subtitle files to a video on my own YouTube channel.

Personal tool. Runs from the command line on my machine, authenticates as me
(one-time OAuth consent), and uploads .srt files as caption tracks.

Setup:
    pip install google-api-python-client google-auth-oauthlib
    put the OAuth client file from Google Cloud Console next to this script as client_secret.json

Usage:
    python upload_captions.py VIDEO_ID captions/          # uploads every captions/<lang>.srt
    python upload_captions.py VIDEO_ID captions/ --dry    # list what would be uploaded
    python upload_captions.py VIDEO_ID --list             # show existing tracks

Language is taken from the file name (ro.srt, pt-BR.srt, zh-Hans.srt ...).
The token is cached in token.json; delete that file to revoke local access.
"""
import glob
import os
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

HERE = os.path.dirname(os.path.abspath(__file__))
CLIENT = os.path.join(HERE, "client_secret.json")
TOKEN = os.path.join(HERE, "token.json")
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
NAMES = {
    "de": "Deutsch", "en": "English", "es": "Español", "fr": "Français", "hi": "हिन्दी",
    "id": "Bahasa Indonesia", "it": "Italiano", "ja": "日本語", "ko": "한국어",
    "pt-BR": "Português (Brasil)", "ro": "Română", "ru": "Русский", "tr": "Türkçe",
    "zh-Hans": "中文 (简体)",
}


def creds():
    c = Credentials.from_authorized_user_file(TOKEN, SCOPES) if os.path.exists(TOKEN) else None
    if c and c.expired and c.refresh_token:
        c.refresh(Request())
    if not c or not c.valid:
        c = InstalledAppFlow.from_client_secrets_file(CLIENT, SCOPES).run_local_server(port=0)
        with open(TOKEN, "w") as f:
            f.write(c.to_json())
    return c


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    video_id = sys.argv[1]
    dry = "--dry" in sys.argv
    yt = build("youtube", "v3", credentials=creds())
    items = yt.captions().list(part="snippet", videoId=video_id).execute().get("items", [])
    have = {c["snippet"]["language"]: c["id"] for c in items}
    print("existing tracks:", ", ".join(sorted(have)) or "none")
    if "--list" in sys.argv or len(sys.argv) < 3:
        return
    for path in sorted(glob.glob(os.path.join(sys.argv[2], "*.srt"))):
        lang = os.path.splitext(os.path.basename(path))[0]
        if lang in have:
            print("skip (exists):", lang)
            continue
        print("upload:", lang, NAMES.get(lang, lang), os.path.getsize(path), "bytes")
        if dry:
            continue
        body = {"snippet": {"videoId": video_id, "language": lang,
                            "name": NAMES.get(lang, lang), "isDraft": False}}
        media = MediaFileUpload(path, mimetype="application/octet-stream")
        r = yt.captions().insert(part="snippet", body=body, media_body=media).execute()
        print("  ok", r["id"])


if __name__ == "__main__":
    main()
