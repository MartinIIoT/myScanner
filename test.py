import time

with open('./last_update.conf', 'r') as f:
        dateTime_old = float(f.read())
        dateTime_now = time.time()

        dateTime_delta = dateTime_now - dateTime_old

        print(dateTime_old)
        print(dateTime_now)
        print(dateTime_delta)

