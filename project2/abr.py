from enum import Enum
from collections import deque

BITRATES = [300, 750, 1200, 1850, 2850, 4300]  # Kbps


class CALLBACK_EVENT(Enum):
    INIT = 0
    DOWNLOAD_COMPLETED = 1
    TIMEOUT = 2
    REBUFFERING = 3


current = None
last_chunk = None
last_quality = None
last_download = None

last_change = 0

bandwidth = deque(maxlen=10)


def abr(
        typ,
        current_time,
        playback_time,
        playback_chunk,
        current_chunk,
        current_chunk_quality,
        current_chunk_download,
        video
):
    """
        typ - type of event
            INIT - initial call at time 0
            DOWNLOAD_COMPLETED - a chunk has been downloaded
            TIMEOUT - timeout has happend
            REBUFFERING - rebuffering started
        
        current_time - time from the beginning of the simulation in seconds
        
        playback_time - how much of the video has been shown (in seconds)
        playback_chunk - the chunk that is playing right now
        current_chunk - the chunk number that is downloading right now (or has been just finished)
        current_chunk_quality - the quality of the current_chunk
        current_chunk_download - how much of current_chunk has been downloaded (in bytes)
        video - contains 6 video arrays (one per quality level) - Each subarray contain the size of each chunk in the video

        Returns
            quality_to_download_now, chunk_to_download_now, timeout

        ABR function returns the next chunk that should be downloaded
           * quality_to_download_now - quality of the next chunk from 0 to 5
           * chunk_to_download_now   - chunk number of the chunk that should be downloaded
                                     - next_chunk cannot be in the past, if the player plays chunk 10, chunk 9 shouldn't be downloaded
                                     - if you set next_chunk to -1, no chunk will be downloaded
                                     - if the previou download hasn't been completed (e.g. in case of rebuffering) you can change the chunk
                                       that is currently downloading. For instance, you started downloading a high quality chunk, but
                                       rebuffering happened and now you would like to lower the quality. In that case, return the same chunk
                                       number, but different quality.
           * timeout    - set a timer that will trigger the abr function again
                        - timeout is in absolute time, usually set it as current_time+X (where min X is 200ms)
                        - timeout 0 means no timeout
    """

    global last_chunk, last_quality, last_download, bandwidth, last_change

    # Initialization
    if typ == CALLBACK_EVENT.INIT:
        last_chunk = 0
        last_quality = 0
        last_download = 0

        return dispatch(0, 0, current_time + 0.2)

    # Chunk downloaded
    if typ == CALLBACK_EVENT.DOWNLOAD_COMPLETED:
        next_chunk = current_chunk + 1

        if next_chunk == len(video[0]):
            return dispatch(-1, 0)

        if buffer_size(current_chunk, playback_chunk) > 10 and last_change > 4:
            next_chunk_quality = min(current_chunk_quality + 1, 5)
        elif buffer_size(current_chunk, playback_chunk) < 3:
            next_chunk_quality = max(current_chunk_quality - 1, 0)
        else:
            next_chunk_quality = current_chunk_quality

        last_change += 1
        if next_chunk_quality != current_chunk_quality:
            last_change = 0

        return dispatch(next_chunk, next_chunk_quality)

    # Trigger
    if typ == CALLBACK_EVENT.TIMEOUT:

        if last_chunk == current_chunk:
            current_bandwidth = current_chunk_download - last_download
        else:
            current_bandwidth = BITRATES[last_quality] * 4 - last_download

        bandwidth.append(current_bandwidth)

        last_chunk = current_chunk
        last_quality = current_chunk_quality
        last_download = current_chunk_download

        return dispatch(current_chunk, current_chunk_quality, current_time + 200)

    # Rebuffering, fall back to the lowest quality
    if typ == CALLBACK_EVENT.REBUFFERING:
        return dispatch(current_chunk, 0)


def dispatch(chunk, quality, next=0):
    global current

    current = (chunk, quality)

    return quality, chunk, next


def buffer_size(current_chunk, playback_chunk):
    return current_chunk - playback_chunk


def get_bandwidth():
    global bandwidth

    return sum(bandwidth) / 2
