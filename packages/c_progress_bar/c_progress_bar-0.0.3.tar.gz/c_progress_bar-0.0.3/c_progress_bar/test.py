from c_progress_bar import progress_bar
import time

for i in range(100):
    progress_bar(i+1,100)
    time.sleep(0.01)