import time

with open('./last_update.conf', 'w') as f:
        data = str(time.time())
        f.write(data)
        time.sleep(10)