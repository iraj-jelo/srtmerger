from datetime import datetime, timezone


def time_to_timestamp(time: str|datetime):
    """Turn a time string or datetime instance to timestamp in seconds or milliseconds"""
    # OSError: [Errno 22] Invalid argument
    # The timestamp() method may fail on systems like Windows for dates before
    # the UNIX epoch (1970-01-01) or far into the future.
    # logger.debug(f"⌛ {repr(time)} <- {time}, {type(time)}")
    if  type(time) is str:
        if ',' in time:            
            time, milliseconds = time.split(',')
            timestamp = (
                datetime
                .strptime(time, '%H:%M:%S')
                .replace(tzinfo=timezone.utc)
                .timestamp()
            )
            timestamp_with_milliseconds = (
                timestamp +
                (
                    (
                        int(milliseconds) / (10**len(milliseconds))
                    ) * (-1 if (timestamp < 0) else 1)
                )
            )
            return timestamp_with_milliseconds
        return (
            datetime
            .strptime(time, '%H:%M:%S')
            .replace(tzinfo=timezone.utc)
            .timestamp()
        )
    return time.replace(tzinfo=timezone.utc).timestamp()