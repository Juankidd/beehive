
import time
import random
import subprocess
import Adafruit_DHT
import psutil

# Configuración del sensor DHT22
SENSOR = Adafruit_DHT.DHT22
PIN_SENSOR = 4  # GPIO pin

# ==================== Clases Base ====================
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
        print(f"Disponibles: {self.available}")

class TaskScheduler:
    def __init__(self, resource_manager):
        self.task_queue = []
        self.rm = resource_manager

    def add_task(self, task):
        self.task_queue.append(task)
        self.task_queue.sort(key=lambda t: t.priority)

    def run_cycle(self):
        print("\n Ciclo del planificador")
        self.rm.log()
        executed = []
        for task in self.task_queue:
            if self.rm.can_run(task):
                print(f" Ejecutando: {task.name}")
                self.rm.allocate(task)
                task.action()
                time.sleep(1)
                self.rm.release(task)
                executed.append(task)
            elif task.priority == 3:
                print(f"Reprogramando: {task.name}")
        self.task_queue = [t for t in self.task_queue if t not in executed]

# ==================== Funciones reales ====================
def leer_sensor():
    humedad, temp = Adafruit_DHT.read_retry(SENSOR, PIN_SENSOR)
    if humedad is not None and temp is not None:
        print(f" Temp: {temp:.2f}°C |  Humedad: {humedad:.2f}%")
        return temp, humedad
    else:
        print("Sensor no disponible")
        return None, None

def ejecutar_phi3(temp, hum):
    print(" Ejecutando Phi-3.5 (Ollama)...")
    prompt = f"¿Qué recomendaciones puedes dar si la temperatura es {temp:.2f} °C y la humedad es {hum:.2f}% en una colmena?"
    try:
        result = subprocess.run(["ollama", "run", "phi3", prompt], capture_output=True, text=True)
        print(" Recomendación:\n", result.stdout.strip())
    except Exception as e:
        print(" Error ejecutando modelo:", e)

def ejecutar_tinyllama(temp, hum):
    print(" Ejecutando TinyLlama (Ollama)...")
    prompt = f"La colmena presenta {temp:.1f} °C y {hum:.1f}% humedad. ¿Qué acciones tomar?"
    try:
        result = subprocess.run(["ollama", "run", "tinyllama", prompt], capture_output=True, text=True)
        print(" Recomendación:\n", result.stdout.strip())
    except Exception as e:
        print(" Error ejecutando modelo:", e)

# ==================== Ejecución principal ====================
if __name__ == "__main__":
    rm = ResourceManager()
    scheduler = TaskScheduler(rm)

    def tarea_sensores():
        temp, hum = leer_sensor()
        if temp and hum:
            # Agregar tareas secundarias con los datos del sensor
            scheduler.add_task(Task("SLM_Phi3", 2, 30, 300, 20, lambda: ejecutar_phi3(temp, hum)))
            scheduler.add_task(Task("SLM_TinyLlama", 3, 20, 200, 10, lambda: ejecutar_tinyllama(temp, hum)))

    # Agregar tarea principal
    scheduler.add_task(Task("Lectura de sensores", 1, 15, 100, 5, tarea_sensores))

    # Ejecutar ciclos continuos
    while True:
        scheduler.run_cycle()
        time.sleep(30)  # Nuevo ciclo cada 30 segundos
