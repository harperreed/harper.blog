import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
import frontmatter
import logging
from dotenv import load_dotenv
from slugify import slugify
import hashlib

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

def get_saved_tracks(sp, limit=50):
    """Fetch user's saved tracks from Spotify."""
    tracks = []
    offset = 0
    
    try:
        while True:
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
                    'album_image': track['album']['images'][0]['url'] if track['album']['images'] else None
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
    # try:
    if True:
        slug = generate_unique_slug(track['title'], track['added_at'], track['spotify_url'])
        file_path = os.path.join(output_dir, f"{slug}.md")
        
        if os.path.exists(file_path):
            logging.info(f"Track already exists: {file_path}")
            return False

        # Create post with frontmatter
        post = frontmatter.Post("")
        post['title'] = track['title']
        post['date'] = datetime.fromisoformat(track['added_at'].replace('Z', '+00:00'))
        post['artist'] = track['artist']
        post['album'] = track['album']
        post['spotify_url'] = track['spotify_url']
        post['preview_url'] = track['preview_url']
        post['duration'] = track['duration_ms']
        post['album_image'] = track['album_image']
        post['draft'] = False
        post['type'] = 'music'
        
        post.content = f"""
## {post['artist']} on the album {post['album']}

You can listen [here]({post['spotify_url']})

{{{{% spotify "{track['id']}" small %}}}}

added on {post['date'].strftime("%B %d, %Y")}
"""
        
        # Write the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
        
        logging.info(f"Created new track post: {file_path}")
        return True
        
    # except Exception as e:
    #     logging.error(f"Error creating post for '{track['title']}': {e}")
    #     return False

def main():
    """Main function to orchestrate the script."""
    # Get environment variables
    hugo_content_dir = os.getenv('MUSIC_HUGO_CONTENT_DIR', "../content/music")
    
    if not hugo_content_dir:
        logging.error("MUSIC_HUGO_CONTENT_DIR must be set in the .env file")
        return
        
    # Ensure content directory exists
    os.makedirs(hugo_content_dir, exist_ok=True)
    
    try:
        # Initialize Spotify client
        sp = setup_spotify()
        
        # Fetch tracks
        tracks = get_saved_tracks(sp)
        
        # Create content files
        new_tracks_count = 0
        for track in tracks:
            if create_hugo_content(track, hugo_content_dir):
                new_tracks_count += 1
                
        logging.info(f"Successfully processed {len(tracks)} tracks")
        logging.info(f"Created {new_tracks_count} new track posts")
        
    except Exception as e:
        logging.error(f"Script failed: {e}")

if __name__ == "__main__":
    main()
