from enum import Enum


class CALLBACK_EVENT( Enum ):
    INIT = 0
    DOWNLOAD_COMPLETED = 1
    TIMEOUT  = 2
    REBUFFERING = 3


last_chunk = 0
byte_downloaded = 0

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
    global last_chunk, byte_downloaded
    
    #initial
    if typ == CALLBACK_EVENT.INIT:
        last_chunk = 0
        return 0, 0, current_time + 0.2

    # print("current chunk downloaded: ", current_chunk_download)
    # print("total size: ", video[current_chunk_quality][current_chunk])

    #rebuffering or timeout, ignore 
    if typ == CALLBACK_EVENT.DOWNLOAD_COMPLETED:
        # print("complete, quality: ", current_chunk_quality)
        next_chunk = current_chunk + 1
        byte_downloaded = 0
        last_chunk = next_chunk

        if next_chunk == len(video[0]):
            return 0, -1, 0.0
        
        # increase
        if current_chunk - playback_chunk > 3:
            next_chunk_quality = min(current_chunk_quality + 1, 5)
        # decrease
        elif current_chunk - playback_chunk < 3:
            next_chunk_quality = max(current_chunk_quality - 1, 0)
        else:
            next_chunk_quality = current_chunk_quality

        return next_chunk_quality, next_chunk, current_time + 0.2

    # Rebuffering, fall back to the lowest quality
    if typ == CALLBACK_EVENT.REBUFFERING:
        return 0, current_chunk, current_time + 0.2

    # Trigger
    if typ == CALLBACK_EVENT.TIMEOUT:
        current_bandwidth = current_chunk_download - byte_downloaded
        # print("bw (last 200ms): ", current_bandwidth)


        byte_downloaded = current_chunk_download


        return current_chunk_quality, current_chunk, current_time + 0.2

