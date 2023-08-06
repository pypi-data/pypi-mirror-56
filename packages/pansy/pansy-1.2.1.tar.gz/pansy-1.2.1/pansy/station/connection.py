import socket
import errno
import select
import time

from ..share import constants
from ..share.log import logger
from ..share.task import Task


class Connection:
    worker = None
    client = None

    # 待发送buf
    send_buf = None

    # 接收到buf
    recv_buf = None

    task_list = None

    _connect_expire_time = None

    def __init__(self, worker):
        self.worker = worker
        self.send_buf = bytearray()
        self.recv_buf = bytearray()
        self.task_list = []

    def fetch_task_list(self):
        task_list = self.task_list
        self.task_list = []
        return task_list

    def close(self):
        if self.client:
            try:
                self.client.close()
            except:
                logger.error('exc occur.', exc_info=True)
            finally:
                self.client = None

    def closed(self):
        """
        是否关闭
        :return:
        """
        return not self.client

    def update(self):
        """
        定时操作
        :return:
        """

        while self.worker.enabled and self.closed():
            try:
                self._connect()
            except KeyboardInterrupt as e:
                # 该退出了
                return
            except:
                # 其他异常，休息后继续
                time.sleep(constants.RECONNECT_INTERVAL)
                continue
            else:
                # 连接成功
                # 设置为非阻塞
                self.client.setblocking(False)
                self._on_connected()
                break

        if not self.worker.enabled:
            return

        # 能到这里，一定是连接成功了
        if self.worker.working:
            wait_timeout = 0
        else:
            # 如果不是游戏中，就阻塞在这里，可以极大提升性能
            wait_timeout = self.worker.app.conn_timeout

        wlist = [self.client] if self.send_buf else []

        ready_to_read, ready_to_write, in_error = select.select(
            [self.client], wlist, [self.client], wait_timeout
        )

        # 有事件之后，都设置为非阻塞来读取数据
        self.client.setblocking(False)

        if ready_to_read:
            self._try_to_recv()

        if ready_to_write:
            self._try_to_send()

        if in_error:
            self.close()

        if self.recv_buf:
            self.task_list.extend(self._parse_recv_buf())

    def write(self, data):
        self.send_buf.extend(data)

    def send_now(self):
        """
        立即发送数据
        :return:
        """
        self._try_to_send()

    def _connect(self):
        """
        连接
        :return:
        """

        if ':' in self.worker.app.host:
            # IPV6
            socket_type = socket.AF_INET6
        else:
            socket_type = socket.AF_INET

        client = socket.socket(socket_type, socket.SOCK_STREAM)
        client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        client.setblocking(True)
        client.settimeout(self.worker.app.conn_timeout)

        try:
            client.connect((self.worker.app.host, self.worker.app.port))
        except Exception as e:
            client.close()
            raise e

        self.client = client

    def _parse_recv_buf(self):
        task_list = []
        offset = 0
        while offset < len(self.recv_buf):
            task = Task()
            ret = task.unpack(bytes(self.recv_buf[offset:]))
            if ret < 0:
                # 说明buf有问题
                self.recv_buf = bytearray()
                break
            elif ret == 0:
                # 没有接收完
                break
            else:
                offset += ret
                task_list.append(task)

        self.recv_buf = self.recv_buf[offset:]

        return task_list

    def _on_connected(self):
        self._ask_for_task()

    def _ask_for_task(self):
        task = Task()
        task.cmd = constants.CMD_WORKER_ASK_FOR_TASK
        task.room_id = self.worker.room_id

        self.write(task.pack())
        self.send_now()

    def _try_to_recv(self):
        while not self.closed():
            try:
                chunk = self.client.recv(self.worker.app.config['RECV_CHUNK_SIZE'])
                if not chunk:
                    self.close()
                    break

                self.recv_buf.extend(chunk)

            except socket.error as e:
                if e.errno in (errno.EINTR, errno.EAGAIN):
                    # 中断 或者 没有可读数据(非阻塞模式)
                    break
                else:
                    # Connection reset by peer 的原因说明:
                    # 网上说是对端非正常关闭连接，比如对端程序异常退出之类
                    # 我重现的方法是: C向S发送数据，如果S有回应，而C没有读取，C就调用close或者被析构的话
                    logger.error('exc occur.', exc_info=True)
                    self.close()
                    break
            except KeyboardInterrupt as e:
                # 中断
                raise e
            except:
                logger.error('exc occur.', exc_info=True)
                # 其他都直接关闭
                self.close()
                break

    def _try_to_send(self):
        """
        尝试发送，因为考虑到实时性，应该尽快发送出去
        :return:
        """

        while not self.closed() and self.send_buf:
            try:
                ret = self.client.send(self.send_buf)
                if ret < 0:
                    # 说明报错
                    break
                else:
                    self.send_buf = self.send_buf[ret:]
            except:
                logger.error('exc occur.', exc_info=True)
                break
