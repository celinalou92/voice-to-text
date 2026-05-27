import yt_dlp

def yt_download(url, output_dir):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'restrictfilenames': True,
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'extractor_args': {'youtube': {'js_runtimes': ['nodejs']}},
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            },
        ],
        'progress_hooks': [progress_hook],
        'cookiesfrombrowser': ('firefox',)
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filepath = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'
        return filepath


def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', 'N/A')
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        print(f"\rProgress: {percent} | Speed: {speed} | ETA: {eta}", end='')
    elif d['status'] == 'finished':
        print(f"\nDownload complete: {d['filename']}")

