"""Upload a video to my own YouTube channel.

Personal tool. Runs from the command line on my machine, authenticates as me
(same OAuth token as upload_captions.py), and uploads one video file with its
title, description, tags, visibility, optional thumbnail and optional subtitles.

Shorts: there is no separate API call. A vertical video up to 3 minutes long
is classified as a Short by YouTube automatically.

Usage:
    python upload_video.py FILE.mp4 --title "Title" [options]
    python upload_video.py --status VIDEO_ID

Options:
    --title TEXT              video title (required for upload)
    --description TEXT        description text
    --description-file PATH   read the description from a text file
    --tags a,b,c              comma-separated tags
    --privacy VALUE           public | unlisted | private (default: private)
    --thumbnail PATH          custom thumbnail (jpg/png)
    --captions DIR            upload every DIR/<lang>.srt as a subtitle track after the upload
    --category ID             YouTube category id (default 28, Science & Technology)
"""
import argparse
import os
import sys
import time

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from upload_captions import NAMES, creds


def show_status(yt, video_id):
    r = yt.videos().list(part="snippet,status,processingDetails,contentDetails", id=video_id).execute()
    if not r.get("items"):
        print("video not found:", video_id)
        return
    v = r["items"][0]
    s = v["status"]
    print("video id:     ", video_id)
    print("title:        ", v["snippet"]["title"])
    print("channel:      ", v["snippet"]["channelTitle"])
    print("visibility:   ", s.get("privacyStatus"))
    print("upload status:", s.get("uploadStatus"))
    print("processing:   ", v.get("processingDetails", {}).get("processingStatus", "n/a"))
    print("duration:     ", v.get("contentDetails", {}).get("duration", "n/a"))
    print("watch:         https://youtu.be/" + video_id)
    print("studio:        https://studio.youtube.com/video/" + video_id + "/edit")
    return s.get("privacyStatus")


def upload_captions(yt, video_id, folder):
    for name in sorted(os.listdir(folder)):
        if not name.endswith(".srt"):
            continue
        lang = name[:-4]
        body = {"snippet": {"videoId": video_id, "language": lang,
                            "name": NAMES.get(lang, lang), "isDraft": False}}
        media = MediaFileUpload(os.path.join(folder, name), mimetype="application/octet-stream")
        r = yt.captions().insert(part="snippet", body=body, media_body=media).execute()
        print("  subtitles", lang, "ok", r["id"])


def main():
    p = argparse.ArgumentParser(description="Upload a video to my own YouTube channel.")
    p.add_argument("file", nargs="?")
    p.add_argument("--status", metavar="VIDEO_ID")
    p.add_argument("--title")
    p.add_argument("--description", default="")
    p.add_argument("--description-file")
    p.add_argument("--tags", default="")
    p.add_argument("--privacy", default="private", choices=["public", "unlisted", "private"])
    p.add_argument("--thumbnail")
    p.add_argument("--captions")
    p.add_argument("--category", default="28")
    a = p.parse_args()

    yt = build("youtube", "v3", credentials=creds())

    if a.status:
        show_status(yt, a.status)
        return
    if not a.file or not a.title:
        print(__doc__)
        sys.exit(1)

    me = yt.channels().list(part="snippet", mine=True).execute()["items"][0]
    print("signed in as channel:", me["snippet"]["title"], "(" + me["id"] + ")")

    description = a.description
    if a.description_file:
        with open(a.description_file, encoding="utf-8") as f:
            description = f.read()

    body = {
        "snippet": {
            "title": a.title,
            "description": description,
            "tags": [t.strip() for t in a.tags.split(",") if t.strip()],
            "categoryId": a.category,
        },
        "status": {"privacyStatus": a.privacy, "selfDeclaredMadeForKids": False},
    }
    size_mb = os.path.getsize(a.file) / 1e6
    print(f"uploading {os.path.basename(a.file)} ({size_mb:.1f} MB) as {a.privacy} ...")

    media = MediaFileUpload(a.file, chunksize=8 * 1024 * 1024, resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp, t0 = None, time.time()
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print(f"  {int(status.progress() * 100)}%")
    video_id = resp["id"]
    print(f"upload complete in {time.time() - t0:.0f}s, video id {video_id}")

    if a.thumbnail:
        yt.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(a.thumbnail)).execute()
        print("  thumbnail ok")
    if a.captions:
        upload_captions(yt, video_id, a.captions)

    print()
    got = show_status(yt, video_id)
    if got != a.privacy:
        print()
        print(f"NOTE: requested '{a.privacy}' but YouTube set '{got}'.")


if __name__ == "__main__":
    main()
