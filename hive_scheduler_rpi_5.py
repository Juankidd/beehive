
import time
import random
import subprocess
import Adafruit_DHT
import psutil

# Sensor configuration for DHT22
SENSOR = Adafruit_DHT.DHT22
PIN_SENSOR = 4  # GPIO pin

# ==================== Base Classes ====================
class Task:
    def __init__(self, name, priority, cpu, mem, energy, action):
        self.name = name
        self.priority = priority
        self.resources = {'cpu': cpu, 'mem': mem, 'energy': energy}
        self.action = action

class ResourceManager:
    def __init__(self, cpu_limit=90, mem_limit=800, energy=100):
        self.available = {'cpu': cpu_limit, 'mem': mem_limit, 'energy': energy}

    def can_run(self, task):
        return all(self.available[k] >= task.resources[k] for k in self.available)

    def allocate(self, task):
        for k in self.available:
            self.available[k] -= task.resources[k]

    def release(self, task):
        for k in self.available:
            self.available[k] += task.resources[k]

    def log(self):
        print(f"Available resources: {self.available}")

class TaskScheduler:
    def __init__(self, resource_manager):
        self.task_queue = []
        self.rm = resource_manager

    def add_task(self, task):
        self.task_queue.append(task)
        self.task_queue.sort(key=lambda t: t.priority)

    def run_cycle(self):
        print("\nScheduler cycle")
        self.rm.log()
        executed = []
        for task in self.task_queue:
            if self.rm.can_run(task):
                print(f"Executing: {task.name}")
                self.rm.allocate(task)
                task.action()
                time.sleep(1)
                self.rm.release(task)
                executed.append(task)
            elif task.priority == 3:
                print(f"Rescheduling: {task.name}")
        self.task_queue = [t for t in self.task_queue if t not in executed]

# ==================== Real Functions ====================
def read_sensor():
    humidity, temp = Adafruit_DHT.read_retry(SENSOR, PIN_SENSOR)
    if humidity is not None and temp is not None:
        print(f"Temp: {temp:.2f}°C | Humidity: {humidity:.2f}%")
        return temp, humidity
    else:
        print("Sensor not available")
        return None, None

def run_phi3(temp, hum):
    print("Running Phi-3.5 (Ollama)...")
    prompt = f"What recommendations can you give if the temperature is {temp:.2f} °C and the humidity is {hum:.2f}% in a beehive?"
    try:
        result = subprocess.run(["ollama", "run", "phi3", prompt], capture_output=True, text=True)
        print("Recommendation:\n", result.stdout.strip())
    except Exception as e:
        print("Error running model:", e)

def run_tinyllama(temp, hum):
    print("Running TinyLlama (Ollama)...")
    prompt = f"The beehive shows {temp:.1f} °C and {hum:.1f}% humidity. What actions should be taken?"
    try:
        result = subprocess.run(["ollama", "run", "tinyllama", prompt], capture_output=True, text=True)
        print("Recommendation:\n", result.stdout.strip())
    except Exception as e:
        print("Error running model:", e)

# ==================== Main Execution ====================
if __name__ == "__main__":
    rm = ResourceManager()
    scheduler = TaskScheduler(rm)

    def sensor_task():
        temp, hum = read_sensor()
        if temp and hum:
            # Add secondary tasks with sensor data
            scheduler.add_task(Task("SLM_Phi3", 2, 30, 300, 20, lambda: run_phi3(temp, hum)))
            scheduler.add_task(Task("SLM_TinyLlama", 3, 20, 200, 10, lambda: run_tinyllama(temp, hum)))

    # Add main sensor reading task
    scheduler.add_task(Task("Sensor reading", 1, 15, 100, 5, sensor_task))

    # Execute continuous cycles
    while True:
        scheduler.run_cycle()
        time.sleep(30)  # New cycle every 30 seconds
