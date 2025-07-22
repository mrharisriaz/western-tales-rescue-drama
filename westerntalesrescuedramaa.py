import streamlit as st
import requests
from datetime import datetime, timedelta

# YouTube API Key
API_KEY = "AIzaSyB8XLlAaZsST1bsInOpyEm-Uo0QJBH8QLQ"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# Streamlit App Title
st.title("YouTube Viral Topics Tool")

# Input Fields
days = st.number_input("Enter Days to Search (1-30):", min_value=1, max_value=30, value=5)

# List of broader keywords
keywords = [
 "Archer", "Comanche", "Apache", "Lakota", "Cowboy", "Soldier", "Horse", "Widow", "Bride", "Nurse", "Maid", "CEO", "Millionaire", "Billionaire", "Stranger", "Silent", "Quiet", "Child", "Baby", "Daughter", "Son", "Kids", "Orphan", "Mom", "Father", "Family", "Auction", "Rescue", "Freedom", "Pregnant", "Rejected", "Abandoned", "Starving", "Homeless", "Crying", "Hungry", "Shackled", "Cage", "Fence", "Barn", "Church", "Shroud", "Fire", "Desert", "River", "Trail", "Tree", "Well", "Office", "Love", "Marriage", "Home", "Shelter", "Coffee", "Jacket", "Blanket", "Armor", "Courage", "Adversity", "Addiction", "Widow", "Bride", "Cowboy", "Soldier", "Cook", "Nurse", "Teacher", "Doctor", "Maid", "CEO", "Billionaire", "Millionaire", "Orphan", "Daughter", "Son", "Kids", "Child", "Baby", "Mom", "Father", "Pregnant", "Rejected", "Starving", "Homeless", "Crying", "Shackled", "Cage", "Fence", "Barn", "Church", "Shroud", "Fire", "Desert", "River", "Trail", "Tree", "Ill", "Office", "Love", "Marriage", "Home", "Shelter", "Coffee", "Jacket", "Blanket", "Armor", "Courage", "Adversity", "Addiction", "Widow", "Bride", "Cowboy", "Soldier", "Cook", "Nurse", "Teacher", "Doctor", "Maid", "CEO", "Billionaire", "Millionaire", "Orphan", "Daughter", "Son", "Kids", "Child", "Baby", "Mom", "Father", "Pregnant", "Rejected", "Starving", "Homeless", "Crying", "Shackled", "Cage", "Fence", "Barn", "Church", "Shroud", "Fire", "Desert", "River", "Trail", "Tree", "Well", "Office", "Love", "Marriage", "Home", "Shelter", "Coffee", "Jacket", "Blanket", "Armor", "Courage", "Adversity", "Addiction", "Broken Woman", "Girl", "Stranger", "Rancher", "Preacher", "Spoils", "Maid", "Soldier", "Scout", "Father", "Mother", "Baby", "Child", "Daughter", "Son", "Family", "Widow", "Love", "Marriage", "Rescue", "Devotion", "Protection", "Shelter", "Abandonment", "Rejection", "Healing", "Belonging", "Redemption", "Trust", "Hope", "Home", "Unconscious", "Crying", "Starving", "Injured", "Blinded", "Escaped", "Fearful", "Alone", "Mistreated", "Abused", "Infertile", "Homeless", "Collapsed", "Tied Up", "Cast Out", "Pregnant", "Displaced", "Fallen", "Hero", "Starvation", "Wilderness", "Survival", "Courage", "Sacrifice", "Faith", "Grace", "Rebirth", "Salvation", "Victory", "Peace", "Western Romance", "Emotional Storytelling", "Cowboy Love", "Mail-Order Bride", "Western Drama", "Rescue Romance", "Historical Fiction", "Protective Cowboy", "Abandoned Woman", "Healing Love", "Redemption Story", "Old West Romance", "Christian Values", "Small Town Love", "Narrated Story", "YouTube Fiction", "Woman in Trouble", "Mail-order Bride", "Ovale Cowboy", "Indian Settler", "Fanfic", "Western Vigilante", "Survival Love Story", "Post-Apocalypse", "Far Western", "Frontier", "Legacy", "Spirit", "Heritage", "Cowboy", "Bride", "Mail-Order Bride", "Frontier", "Rescue", "Romance", "Emotional", "Storytelling", "Outlaws", "Ranch", "Cabin", "Wagon", "Prairie", "Desert", "Love", "Redemption", "Abandoned", "Beaten", "Wild", "Scarlet", "Harvest", "Orphan", "Baby", "Woman", "Man", "Heart", "Devotion", "Sacrifice", "Christian", "Faith", "Marriage", "Family", "Healing", "Survival", "Fire", "River", "Ridge", "Tunnel", "Town", "Church", "Homestead", "Struggles", "Forgiveness", "Hope", "Wilderness", "Widow", "Sheriff", "Soldier", "Stranger", "Mother", "Father", "Protector", "Orphan", "Rescuer", "Guardian", "Sacrament", "Bravery", "Courage", "Conflict", "Showdown", "Reunion", "Soulmates", "Blessing", "Healing"
]

