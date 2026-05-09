from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build("youtube", "v3", developerKey=API_KEY)


def search_youtube(query, max_results=5):

    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results
    )

    response = request.execute()

    results = []

    for item in response["items"]:

        results.append({
            "title": item["snippet"]["title"],
            "video_id": item["id"]["videoId"],
            "link": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            "channel": item["snippet"]["channelTitle"],
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
        })

    return results



def get_transcript(video_id):

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t["text"] for t in transcript])

    except Exception:
        return None
    

def summarize_video(llm, transcript):

    prompt = f"""
    You are a study assistant.

    Summarize this video in:
    - key points
    - explanation
    - important concepts

Transcript:
{transcript[:12000]}
"""

    return llm.invoke(prompt).content