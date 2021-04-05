from callback import CALLBACK_EVENT


class Default:

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

        # initial
        if typ == CALLBACK_EVENT.INIT:
            return 0, 0, 0.0

        # rebuffering or timeout, ignore
        if typ == CALLBACK_EVENT.TIMEOUT or typ == CALLBACK_EVENT.REBUFFERING:
            return current_chunk_quality, current_chunk, 0

        next_chunk = current_chunk + 1

        # if we arrived to the end of the stream or it is not the initial call and the download has finished

        if next_chunk == len(video[0]):
            next_chunk = -1

        return 0, next_chunk, 0.0
