import sys
sys.path.append("..") 
from extensions import scheduler

@scheduler.task('interval', id='do_job_2', seconds=5, timezone='Asia/Taipei')
def job2():
    print('Job 2 executed')
