from LM_neopixel import load_n_init, segment, Data
from LM_neopixel import pinmap as pm


class DrawEffect:
    __instance = None

    def __new__(cls, pixcnt=24):
        if DrawEffect.__instance is None:
            # SocketServer singleton properties
            DrawEffect.__instance = super().__new__(cls)
            DrawEffect.__instance.pix_cnt = None
            DrawEffect.__instance.index_offset = 0
            DrawEffect.__instance.color_wheel = 0
            DrawEffect.__instance.__init_effect(pixcnt)
            DrawEffect.__instance.offset_gen = None
        return DrawEffect.__instance

    def __init_effect(cls, ledcnt):
        """
        Set neopixel object & store pixel cnt
        """
        if Data.NEOPIXEL_OBJ is None:
            load_n_init(ledcnt=ledcnt)
            cls.pix_cnt = Data.NEOPIXEL_OBJ.n
        if cls.pix_cnt is None:
            cls.pix_cnt = Data.NEOPIXEL_OBJ.n
        return cls.pix_cnt

    def __offset(cls, shift):
        def gen(step):
            while True:
                if step:
                    # Step rotation cycle - shift True
                    cls.index_offset += 1
                    if cls.index_offset > cls.pix_cnt - 1:
                        cls.index_offset = 0
                for k in range(cls.index_offset, cls.pix_cnt):
                    yield k
                for k in range(0, cls.index_offset):
                    yield k
        if cls.offset_gen is None:
            cls.offset_gen = gen(step=shift)
        return cls.offset_gen

    def draw(cls, iterable, shift=False):
        """
        DRAW GENERATED COLORS (RGB)
        HELPER FUNCTION with auto shift (offset) sub function
        :param iterable: Colors generator object / iterable
        :ms: wait in ms / step aka speed
        :return: None
        """
        offset_gen = cls.__offset(shift=shift)
        r, g, b, i = 0, 0, 0, 0
        for r, g, b in iterable:
            # Handle index offset - rotate effect
            i = offset_gen.__next__()
            segment(int(r), int(g), int(b), s=i, write=False)
        try:
            # Send (all) and save (last) color
            segment(int(r), int(g), int(b), s=i, cache=True, write=True)
            return True
        except Exception:
            return False


def meteor(r, g, b, shift=False, ledcnt=24):
    def __effect(r, g, b, pixel):
        """
        :param r: red target color
        :param g: green target color
        :param b: blue target color
        :param pixel: number of led segments
        :return: yield tuple with r,g,b
        """
        step = float(0.9 / pixel)
        for k in range(0, pixel):
            fade = (k+1) * step
            data = round(r * fade), round(g * fade), round(b * fade)
            yield data

    # Init custom params
    effect = DrawEffect(pixcnt=ledcnt)
    # Create effect data
    cgen = __effect(r, g, b, effect.pix_cnt)
    # Draw effect data
    effect.draw(cgen, shift=shift)
    return 'Meteor R{}:G{}:B{} N:{}'.format(r, g, b, effect.pix_cnt)


def cycle(r, g, b, ledcnt=24):
    def __effect(r, g, b, n):
        lightrgb = round(r*0.1), round(g*0.1), round(b*0.1)
        yield lightrgb
        yield r, g, b
        yield lightrgb
        for i in range(3, n):
            yield 0, 0, 0

    effect = DrawEffect(pixcnt=ledcnt)
    cgen = __effect(r, g, b, effect.pix_cnt)
    o = effect.draw(cgen, shift=True)
    return 'Cycle: {}'.format(o)


def rainbow(step=15, br=100, ledcnt=24):
    def __wheel(pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            return 0, 0, 0
        if pos < 85:
            return 255 - pos * 3, pos * 3, 0
        if pos < 170:
            pos -= 85
            return 0, 255 - pos * 3, pos * 3
        pos -= 170
        return pos * 3, 0, 255 - pos * 3

    def __effect(cnt, step, br):
        """
        :param cnt: led segment count
        :param br: max brightness 0-100%
        :param step: step size
        """
        cw = DrawEffect().color_wheel
        DrawEffect().color_wheel = 0 if cw >= 255 else cw+step
        for i in range(0, cnt):
            rc_index = (i * 256 // cnt) + DrawEffect().color_wheel
            r, g, b = __wheel(rc_index & 255)
            yield round(r*br*0.01), round(g*br*0.01), round(b*br*0.01)

    effect = DrawEffect(pixcnt=ledcnt)
    cgen = __effect(effect.pix_cnt, step=step, br=br)
    o = effect.draw(cgen, shift=True)
    return 'Rainbow: {}'.format(o)


#######################
# LM helper functions #
#######################

def lmdep():
    return 'neopixel'


def pinmap():
    return pm()


def help():
    return 'meteor r=<0-255> g=<0-255> b=<0-255> shift=False ledcnt=24',\
           'cycle r g b ledcnt=24', 'rainbow step=15 br=<5-100> ledcnt=24', 'pinmap'
