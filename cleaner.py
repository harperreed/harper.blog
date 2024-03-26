import os
import frontmatter
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential
from concurrent.futures import ThreadPoolExecutor
import datetime
import json
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Set your OpenAI API key using an environment variable
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
    # api_base="https://api.openai.com",
)

# Set the path to your content directory
content_dir = "./content/archives2"
model="gpt-3.5-turbo-1106"
system_prompt = "You are a helpful assistant that generates tags and summaries for blog posts."
user_prompt = """
Please generate up to 5 relevant tags and a brief summaryfor the following blog post content.

Important instructions:
    - Match the tone of the post. If it is casual, be casual. If it is formal, be formal. If it has mispellings, include them.
    - You must return JSON.
    - The tags should be a list of strings.
    - The summary should be a string.
    - The tags should be relevant to the content of the post.
    - The summary should be a brief overview of the content of the post.
    - The Author's name is Harper.
    - Cornell is Cornell College
    - The point of view for the summary is first person.

Content:
"""

# Function to generate tags and summary using OpenAI's GPT-4 turbo model
@retry(stop=stop_after_attempt(3), wait=wait_random_exponential(min=1, max=60))
def generate_metadata(content):
    logging.debug(f"Generating metadata for content: {content[:100]}...")
    try:

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{user_prompt}:\n\n{content}"}
            ],
            response_format={ "type": "json_object" },
            max_tokens=100,
            n=1,
            temperature=0.7,
        )

        # Extract the generated tags and summary from the API response
        generated_text = response.choices[0].message.content.strip()

        payload = json.loads(generated_text)

        lines = generated_text.split('\n')
        tags = payload['tags']
        summary = payload['summary']

        return tags, summary
    except client.error.APIError as e:
        logging.error(f"OpenAI API Error: {str(e)}")
        raise

    except Exception as e:
        logging.error(f"Error generating metadata at line {e.__traceback__.tb_lineno}: {str(e)}")
        raise

# Function to process a single file
def process_file(filename):
    logging.debug(f"Processing file: {filename}")
    file_path = os.path.join(content_dir, filename)

    # Load the markdown file with frontmatter
    with open(file_path, 'r') as file:
        post = frontmatter.load(file)

    # Extract the content of the blog post
    content = post.content
    old_tags = post.get('tags', [])
    print(old_tags)

    # print(f"[{content}]")
    # return

    if content == "":
        logging.error("Content is empty")
        return

    if post.get('cleaned', False):
        logging.info(f"File {filename} has already been cleaned")
        return

    # try:
    if True:
        # Check if tags and summary already exist and need updating
        existing_tags = post.get('tags', [])
        existing_summary = post.get('summary', '')

        # Generate tags and summary using OpenAI's API
        tags, summary = generate_metadata(content)
        logging.info(f"Generated tags: {tags}")

        # Update the front matter only if tags or summary have changed
        if set(tags) != set(existing_tags) or summary != existing_summary:
            # Create a backup of the original file with a timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{file_path}.{timestamp}.bak"
            with open(backup_path, 'w', encoding='utf-8') as backup_file:

                backup_file.write(frontmatter.dumps(post))


            # Update the front matter with the generated tags and summary
            post['tags'] = list(set(tags + old_tags))
            post['summary'] = summary
            post['cleaned'] = True


            with open(file_path, 'w', encoding='utf-8') as file:
                # frontmatter.dump(post, file, encoding='utf-8')
                file.write(frontmatter.dumps(post))

            logging.info(f"Updated metadata for {filename}")
        else:
            logging.info(f"Metadata for {filename} is already up to date")
    # except Exception as e:
    #     logging.error(f"Error processing {filename}: {str(e)}")

# Process files in parallel
with ThreadPoolExecutor() as executor:
    futures = []
    for filename in os.listdir(content_dir):
        if filename.endswith(".md"):
            futures.append(executor.submit(process_file, filename))

    # Wait for all futures to complete
    for future in futures:
        future.result()
