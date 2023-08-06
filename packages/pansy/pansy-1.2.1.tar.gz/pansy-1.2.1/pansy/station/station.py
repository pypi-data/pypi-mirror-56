import time
import signal
import setproctitle
import threading

from .worker import Worker


class Station:
    app = None
    room_id_begin = None
    room_id_end = None

    enabled = True

    workers = None

    def __init__(self, app, room_id_begin, room_id_end):
        self.app = app
        self.workers = list()
        self.room_id_begin = room_id_begin
        self.room_id_end = room_id_end

    def run(self):
        setproctitle.setproctitle(self.app.make_proc_name(
            'station:%s-%s' % (self.room_id_begin, self.room_id_end)
        ))
        self._handle_signals()

        self._spawn_workers()

    def _create_worker(self, room_id):
        worker = threading.Thread(
            target=Worker(self, room_id).run,
        )
        # master不可以独自退出
        worker.daemon = False
        # 标记room_id
        worker.room_id = room_id

        worker.start()

        return worker

    def _spawn_workers(self):
        """
        监控线程
        :return:
        """
        for room_id in range(self.room_id_begin, self.room_id_end+1):
            self.workers.append(self._create_worker(room_id))

        while True:
            for idx, process in enumerate(self.workers):
                if process and not process.is_alive():
                    self.workers[idx] = None

                    if self.enabled:
                        # 需要重启启动process
                        self.workers[idx] = self._create_worker(process.room_id)

            if not self.enabled and not any(self.workers):
                # 可以彻底停掉了
                break

            time.sleep(0.1)

    def _handle_signals(self):
        def safe_stop_handler(signum, frame):
            self.enabled = False

        # 忽略掉
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        # 安全停止
        signal.signal(signal.SIGTERM, safe_stop_handler)


