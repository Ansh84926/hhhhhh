import scrapetube

def find_youtube_leads(query, limit=10):
    """
    Finds YouTube channels based on a search query.
    """
    print(f"Searching for YouTube leads for: {query}")
    # The generator might be yielding flattened dictionaries directly if they are video renderers
    videos = scrapetube.get_search(query, limit=limit)

    leads = []
    seen_channels = set()

    for item in videos:
        try:
            # Based on the keys we saw: ['videoId', 'thumbnail', 'title', 'ownerText', 'avatar', ...]
            # This looks like the videoRenderer content but already flattened out of the 'videoRenderer' key.

            channel_name = None
            channel_id = None

            # Try ownerText
            owner_text = item.get('ownerText', {})
            runs = owner_text.get('runs', [])
            if runs:
                channel_name = runs[0].get('text')
                channel_id = runs[0].get('navigationEndpoint', {}).get('browseEndpoint', {}).get('browseId')

            # Try shortBylineText if ownerText failed
            if not channel_id:
                short_byline = item.get('shortBylineText', {})
                runs = short_byline.get('runs', [])
                if runs:
                    channel_name = runs[0].get('text')
                    channel_id = runs[0].get('navigationEndpoint', {}).get('browseEndpoint', {}).get('browseId')

            # Try avatar if still failed
            if not channel_id:
                avatar = item.get('avatar', {}).get('decoratedAvatarViewModel', {})
                renderer_context = avatar.get('rendererContext', {})
                on_tap = renderer_context.get('commandContext', {}).get('onTap', {})
                innertube = on_tap.get('innertubeCommand', {})
                browse = innertube.get('browseEndpoint', {})
                channel_id = browse.get('browseId')
                if not channel_name:
                    channel_name = avatar.get('a11yLabel', '').replace('Go to channel ', '')

            if channel_id and channel_id not in seen_channels:
                seen_channels.add(channel_id)
                leads.append({
                    'source': 'YouTube',
                    'name': channel_name,
                    'id': channel_id,
                    'url': f"https://www.youtube.com/channel/{channel_id}"
                })
        except Exception as e:
            continue

    return leads

if __name__ == "__main__":
    # Test
    results = find_youtube_leads("cooking", limit=20)
    print(f"Found {len(results)} unique channels.")
    for lead in results[:5]:
        print(lead)
