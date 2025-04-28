
import time  # Import required modules
import random  # Import required modules
import subprocess  # Import required modules
import Adafruit_DHT  # Import required modules
import psutil  # Import required modules

# Sensor configuration for DHT22
SENSOR = Adafruit_DHT.DHT22  # Define sensor type (DHT22)
PIN_SENSOR = 4  # GPIO pin  # Define GPIO pin for sensor connection

# ==================== Base Classes ====================
class Task:  # Class representing a scheduled task
    def __init__(self, name, priority, cpu, mem, energy, action):  # Initialize object attributes
        self.name = name
        self.priority = priority
        self.resources = {'cpu': cpu, 'mem': mem, 'energy': energy}
        self.action = action

class ResourceManager:  # Class for managing available system resources
    def __init__(self, cpu_limit=90, mem_limit=800, energy=100):  # Initialize object attributes
        self.available = {'cpu': cpu_limit, 'mem': mem_limit, 'energy': energy}

    def can_run(self, task):  # Check if enough resources exist to run a task
        return all(self.available[k] >= task.resources[k] for k in self.available)

    def allocate(self, task):  # Allocate resources for a running task
        for k in self.available:
            self.available[k] -= task.resources[k]

    def release(self, task):  # Release resources after a task finishes
        for k in self.available:
            self.available[k] += task.resources[k]

    def log(self):  # Print available resources
        print(f"Available resources: {self.available}")

class TaskScheduler:  # Class representing a scheduled task
    def __init__(self, resource_manager):  # Initialize object attributes
        self.task_queue = []
        self.rm = resource_manager

    def add_task(self, task):  # Add a new task to the scheduler queue
        self.task_queue.append(task)
        self.task_queue.sort(key=lambda t: t.priority)

    def run_cycle(self):  # Execute one scheduling cycle
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
def read_sensor():  # Read temperature and humidity from DHT22 sensor
    humidity, temp = Adafruit_DHT.read_retry(SENSOR, PIN_SENSOR)
    if humidity is not None and temp is not None:
        print(f"Temp: {temp:.2f}°C | Humidity: {humidity:.2f}%")
        return temp, humidity
    else:
        print("Sensor not available")
        return None, None

def run_phi3(temp, hum):  # Run the Phi-3 model using Ollama with sensor data
    print("Running Phi-3.5 (Ollama)...")
    prompt = f"What recommendations can you give if the temperature is {temp:.2f} °C and the humidity is {hum:.2f}% in a beehive?"
    try:
        result = subprocess.run(["ollama", "run", "phi3", prompt], capture_output=True, text=True)
        print("Recommendation:\n", result.stdout.strip())
    except Exception as e:
        print("Error running model:", e)

def run_tinyllama(temp, hum):  # Run the TinyLlama model using Ollama with sensor data
    print("Running TinyLlama (Ollama)...")
    prompt = f"The beehive shows {temp:.1f} °C and {hum:.1f}% humidity. What actions should be taken?"
    try:
        result = subprocess.run(["ollama", "run", "tinyllama", prompt], capture_output=True, text=True)
        print("Recommendation:\n", result.stdout.strip())
    except Exception as e:
        print("Error running model:", e)

# ==================== Main Execution ====================
if __name__ == "__main__":  # Main program execution starts here
    rm = ResourceManager()  # Initialize resource manager
    scheduler = TaskScheduler(rm)  # Initialize task scheduler with resource manager

    def sensor_task():  # Define main sensor reading task
        temp, hum = read_sensor()
        if temp and hum:
            # Add secondary tasks with sensor data
            scheduler.add_task(Task("SLM_Phi3", 2, 30, 300, 20, lambda: run_phi3(temp, hum)))  # Add task to run Phi3 model after reading sensor
            scheduler.add_task(Task("SLM_TinyLlama", 3, 20, 200, 10, lambda: run_tinyllama(temp, hum)))  # Add task to run TinyLlama model after reading sensor

    # Add main sensor reading task
    scheduler.add_task(Task("Sensor reading", 1, 15, 100, 5, sensor_task))  # Add initial sensor reading task to scheduler

    # Execute continuous cycles
    while True:  # Continuous loop to run scheduler cycles
        scheduler.run_cycle()
        time.sleep(30)  # New cycle every 30 seconds  # Wait 30 seconds between each scheduling cycle