# Fetch Data Button
if st.button("Fetch Data"):
    try:
        # Calculate date range
        start_date = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"
        all_results = []

        # Iterate over the list of keywords
        for keyword in keywords:
            st.write(f"Searching for keyword: {keyword}")

            # Define search parameters
            search_params = {
                "part": "snippet",
                "q": keyword,
                "type": "video",
                "order": "viewCount",
                "publishedAfter": start_date,
                "maxResults": 5,
                "key": API_KEY,
            }

            # Fetch video data
            response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)
            data = response.json()

            # Check if "items" key exists
            if "items" not in data or not data["items"]:
                st.warning(f"No videos found for keyword: {keyword}")
                continue

            videos = data["items"]
            video_ids = [video["id"]["videoId"] for video in videos if "id" in video and "videoId" in video["id"]]
            channel_ids = [video["snippet"]["channelId"] for video in videos if "snippet" in video and "channelId" in video["snippet"]]

            if not video_ids or not channel_ids:
                st.warning(f"Skipping keyword: {keyword} due to missing video/channel data.")
                continue

            # Fetch video statistics
            stats_params = {"part": "statistics", "id": ",".join(video_ids), "key": API_KEY}
            stats_response = requests.get(YOUTUBE_VIDEO_URL, params=stats_params)
            stats_data = stats_response.json()

            if "items" not in stats_data or not stats_data["items"]:
                st.warning(f"Failed to fetch video statistics for keyword: {keyword}")
                continue

            # Fetch channel statistics
            channel_params = {"part": "statistics", "id": ",".join(channel_ids), "key": API_KEY}
            channel_response = requests.get(YOUTUBE_CHANNEL_URL, params=channel_params)
            channel_data = channel_response.json()

            if "items" not in channel_data or not channel_data["items"]:
                st.warning(f"Failed to fetch channel statistics for keyword: {keyword}")
                continue

            stats = stats_data["items"]
            channels = channel_data["items"]

            # Collect results
            for video, stat, channel in zip(videos, stats, channels):
                title = video["snippet"].get("title", "N/A")
                description = video["snippet"].get("description", "")[:200]
                video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
                views = int(stat["statistics"].get("viewCount", 0))
                subs = int(channel["statistics"].get("subscriberCount", 0))

                if subs < 2,000:  # Only include channels with fewer than 2,000 subscribers
                    all_results.append({
                        "Title": title,
                        "Description": description,
                        "URL": video_url,
                        "Views": views,
                        "Subscribers": subs
                    })

        # Display results
        if all_results:
            st.success(f"Found {len(all_results)} results across all keywords!")
            for result in all_results:
                st.markdown(
                    f"**Title:** {result['Title']}  \n"
                    f"**Description:** {result['Description']}  \n"
                    f"**URL:** [Watch Video]({result['URL']})  \n"
                    f"**Views:** {result['Views']}  \n"
                    f"**Subscribers:** {result['Subscribers']}"
                )
                st.write("---")
        else:
            st.warning("No results found for channels with fewer than 3,000 subscribers.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
