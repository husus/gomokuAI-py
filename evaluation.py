def create_pattern_dict():
    x = -1
    patternDict = {}
    while (x < 2):
        y = -x
        # long_5
        patternDict[(x, x, x, x, x)] = 1000000 * x
        # live_4
        patternDict[(0, x, x, x, x, 0)] = 50000 * x
        # go_4
        patternDict[(0, x, x, x, x, y)] = 10000 * x
        patternDict[(y, x, x, x, x, 0)] = 10000 * x
        patternDict[(0, x, x, x, 0, x, 0)] = 10000 * x
        patternDict[(0, x, 0, x, x, x, 0)] = 10000 * x
        patternDict[(0, x, x, 0, x, x, 0)] = 10000 * x
        # dead_4
        patternDict[(y, x, x, x, x, y)] = -50 * x
        # live_3
        patternDict[(0, x, x, x, 0)] = 5000 * x
        patternDict[(0, x, 0, x, x, 0)] = 5000 * x
        patternDict[(0, x, x, 0, x, 0)] = 5000 * x
        # sleep_3
        patternDict[(0, 0, x, x, x, y)] = 500 * x
        patternDict[(y, x, x, x, 0, 0)] = 500 * x
        patternDict[(0, x, 0, x, x, y)] = 500 * x
        patternDict[(y, x, x, 0, x, 0)] = 500 * x
        patternDict[(0, x, x, 0, x, y)] = 500 * x
        patternDict[(y, x, 0, x, x, 0)] = 500 * x
        patternDict[(x, 0, 0, x, x)] = 500 * x
        patternDict[(x, x, 0, 0, x)] = 500 * x
        patternDict[(x, 0, x, 0, x)] = 500 * x
        patternDict[(y, 0, x, x, x, 0, y)] = 500 * x
        # dead_3
        patternDict[(y, x, x, x, y)] = -50 * x
        # live_2
        patternDict[(0, 0, x, x, 0)] = 100 * x
        patternDict[(0, x, x, 0, 0)] = 100 * x
        patternDict[(0, x, 0, x, 0)] = 100 * x
        patternDict[(0, x, 0, 0, x, 0)] = 100 * x
        # sleep_2
        patternDict[(0, 0, 0, x, x, y)] = 50 * x
        patternDict[(y, x, x, 0, 0, 0)] = 50 * x
        patternDict[(0, 0, x, 0, x, y)] = 50 * x
        patternDict[(y, x, 0, x, 0, 0)] = 50 * x
        patternDict[(0, x, 0, 0, x, y)] = 50 * x
        patternDict[(y, x, 0, 0, x, 0)] = 50 * x
        patternDict[(x, 0, 0, 0, x)] = 50 * x
        patternDict[(y, 0, x, 0, x, 0, y)] = 50 * x
        patternDict[(y, 0, x, x, 0, 0, y)] = 50 * x
        patternDict[(y, 0, 0, x, x, 0, y)] = 50 * x
        # dead_2
        patternDict[(y, x, x, y)] = -50 * x
        x += 2
    return patternDict