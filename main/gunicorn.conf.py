"""Gunicorn worker가 시작된 뒤 APScheduler를 구동한다.

Render의 Gunicorn preload 환경에서 Django AppConfig가 scheduler thread를 만들면
worker fork 과정에서 thread가 사라질 수 있으므로 worker hook을 사용한다.
"""


def post_worker_init(worker):
    from jobs.scheduler import start_work24_scheduler

    start_work24_scheduler()


def worker_exit(server, worker):
    from jobs.scheduler import stop_work24_scheduler

    stop_work24_scheduler()
