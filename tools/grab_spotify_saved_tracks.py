import html
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
import frontmatter
import logging
from dotenv import load_dotenv
from slugify import slugify
import hashlib
import yaml

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def setup_spotify():
    """Initialize Spotify client with proper authentication."""
    try:
        # Use cache_path to specify where the token cache should be stored
        cache_path = os.getenv('SPOTIFY_TOKEN_CACHE_PATH', '.spotify_cache')
        
        # If we have a cached token in environment variable, write it to the cache file
        cached_token = os.getenv('SPOTIFY_TOKEN_CACHE')
        if cached_token:
            with open(cache_path, 'w') as f:
                f.write(cached_token)
        
        auth_manager = SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
            scope='user-library-read',
            cache_path=cache_path,
            open_browser=False  # Important for headless environments
        )
        
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        # After authentication, save the token back to environment if needed
        # if os.path.exists(cache_path):
        #     with open(cache_path, 'r') as f:
        #         token_info = f.read()
        #         # In a GitHub Action, you might want to set this as an output
        #         # to save for the next run
        #         print(f"::set-output name=spotify_token::{token_info}")
        
        return sp
    except Exception as e:
        logging.error(f"Failed to initialize Spotify client: {e}")
        raise

def get_saved_tracks(sp, limit=50, offset=0, grab_all=True):
    """Fetch user's saved tracks from Spotify."""
    tracks = []
    offset = 0
    
    try:
        while grab_all:
            results = sp.current_user_saved_tracks(limit=limit, offset=offset)
            if not results['items']:
                break
                
            for item in results['items']:
                track = item['track']
                added_at = item['added_at']
          
                track_data = {
                    'id': track['id'],
                    'title': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album': track['album']['name'],
                    'added_at': added_at,
                    'spotify_url': track['external_urls']['spotify'],
                    'preview_url': track['preview_url'],
                    'duration_ms': track['duration_ms'],
                    'album_image': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'raw_data': track,
                }
                tracks.append(track_data)
            
            offset += limit
            logging.info(f"Fetched {len(tracks)} tracks so far...")
            
            # Optional: break after first batch during development
            # if offset >= limit:
            #     break
            
    except Exception as e:
        logging.error(f"Error fetching tracks: {e}")
        raise
        
    return tracks

def generate_unique_slug(title, date_str, url):
    """Generate a unique slug for the markdown file."""
    base_slug = slugify(title)
    url_hash = hashlib.md5(url.encode()).hexdigest()[:6]
    
    try:
        date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except ValueError:
        date = datetime.now()
    
    date_str = date.strftime("%Y%m%d")
    return f"{date_str}-{base_slug}-{url_hash}"

def create_hugo_content(track, output_dir):
    """Create a Hugo markdown file for a track."""
    try:
        slug = generate_unique_slug(track['title'], track['added_at'], track['spotify_url'])
        file_path = os.path.join(output_dir, f"{slug}.md")

        if os.path.exists(file_path):
            logging.info(f"Track already exists: {file_path}")
            return False

        date = datetime.fromisoformat(track['added_at'].replace('Z', '+00:00'))
        # Metadata values are YAML-serialized so special chars are safe there.
        # The markdown body is rendered by goldmark (unsafe=true), so escape
        # feed-derived text that lands in the body.
        artist_safe = html.escape(track['artist'])
        album_safe = html.escape(track['album'])

        post = frontmatter.Post(
            f"## {artist_safe} on the album {album_safe}\n\n"
            f"You can listen [here]({track['spotify_url']})\n\n"
            f"{{{{% spotify \"{track['id']}\" small %}}}}\n\n"
            f"added on {date.strftime('%B %d, %Y')}\n",
            title=track['title'],
            translationKey=f"{track['title']}-{track['album']}-{track['artist']}",
            date=date,
            artist=track['artist'],
            album=track['album'],
            spotify_url=track['spotify_url'],
            preview_url=track['preview_url'],
            duration=track['duration_ms'],
            album_image=track['album_image'],
            draft=False,
            type='music',
        )

        # Write the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))

        logging.info(f"Created new track post: {file_path}")
        return True

    except Exception as e:
        logging.error(f"Error creating post for '{track.get('title', '?')}': {e}")
        return False

def main():
    """Main function to orchestrate the script. Returns 0 on success, 1 on failure."""
    hugo_content_dir = os.getenv('MUSIC_HUGO_CONTENT_DIR', "../content/music")
    hugo_data_dir = os.getenv('MUSIC_HUGO_DATA_DIR', "../data/music")

    os.makedirs(hugo_content_dir, exist_ok=True)
    os.makedirs(hugo_data_dir, exist_ok=True)

    try:
        sp = setup_spotify()
        tracks = get_saved_tracks(sp)

        new_tracks_count = 0
        for track in tracks:
            if create_hugo_content(track, hugo_content_dir):
                new_tracks_count += 1
                logging.info(f"Created new track post: {track['title']}")

                track_title = f"{track['added_at']} - {track['title']} - {track['artist']} - {track['album']}"
                data_filename = os.path.join(hugo_data_dir, f"{slugify(track_title)}.yaml")
                if os.path.exists(data_filename):
                    logging.info(f"Data file already exists: {data_filename}")
                    continue
                with open(data_filename, "w", encoding="utf-8") as f:
                    yaml.safe_dump(track, f, default_flow_style=False)
                    logging.info(f"Data file created: {data_filename}")

        logging.info(f"Successfully processed {len(tracks)} tracks")
        logging.info(f"Created {new_tracks_count} new track posts")
        return 0

    except Exception as e:
        logging.error(f"Script failed: {e}")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
