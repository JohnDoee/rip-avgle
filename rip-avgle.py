#!/usr/bin/env python

import argparse
import json
import os
import subprocess
import tempfile

import requests


def sanitize_title(title):
    keepcharacters = (' ','.','_')
    return "".join(c for c in title if c.isalnum() or c in keepcharacters).strip()[-50:]

def extract_m3u8_url(video_url):
    video_info = subprocess.check_output([
        'docker', 'run', '--rm',
        '-v', '%s:/app/index.js' % (os.path.join(os.path.dirname(os.path.abspath(__file__)), 'extract-avgle-url.js'), ),
        'alekzonder/puppeteer:latest',
        'node', 'index.js',
        video_url
    ], universal_newlines=True)
    video_info = json.loads(video_info)

    url = video_info['url']
    title = video_info['title'].split('>')[-1].strip()
    id_ = video_url.split('/')[4]

    r = requests.get(url, allow_redirects=False)

    return r.headers['Location'], title, id_


def download_m3u8(m3u8_url, target_file):
    cmd = ['ffmpeg']

    if 'ahcdn.com' not in m3u8_url:
        cmd += ['-headers', 'Referer: http://www.avg' + 'le.com',]

    cmd += [
        '-i', m3u8_url,
        '-c', 'copy',
        '-f', 'mp4',
        target_file
    ]
    print(cmd)
    p = subprocess.Popen(cmd)
    p.wait()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download videos from avgle.')
    parser.add_argument('url',  type=str, nargs='+', help='URL to download')

    args = parser.parse_args()
    for url in args.url:
        print('Downloading: %s' % (url, ))

        m3u8_url, video_title, video_id = extract_m3u8_url(url)
        filename = '%s - %s.mp4' % (sanitize_title(video_title), video_id, )
        download_m3u8(m3u8_url, filename)