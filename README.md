# yt-captions

A personal command-line script for uploading subtitle files to videos on my own YouTube channel
([youtube.com/@eightrice](https://www.youtube.com/@eightrice)) through the YouTube Data API v3.

It is not a service and has no users other than me. It runs on my computer, authenticates as me,
and touches only my own videos. I publish it here so the code is in the open and so the
YouTube API compliance review has something to look at.

## What it does

- Lists the caption tracks already on a video.
- Uploads `.srt` files as caption tracks, one per language, skipping languages that already exist.

## What it does not do

- It does not read, store or process data from any other YouTube account.
- It does not run as a server, website or hosted application.
- It does not share anything with third parties.

## Data handling

The only stored data is the OAuth token in `token.json` on my own machine. Deleting that file,
or revoking access at [myaccount.google.com/permissions](https://myaccount.google.com/permissions),
ends the script's access. See [PRIVACY.md](PRIVACY.md) and [TERMS.md](TERMS.md).

## Usage

```
pip install google-api-python-client google-auth-oauthlib
python upload_captions.py VIDEO_ID captions/
```

Caption files are named by language code: `captions/ro.srt`, `captions/pt-BR.srt`, `captions/zh-Hans.srt`.
