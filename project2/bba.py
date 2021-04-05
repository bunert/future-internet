from collections import deque
from callback import CALLBACK_EVENT


class BBA:
    BITRATES = [300, 750, 1200, 1850, 2850, 4300]  # Kbps

    current = None
    last_chunk = None
    last_quality = None
    last_download = None
    last_change = 0
    bandwidth = deque(maxlen=10)

    def abr(
            self,
            typ,
            current_time,
            playback_time,
            playback_chunk,
            current_chunk,
            current_chunk_quality,
            current_chunk_download,
            video,
    ):

        # Initialization
        if typ == CALLBACK_EVENT.INIT:
            self.last_chunk = 0
            self.last_quality = 0
            self.last_download = 0

            return self.dispatch(0, 0, current_time + 0.2)

        # Chunk downloaded
        if typ == CALLBACK_EVENT.DOWNLOAD_COMPLETED:
            next_chunk = current_chunk + 1

            if next_chunk == len(video[0]):
                return self.dispatch(-1, 0)

            if self.buffer_size(current_chunk, playback_chunk) > 10 and self.last_change > 4:
                next_chunk_quality = min(current_chunk_quality + 1, 5)
            elif self.buffer_size(current_chunk, playback_chunk) < 3:
                next_chunk_quality = max(current_chunk_quality - 1, 0)
            else:
                next_chunk_quality = current_chunk_quality

            self.last_change += 1
            if next_chunk_quality != current_chunk_quality:
                self.last_change = 0

            return self.dispatch(next_chunk, next_chunk_quality)

        # Trigger
        if typ == CALLBACK_EVENT.TIMEOUT:

            if self.last_chunk == current_chunk:
                current_bandwidth = current_chunk_download - self.last_download
            else:
                current_bandwidth = self.BITRATES[self.last_quality] * 4 - self.last_download

            self.bandwidth.append(current_bandwidth)

            self.last_chunk = current_chunk
            self.last_quality = current_chunk_quality
            self.last_download = current_chunk_download

            return self.dispatch(current_chunk, current_chunk_quality, current_time + 200)

        # Rebuffering, fall back to the lowest quality
        if typ == CALLBACK_EVENT.REBUFFERING:
            return self.dispatch(current_chunk, 0)

    def dispatch(self, chunk, quality, next=0):
        self.current = (chunk, quality)

        return quality, chunk, next

    @staticmethod
    def buffer_size(current_chunk, playback_chunk):
        return current_chunk - playback_chunk

    def get_bandwidth(self):
        return sum(self.bandwidth) / 2
