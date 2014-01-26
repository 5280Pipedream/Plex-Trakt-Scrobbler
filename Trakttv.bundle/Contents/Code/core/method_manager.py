from core.helpers import spawn, plural
from core.logger import Logger
import threading

log = Logger('core.method_manager')


class Method(object):
    name = None

    def __init__(self, threaded=True):
        if threaded:
            self.thread = threading.Thread(target=self.run, name=self.get_name())
            self.running = False

        self.threaded = threaded

    def get_name(self):
        return self.name

    @classmethod
    def test(cls):
        raise NotImplementedError()

    def start(self):
        if not self.threaded or self.running:
            return False

        self.thread.start()
        self.running = True

    def run(self):
        raise NotImplementedError()


class Manager(object):
    tag = None

    available = []
    enabled = []

    @classmethod
    def register(cls, method, weight=None):
        item = (weight, method)

        # weight = None, highest priority
        if weight is None:
            cls.available.insert(0, item)
            return

        # insert in DESC order
        for x in xrange(len(cls.available)):
            w, _ = cls.available[x]

            if w is not None and w < weight:
                cls.available.insert(x, item)
                return

        # otherwise append
        cls.available.append(item)

    @classmethod
    def start(cls, blocking=False):
        if not blocking:
            spawn(cls.start, blocking=True)
            return

        # Test methods until an available method is found
        for weight, method in cls.available:
            if weight is None:
                cls.start_method(method)
            elif method.test():
                cls.start_method(method)

                if not Prefs['force_legacy']:
                    break
            else:
                log.info("method '%s' not available" % method.name, tag=cls.tag)

        log.info(
            'Finished starting %s method%s: %s',
            len(cls.enabled), plural(cls.enabled),
            ', '.join([("'%s'" % m.name) for m in cls.enabled]),

            tag=cls.tag
        )

    @classmethod
    def start_method(cls, method):
        obj = method()
        cls.enabled.append(obj)

        spawn(obj.start)
