import sys
import bisect

HAYSTACK = [0] + [i for i in range(30) if i % 2 == 1]
NEEDLE = [i for i in range(31) if i % 2 == 0]

ROW_FMT = '{0:2d} @ {0:2d}    {2}{0:<2d}'


def demo(bisect_fn):
    for needle in reversed(NEEDLE):
        position = bisect_fn(HAYSTACK, needle)
        offset = position * '  |'
        print(ROW_FMT.format(needle, position, offset))


if __name__ == '__main__':
    if sys.argv[-1] == 'left':  # sys.argv[-1]表示控制台编译该python文件时，最后一个输入的参数
        bisect_fn = bisect.bisect_left
    else:
        bisect_fn = bisect.bisect

    print('DEMO:', bisect_fn.__name__)
    print('haystack ->', ' '.join('%2d' % n for n in HAYSTACK))
    demo(bisect_fn)
