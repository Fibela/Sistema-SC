from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import tensorflow as tf
import numpy as np
import psutil
import subprocess
import json

# Definir el input_shape basado en la forma de los datos de entrada
input_shape = 622

# Cargar modelo usando una ruta raw string
model = tf.keras.models.load_model(r'C:\Users\TICSA\Documents\Sistema_sc\best_model.h5')

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def formulario_analisis(request):
    if request.method == "POST":
        opcion = request.POST.get('opcion')
        # Redirigir a la vista de análisis con los datos de la solicitud
        return redirect('realizar_analisis', opcion=opcion)
    return render(request, 'formulario.html')

@csrf_exempt
def realizar_analisis(request, opcion):
    if request.method == "POST":
        data = {
            "opcion": opcion,
            "data": []
        }
        resultado = analizar_equipo()
        return render(request, 'analisis.html', {'resultado': resultado})
    return redirect('formulario_analisis')

from django.shortcuts import render

def metricas_tiempo_real(request):
    return render(request, 'metricas.html')

def obtener_uso_cpu():
    return psutil.cpu_percent(interval=1)

def estado_windows_defender():
    try:
        result = subprocess.run(['powershell.exe', 'Get-MpComputerStatus | ConvertTo-Json'], capture_output=True, text=True)
        status = json.loads(result.stdout)
        return status
    except Exception as e:
        return {"error": str(e)}

def analizar_equipo():
    try:
        # Obtener métricas del sistema
        uso_cpu = obtener_uso_cpu()
        estado_defender = estado_windows_defender()

        # Realizar el análisis basado en la tabla de clasificación
        resultado_analisis = {
            'uso_cpu': uso_cpu,
            'estado_defender': estado_defender,
        }

        # Evaluar si el equipo está en peligro
        en_peligro = False
        if uso_cpu > 80:  # Por ejemplo, si el uso de CPU es mayor al 80%
            en_peligro = True
        
        # Analizar el estado de Windows Defender
        if estado_defender.get('RealTimeProtectionEnabled') == False:
            en_peligro = True

        resultado_analisis['en_peligro'] = en_peligro

        return resultado_analisis
    except Exception as e:
        return {"error": str(e)}

class PredictView(APIView):
    def post(self, request):
        try:
            data = request.data.get('data', [])
            opcion = request.data.get('opcion', 'predecir')  # Obtener la opción del cuerpo de la solicitud
            
            if opcion == 'analizar':
                resultado = analizar_equipo()
                return render(request, 'analisis.html', {'resultado': resultado})
            else:
                data = np.array(data).reshape(-1, input_shape)
                prediction = model.predict(data)
                predicted_class = np.argmax(prediction, axis=1)
                return Response({'prediction': predicted_class.tolist()}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
