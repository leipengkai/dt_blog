# coding=utf-8
import logging
from apscheduler.schedulers.tornado import TornadoScheduler

logger = logging.getLogger(__name__)


class TimeTask(object):
    def __init__(self, sqlalchemy_engine):
        # 调度器(scheduler):调度job
        self.scheduler = TornadoScheduler()
        # 作业存储(job store) redis, mongodb, 关系型数据库,　内存
        self.scheduler.add_jobstore("sqlalchemy", engine=sqlalchemy_engine)

    def add_cache_flush_task(self, func, *args, **kwargs):
        self.scheduler.add_job(func, 'cron', args=args, kwargs=kwargs,
                               id="cache_flush", replace_existing=True, hour=0, day='*')
        # (func,'cron', day_of_week='mon-fri', hour='0-9', minute='30-59', second='*/3')
        # 模仿cron来执行的，在周一到周五其间，每天的0点到9点，在30分到59分之间执行，执行频次为３秒
        return self

    def start_tasks(self):
        self.scheduler.start()
