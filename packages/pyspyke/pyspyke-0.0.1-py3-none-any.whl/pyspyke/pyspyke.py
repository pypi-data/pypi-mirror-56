import psutil
import numpy
from datetime import date, time, datetime
import time
import click

def get_memory_allocation_int(percentage):
    """
    Accepts a percentage integer value and will spike memory of the system to said percentage.
    """
    return int(int((percentage/100)*psutil.virtual_memory().available)/1000000)

def spike_mem_usage(percentage, time_frame):
    """
    Loop until memory used hits 90%
    Note: This will cause memory to spike to over 90% at times, generally no more than 5-6% over. Use caution with high values and lengthy times.
    """
    if int(time_frame) == 0:
        time_sleep = int(time_frame)
        time_frame = datetime.now().strftime('%s')
    elif int(time_frame) <= 5:
        time_sleep = int((time_frame*60))
        time_frame = int(datetime.now().strftime('%s')) + int(60 * int(time_frame))
    else:
        print('This time is to great in value, please re-attempt this.')
        exit
    while int(psutil.virtual_memory().percent) <= int(percentage):
        result = [numpy.random.bytes(1024*1024) for x in range(get_memory_allocation_int(percentage))]
        if int(psutil.virtual_memory().percent) >= int(percentage) and datetime.now().strftime('%s') >= time_frame:
            break
        elif int(psutil.virtual_memory().percent) >= int(percentage) and datetime.now().strftime('%s') <= time_frame:
            time.sleep(time_sleep)
            break

@click.command()
@click.option('--time', default=0, help='Amout of time you wish to have the memory consumed.')
@click.option('--percentage', default=50, help='The percentage value you wish to spike the Memory to. i.e. 50 = 50% memory utilization.')
def main(time, percentage):
    spike_mem_usage(percentage, time)

if __name__ == '__main__':
    main()
