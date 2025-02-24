import pandas as pd
import numpy as np

# Generar datos sintéticos similares a tus datos originales
def generar_datos_sinteticos(num_filas):
    datos_sinteticos = []
    for i in range(num_filas):
        fila = {
            'id': i + 11,  # Continuar con el id consecutivo
            'nombre': f'Malware_{i}',  # Nombre generado
            'categoria': np.random.choice(['Malware', 'Phishing', 'Interceptacion', 'Autentificacion', 'Explotacion']),
            'fecha_creacion': '2025-01-01',
            'tipo_transmision': np.random.choice(['Internet', 'Red', 'Correo electrónico', 'Memoria', 'Sistema Operativo']),
            'plataforma': np.random.choice(['Linux', 'Windows', 'Mac', 'Cualquiera']),
            'region': 'Global',
            'autor': 'Desconocido',
            'funcion': 'Robo de información',
            'objetivo': 'Robo de datos personales',
            'uso_cpu': f'{np.random.randint(0, 100)}%',
            'duracion': 'Variable',
            'ruta': np.random.choice(['Internet', 'Red', 'Dispositivos USB']),
            'nivel': np.random.randint(0, 4)
        }
        datos_sinteticos.append(fila)
    
    return pd.DataFrame(datos_sinteticos)

# Generar 10 filas de datos sintéticos
df_sinteticos = generar_datos_sinteticos(10)

# Guardar en un archivo CSV
df_sinteticos.to_csv('datos_sinteticos.csv', index=False)


def generar_manual_conceptos(df):
    categorias = df['categoria'].unique()
    manual = {}
    
    for categoria in categorias:
        manual[categoria] = df[df['categoria'] == categoria].to_dict('records')
    
    return manual

# Cargar datos originales y sintéticos
df_original = pd.read_csv('clasificacion.csv')
df_sinteticos = pd.read_csv('datos_sinteticos.csv')

# Combinar ambos conjuntos de datos
df_combinado = pd.concat([df_original, df_sinteticos], ignore_index=True)

# Seguir con el proceso de preprocesamiento y entrenamiento utilizando df_combinado


# Generar el manual basado en el DataFrame combinado
manual_conceptos = generar_manual_conceptos(df_combinado)

# Mostrar el manual
import pprint
pprint.pprint(manual_conceptos)
