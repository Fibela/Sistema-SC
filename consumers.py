import json
from channels.generic.websocket import WebsocketConsumer
import psutil
import subprocess
import threading
import time

class MetricasConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send_metrics()

    def disconnect(self, close_code):
        pass

    def send_metrics(self):
        def run():
            while True:
                data = obtener_metricas()
                self.send(text_data=json.dumps(data))
                time.sleep(1)  # Enviar datos cada segundo

        thread = threading.Thread(target=run)
        thread.start()

def obtener_metricas():
    uso_cpu = psutil.cpu_percent(interval=1)
    estado_defender = estado_windows_defender()
    return {
        'uso_cpu': uso_cpu,
        'estado_defender': estado_defender
    }

def estado_windows_defender():
    try:
        result = subprocess.run(['powershell.exe', 'Get-MpComputerStatus | ConvertTo-Json'], capture_output=True, text=True)
        status = json.loads(result.stdout)
        return status
    except Exception as e:
        return {"error": str(e)}
