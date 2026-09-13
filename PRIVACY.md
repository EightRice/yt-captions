# Privacy Policy for yt-captions

Last updated: September 13, 2026

yt-captions is a personal command-line script written and operated by Andrei Taranu (the "Operator")
to manage caption tracks on the Operator's own YouTube channel. It is an API Client that uses YouTube
API Services. It has a single user, the Operator. Nobody else can use it, log in to it, or have their
data accessed by it.

## YouTube API Services

This API Client uses YouTube API Services to:

- read the list of caption tracks on videos owned by the Operator;
- upload caption tracks to videos owned by the Operator.

By using YouTube API Services this client is bound by the
[YouTube Terms of Service](https://www.youtube.com/t/terms) and the
[Google Privacy Policy](https://www.google.com/policies/privacy).

## Data accessed

The client accesses only Authorized Data of the Operator's own Google account: the caption track
metadata of the Operator's own videos, and an OAuth token that lets it act on the Operator's behalf.
It does not access any data belonging to any other YouTube user or channel.

## Data stored

- The OAuth token (`token.json`) is stored on the Operator's own computer so that consent does not
  have to be repeated on every run. It is never uploaded, shared, or transmitted anywhere other than
  to Google's API endpoints.
- Caption files uploaded by the script are authored by the Operator and are stored on YouTube as
  caption tracks of the Operator's videos.
- Nothing else is stored. No logs, no analytics, no databases, no cookies.

## Data sharing

No data is shared with any third party. No data is sold. No data leaves the Operator's machine
except in requests to Google's own API.

## Data deletion and revocation

- Deleting `token.json` from the Operator's computer removes all locally stored authorization data.
- Access can also be revoked at any time from
  [Google security settings](https://security.google.com/settings/security/permissions), after which
  the stored token stops working.
- Caption tracks can be removed from a video at any time in YouTube Studio.

## Contact

Questions about this policy: open an issue on this repository, or email contact@eightrice.xyz.
