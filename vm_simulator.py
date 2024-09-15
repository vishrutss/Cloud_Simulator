import time
import psutil

def simulate_vm():
    print("VM started")
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        mem_usage = psutil.virtual_memory().percent
        print(f"CPU: {cpu_usage}% | Memory: {mem_usage}%")
        time.sleep(5)

if __name__ == "__main__":
    simulate_vm()
