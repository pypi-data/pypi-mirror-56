#conding=utf-8
import sys

#进度条函数，输入当前任务以及总任务数
def progress_bar(current,subtotal,current_batch=None,total=None):
    processpercent=round((100.0*current/subtotal),2)
    sys.stdout.write('\r')
    if current_batch is not None and total is not None:
        sys.stdout.write("当前进度 %s/%s-%.2f"%(current_batch,total,processpercent)+"%")
    else:
        sys.stdout.write("当前进度 %.2f"%processpercent+"%")
    sys.stdout.flush()