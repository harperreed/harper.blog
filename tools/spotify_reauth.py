# ABOUTME: Interactive one-time re-auth for the Spotify saved-tracks poller.
# ABOUTME: Mints a fresh .spotify_cache after Spotify expires/revokes the refresh token.

"""Re-authorize the Spotify poller when CI dies with invalid_grant.

Run from tools/:

    uv run spotify_reauth.py

It prompts for the app credentials from https://developer.spotify.com/dashboard
(same app CI uses; env vars SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET /
SPOTIFY_REDIRECT_URI are used when set, so nothing lands in shell history).
Open the printed URL in any browser, approve, and paste back the full URL you
land on — an error page is fine, only the ?code= parameter matters.

On success it writes .spotify_cache and verifies the token with a live API
call. Then update the CI secret from the repo root:

    gh secret set SPOTIFY_TOKEN_CACHE < tools/.spotify_cache
"""

import getpass
import os
import sys

import spotipy
from spotipy.oauth2 import SpotifyOAuth

CACHE_PATH = ".spotify_cache"


def ask(name, secret=False):
    value = os.getenv(name)
    if not value:
        prompt = f"{name}: "
        value = getpass.getpass(prompt) if secret else input(prompt)
    return value.strip()


def main():
    client_id = ask("SPOTIFY_CLIENT_ID")
    client_secret = ask("SPOTIFY_CLIENT_SECRET", secret=True)
    redirect_uri = ask("SPOTIFY_REDIRECT_URI")
    if not all([client_id, client_secret, redirect_uri]):
        print("All three values are required.", file=sys.stderr)
        return 1

    # A dead cached token short-circuits spotipy's flow before it ever asks
    # for a fresh grant, so clear it first.
    if os.path.exists(CACHE_PATH):
        os.remove(CACHE_PATH)

    auth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-library-read",
        cache_path=CACHE_PATH,
        open_browser=False,
    )

    print("\nOpen this URL in any browser and approve access:\n")
    print(auth.get_authorize_url())
    redirected = input("\nPaste the full URL you were redirected to: ").strip()
    code = auth.parse_response_code(redirected)
    auth.get_access_token(code, as_dict=False, check_cache=False)

    sp = spotipy.Spotify(auth_manager=auth)
    me = sp.current_user()
    total = sp.current_user_saved_tracks(limit=1)["total"]
    print(f"\nAuthorized as {me['display_name']} — {total} saved tracks visible.")
    print(f"Fresh token written to {CACHE_PATH}. From the repo root, run:")
    print("    gh secret set SPOTIFY_TOKEN_CACHE < tools/.spotify_cache")
    return 0


if __name__ == "__main__":
    sys.exit(main())
