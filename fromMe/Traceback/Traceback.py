import types
from collections import deque


# print(sys.prefix == sys.base_prefix)

def traceback(e: Exception) -> types.TracebackType:    return e.__traceback__


def get_frame(e: Exception) -> types.FrameType:
    return traceback(e).tb_frame


def get_line(e: Exception) -> int:
    return traceback(e).tb_lineno


def frameLine(frame: types.FrameType) -> int:   return frame.f_lineno


def get_frameLine(e: Exception) -> int:
    return frameLine(get_frame(e))


def frameBack(frame: types.FrameType) -> types.FrameType:   return frame.f_back


def get_frameBack(e: Exception) -> types.FrameType:
    return frameBack(get_frame(e))


def getNext(e: Exception) -> types.TracebackType:   return e.__traceback__.tb_next


def frameName(frame: types.FrameType) -> str:   return frame.f_code.co_name


def get_frameName(e: Exception) -> str:
    return frameName(get_frame(e))


def fileName(frame: types.FrameType) -> str:   return frame.f_code.co_filename


def get_fileName(e: Exception) -> str:
    return fileName(get_frame(e))


def frameLocals(frame: types.FrameType) -> dict:   return frame.f_locals


def get_locals(e: Exception) -> dict:
    return frameLocals(get_frame(e))


def frameVars(frame: types.FrameType) -> tuple[str, ...]:   return frame.f_code.co_varnames


def get_vars(e: Exception) -> tuple[str, ...]:
    return frameVars(get_frame(e))


def frameFirstLine(frame: types.FrameType) -> int:   return frame.f_code.co_firstlineno


def get_frameFirstLine(e: Exception) -> int:
    return frameFirstLine(get_frame(e))


def go_forward(e: Exception):
    tb: types.TracebackType = traceback(e)
    while tb is not None:
        yield tb
        ntb = e.__traceback__.tb_next
        if ntb == tb: break
        tb = ntb


def go_backwards(e: Exception, maxL: int = -1):
    frame = get_frame(e)
    lines: deque[tuple[types.FrameType, str]] = deque()
    i = 0
    while i != maxL:
        upperName = frameName(frame)
        frame = frameBack(frame)
        if frame is None:
            break
        else:
            lines.appendleft((frame, upperName))
            i += 1
    return lines


def formatFrame(fr: types.FrameType, lowerName: str):
    return f'File <{fileName(fr)}> : Inside "{frameName(fr)}" defined at line : [ {frameFirstLine(fr)} ]\n' \
           f'    Line [ {frameLine(fr)} ] : {lowerName}'


def formatError(e: Exception):
    return f'File <{get_fileName(e)}> : Inside "{get_frameName(e)}", defined at line [ {get_frameFirstLine(e)} ]: \n' \
           f'Line [ {get_line(e)} ] : [ {type(e).__name__} ] : {e}'

import datetime

def formatDate(date: datetime.date=None):
    """:return day["d/m/y"] , hour["h,m,s"] """
    if date is None: date = datetime.datetime.now()
    return (f"{date.day}/{date.month}/{date.year}", f"{date.hour} : {date.minute} : {date.second}")

def getRawTraceback(e: Exception):
    return "\n".join(formatFrame(fr, fromFr) for fr, fromFr in go_backwards(e))

def formatTraceback(e: Exception, date: datetime.date):
    day, hour = formatDate(date)
    return f"[ {day} ] : Exception raised at [ {hour} ] :\n{getRawTraceback(e)}\n{formatError(e)}"


class Traceback:
    def __init__(self, exc: Exception, noTraceback=False):
        self.date = datetime.datetime.now()
        self.error = exc
        try: self.errorType = type(exc)
        except Exception as e: self.errorType = BaseException
        self.log = "Traceback Unavaliable" if noTraceback else formatTraceback(exc, self.date)

    def __str__(self):
        return self.log
    def __getitem__(self, item):
        return self.log[item]


def getTraceback(e: Exception):
    return Traceback(e)


def printTraceback(e: Exception):
    print(getTraceback(e))


if __name__ == '__main__':

    def run(_inp):
        try:
            return exec(input(_inp))
        except Exception as e:
            #  raise e
            return getTraceback(e)


    def loop():
        for errors in iter(lambda: run('input... '), "exit"): print("Traceback :\n", errors)


    loop()
