!pip install google-api-python-client

!pip install youtube-transcript-api

import feedparser

rss_url = "https://towardsdatascience.com/feed"
feed = feedparser.parse(rss_url)

for entry in feed.entries[:5]:
    print(f"Title: {entry.title}")
    print(f"Link: {entry.link}")
    print(f"Published: {entry.published}")
    print("-" * 50)


!pip install pillow

import random
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

# YouTube API Key (replace with your own)
YOUTUBE_API_KEY = "AIzaSyDSUBJmjbxh-_qtHDkJF6w2Rtx06NjyruQ"

# Build YouTube API client
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# Fetch trending tech videos
def get_trending_tech_videos(max_results=5):
    request = youtube.search().list(
        q="technology trends",  
        part="snippet",
        type="video",
        maxResults=max_results,
        order="viewCount"
    )
    response = request.execute()

    videos = []
    for item in response["items"]:
        videos.append({
            "title": item["snippet"]["title"],
            "video_id": item["id"]["videoId"],
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]  # Get high-quality thumbnail
        })

    return videos

# Search YouTube for a specific topic
def search_youtube_videos(query, max_results=5):
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results,
        order="relevance"
    )
    response = request.execute()

    videos = []
    for item in response["items"]:
        videos.append({
            "title": item["snippet"]["title"],
            "video_id": item["id"]["videoId"],
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
        })

    return videos

# Get transcript from YouTube video
def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([item["text"] for item in transcript])
    except Exception:
        return None  # Silently skip videos without transcripts

# Summarize transcript
def summarize_text(text):
    if len(text) < 300:  # Shorter texts don't need summarization
        return text

    summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")
    max_chunk = 300
    chunks = [text[i:i + max_chunk] for i in range(0, len(text), max_chunk)]

    summary = ""
    for chunk in chunks:
        summary_part = summarizer(chunk, max_length=50, min_length=20, do_sample=False)
        summary += summary_part[0]["summary_text"] + " "

    return summary.strip()

# Generate short, engaging LinkedIn posts
def create_insight_post(title, summary):
    opening_lines = [
        "Tech is evolving fast —",
        "I just came across something fascinating —",
        "Here’s a quick insight worth sharing —",
        "It’s amazing how this is shaping our future —",
        "One thing that really stood out to me —"
    ]

    reflection_lines = [
        "The future is closer than we think.",
        "We’re living in exciting times!",
        "It’s time we pay attention to this.",
        "This could change everything.",
        "Adapting to this will be crucial."
    ]

    hashtags = [
        "#TechTrends", "#Innovation", "#AI", "#FutureOfWork", "#DataScience", "#Automation"
    ]

    opening = random.choice(opening_lines)
    reflection = random.choice(reflection_lines)
    random_hashtags = " ".join(random.sample(hashtags, 2))

    post = (
        f"{opening} {title}.\n\n"
        f"{summary} {reflection}\n\n"
        f"{random_hashtags}"
    )

    return post

# Full workflow
def generate_insight_posts(topic=None, max_results=5):
    if topic:
        videos = search_youtube_videos(topic, max_results)
    else:
        print("\n Fetching trending tech topics...\n")
        videos = get_trending_tech_videos(max_results)

    for video in videos:
        transcript = get_video_transcript(video["video_id"])

        if transcript:
            summary = summarize_text(transcript)
            insight_post = create_insight_post(video["title"], summary)
            print("\n LinkedIn Post:\n")
            print(insight_post)
            print(f" Thumbnail: {video['thumbnail']}")
            print("-" * 80)
        else:
            print(f" Skipped: No transcript for '{video['title']}'")

# User input for custom topic or auto-fetch trending tech
user_topic = input("Enter a topic (or press Enter to get trending tech topics): ").strip()
generate_insight_posts(user_topic if user_topic else None, max_results=6)
