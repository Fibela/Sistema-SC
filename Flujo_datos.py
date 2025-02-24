import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Función para verificar si una entrada ya existe en el archivo
def existe_entrada(entrada, csvfile):
    csvfile.seek(0)
    lector = csv.DictReader(csvfile)
    for copia in lector:
        if entrada == copia:
            return True
    return False

# Función para agregar entradas únicas
def agregar_entradas_unicas(archivo_csv, nuevas_entradas):
    with open(archivo_csv, 'a+', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'nombre', 'categoria', 'fecha_creacion', 'tipo_transmision','vectores_ataque', 'IOC(Indicadores de compromiso)', 'IF(impacto financiero)', 'Perdida_datos', 'plataforma', 'region', 'autor', 'funcion', 'objetivo', 'uso_cpu', 'duracion', 'ruta', 'nivel']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Escribir la cabecera si el archivo está vacío
        csvfile.seek(0)
        if csvfile.read(1) == '':
            writer.writeheader()
        else:
            csvfile.seek(0, 2)
        
        # Añadir las nuevas entradas si no existen
        for entrada in nuevas_entradas:
            if not existe_entrada(entrada, csvfile):
                writer.writerow(entrada)

# Lista de nuevas entradas
nuevas_entradas = [
    {'id': 1, 'nombre': 'Mirai', 'categoria': 'Malware', 'fecha_creacion': '23-11-2023', 'tipo_transmision': 'Infección en dispositivos IoT', 
     'plataforma': 'Linux', 'region': 'China, Estados Unidos, Canadá, Alemania, India, Brasil, Rusia, Pakistán', 'autor': 'Desconocido', 
     'vectores_ataque': 'Vulnerabilidades en dispositivos loT y Exploits conocidos', 'IOC(Indicadores de compromiso)': 'trafico de red inusual, comandos y control, ejecucion de comandos y escaneo de puertos', 'IF(impacto financiero)': 'Perdidas de ingresos y daño a la reputacion', 'Perdida_datos': ' No esta diseñado para robar datos', 
     'funcion': 'Crear botnets', 'objetivo': 'Crear una botnet que pueda ser controlada de manera remota y lanzar ataques DDoS', 
     'uso_cpu': '70-100%', 'duracion': 'Segundos a minutos', 'ruta': 'Internet (credenciales predeterminadas o débiles)', 'nivel': 3},
    
    {'id': 2, 'nombre': 'Phishing', 'categoria': 'Phishing', 'fecha_creacion': '02-01-1996', 'tipo_transmision': 'Correo electrónico', 
     'plataforma': 'Todos los sistemas son vulnerables', 'region': 'Todas las regiones', 'autor': 'Desconocido', 
     'vectores_ataque': 'Mensajes de texto, Redes sociales, anuncios en linea, mensajeria instantanea', 'IOC(Indicadores de compromiso)': 'Enlaces acotados o distinguidos, errores ortograficos o gramaticales, sentido de urgencia, solicitudes de informacion confidencial', 'IF(impacto financiero)': 'Perdida directa de dinero, costos de recuperacion', 'Perdida_datos': 'Informacion personal, credenciales de inicio de sesion e informacion financiera', 
     'funcion': 'Engaño y Fraude', 'objetivo': 'Robo de información personal y financiera', 
     'uso_cpu': '0-10%', 'duracion': 'Inmediata', 'ruta': 'Servicios de mensajería', 'nivel': 0},
    
    {'id': 3, 'nombre': 'Man-in-the-Middle', 'categoria': 'Interceptacion', 'fecha_creacion': '23-11-2023', 'tipo_transmision': 'Red',
     'plataforma': 'Cualquiera', 'region': 'Global', 'autor': 'Desconocido', 
     'vectores_ataque': 'Redes de Wi-Fi publicas, Proxy web, Ataques ARP, Ataques DNS', 'IOC(Indicadores de compromiso)': 'Cerificados SSL invalidos, Trafico de red inusual, cambios de contenido de las paginas web', 'IF(impacto financiero)': 'Robo de credenciales, Interceptacion de comunicaciones, alteracion de datos e infeccion de dispositivo', 'Perdida_datos': 'Informacion personal, datos corporativos confidenciales, comunicaciones privadas', 
     'funcion': 'Intercepta y manipula la comunicacion entre dos partes', 'objetivo': 'Robar informacion confidecial, alterar datos', 
     'uso_cpu': '0-20%', 'duracion': 'Continua', 'ruta': 'Capa de red', 'nivel': 3},
    
    {'id': 4, 'nombre': 'Ataque de fuerza bruta', 'categoria': 'Autentificacion', 'fecha_creacion': '24-11-2023', 'tipo_transmision': 'Red',
     'plataforma': 'Cualquiera con credenciales', 'region': 'Global', 'autor': 'Desconocido', 
     'vectores_ataque': 'Contraseñas, claves de cifrado, otros tipos de credenciales', 'IOC(Indicadores de compromiso)': 'Intentos de inicio de sesion fallidos, consumo excesivo de recursos, bloqueo de cuentas', 'IF(impacto financiero)': 'Perdida de acceso, Robo de identidad, Interrupcion de los servicios', 'Perdida_datos': 'Robo de datos personales, Borrado accidental de datos', 
     'funcion': 'Intenta adivinar contraseñas probando todas las combinaciones', 'objetivo': 'Obtener acceso no autorizado', 
     'uso_cpu': '70-100%', 'duracion': 'Variable', 'ruta': 'Protocolo de autentificacion', 'nivel': 2},
    
    {'id': 5, 'nombre': 'Escalada de privilegios', 'categoria': 'Explotacion', 'fecha_creacion': '25-11-2023', 'tipo_transmision': 'Sistema Operativo',
     'plataforma': 'Cualquier sistema operativo', 'region': 'Global', 'autor': 'Desconocido', 
     'vectores_ataque': 'Explotacion de vulnerabilidades, Configuracion incorrecta, Ataques de contraseñas, Ataques de inyeccion', 'IOC(Indicadores de compromiso)': 'Archivos o procesos inusuales, cambios en los registros del sistema, aumento de los privilegios de usuario, comportamiento anomalo de las aplicaciones', 'IF(impacto financiero)': 'Perdida de control de sistema, robo de datos, daño de sistema, uso del sistema para lanzar otros ataques', 'Perdida_datos': 'Robo de informacion confidencial, Exfiltracion de datos, modificacion de datos, borrado accidental de datos', 
     'funcion': 'Obtener acceso a niveles de permisos mas altos', 'objetivo': 'Obtener control total del sistema', 
     'uso_cpu': '50-80%', 'duracion': 'Una vez obtenido el acceso', 'ruta': 'Vulnerabilidades del sistema', 'nivel': 3},
    
    {'id': 6, 'nombre': 'Rootkit', 'categoria': 'Malware', 'fecha_creacion': '23-11-2023', 'tipo_transmision': 'SIstema operativo',
     'plataforma': 'Cualquier sistema operativo', 'region': 'Rusia, Estados Unidos, China y Corea del Norte', 'autor': 'Desconocido', 
     'vectores_ataque': 'Explotacion de vulnerabilidades, medios extraibles infectados, redes, ingenieria social', 'IOC(Indicadores de compromiso)': 'archivos ocultos, procesos inusuales, cambios en el registro del sistema, rendimiento del sistema degradado, dificultad  para instalar software de seguridad', 'IF(impacto financiero)': 'Costos de recuperacion, perdida de productividad, daños a la reputacion', 'Perdida_datos': 'Robo de datos confidenciales, borrado de datos, corrupcion de datos', 
     'funcion': 'Oculta presencia de malware en un sistema', 'objetivo': 'Mantener el acceso persistente al sistema', 
     'uso_cpu': '10-20%', 'duracion': 'Continua', 'ruta': 'Nucleo del sistema operativo', 'nivel': 4},
    
    {'id': 7, 'nombre': 'Botnet', 'categoria': 'Malware', 'fecha_creacion': '24-11-2023', 'tipo_transmision': 'Red',
     'plataforma': 'Cualquier dispositivo conectado a intetnet', 'region': 'Global', 'autor': 'Desconocido', 
     'vectores_ataque': 'Escaneo de puertos, fuerza bruta, exploits de dia cero, kits de explotacion', 'IOC(Indicadores de compromiso)': 'Aumento del trafico de red, conexiones a servidores de comando y control, ejecucion de comandos remotos', 'IF(impacto financiero)': 'Costos de mitigacion, perdida de ingresos por interrupcion de servicios', 'Perdida_datos': 'Robo de datos confidenciales, borrado de datos, corrupcion de datos', 
     'funcion': 'Red de dispositivos infectados controlados de forma remota', 'objetivo': 'Realizar ataques DDoS, enviar spam', 
     'uso_cpu': '1-100%', 'duracion': 'Continua', 'ruta': 'Cualquier servicio en red', 'nivel': 3},
    
    {'id': 8, 'nombre': 'Cryptojacker', 'categoria': 'Malware', 'fecha_creacion': '25-11-2023', 'tipo_transmision': 'Sistema operativo',
     'plataforma': 'Cualquier sistema operativo', 'region': 'Global', 'autor': 'Coinhive', 
     'vectores_ataque': 'Explotacion de vulnerabilidaes, kits de explotacion, ingenieria social', 'IOC(Indicadores de compromiso)': 'Alto uso de la CPU, lentitud dwl del sistema, aumento de la temperatura del dipositivo, generacion de monedas virtuales', 'IF(impacto financiero)': 'Aumento a los costos de energia, disminucion del rendimiento del sistema, perdida de productividad', 'Perdida_datos': 'No directamente', 
     'funcion': 'Utiliza el poder de computo del dispositivo para minar criptomonedas', 'objetivo': 'Obtener ganancias financieras usando datos privados', 
     'uso_cpu': '80-100%', 'duracion': 'Continua', 'ruta': 'Procesador del dispositivo', 'nivel': 2},
    
    {'id': 9, 'nombre': 'Ataque_CEO', 'categoria': 'Ingenieria social', 'fecha_creacion': '03-12-2023', 'tipo_transmision': 'Correo electronico',
     'plataforma': 'Cualquier correo electronico', 'region': 'Global', 'autor': 'Cibercriminales sofisticados', 
     'vectores_ataque': 'Correo electronico, telefono, plataforma de mensajeria', 'IOC(Indicadores de compromiso)': 'Solicitudes inusuales de transferencia de fondos, cambios en los proovedores, solicitudes de informacion confidencial', 'IF(impacto financiero)': 'Perdidas financieras por transferencia fraudulentas', 'Perdida_datos': 'Perdida de in formacion confiudencial, secretos comerciales', 
     'funcion': 'Suplantar la identidad de un ejecutivo de alto rango para engañar a empleados y obtener informacion confidencial', 'objetivo': 'Acceso no autorizado a sistemas o datos sensibles', 
     'uso_cpu': '10-20%', 'duracion': 'Variable', 'ruta': 'Correo electronico', 'nivel': 4},
    
    {'id': 10, 'nombre': 'Malware sin archivos', 'categoria': 'Malware', 'fecha_creacion': '04-12-2023', 'tipo_transmision': 'Memoria',
     'plataforma': 'Windows, linux', 'region': 'Global', 'autor': 'Grupos de hackers avanzados', 
     'vectores_ataque': 'Explotacion de vulnerabilidades, kits de explotacion, memorias usb infectadas', 'IOC(Indicadores de compromiso)': 'Cambios en el comportamiento del sistema, ejecucion, de procesos inusuales, dificultas para detectar malwarees', 'IF(impacto financiero)': 'Cosots de recuperacion, perdida de productividad', 'Perdida_datos': 'Robo de datos confidenciales, borrado de datos, corrupcion de datos', 
     'funcion': 'Ejecuta codigos directamente en la memoria del sistema, sin dejar archivos en el disco', 'objetivo': 'Evadir la deteccion de antivirus y comprometer sistemas', 
     'uso_cpu': 'Variable', 'duracion': 'Vaariable', 'ruta': 'Memoria del sistema', 'nivel': 3},
    
    {'id': 11, 'nombre': 'Ataque de replay', 'categoria': 'Integridad', 'fecha_creacion': '05-12-2023', 'tipo_transmision': 'Red',
    'plataforma': 'Cualquier sistema operativo', 'region': 'Global', 'autor': 'Hackers individuales',
    'vectores_ataque': 'Interceptacion de paquetes de red, ataques de repeticion', 'IOC(Indicadores de compromiso)': 'repeticion de transacciones, acceso no autorizado a cuentas, cambios en los datos transmitidos', 'IF(impacto financiero)': 'Perdida finaciera por transacciones fraudulentas', 'Perdida_datos': 'Robo de datos confidenciales trasnmitidos por la red', 
    'funcion': 'Repetir comunicaciones validas para engañar a los sistemas', 'objetivo': 'Obtener acceso no autorizado',
    'uso_cpu': '1-20%', 'duracion': 'Variable', 'ruta': 'Capa de red', 'nivel': 3},
    
    {'id': 12, 'nombre': 'Ataque de inyeccion de comandos', 'categoria': 'Ejecucion de comandos ', 'fecha_creacion': '06-12-2023', 'tipo_transmision': 'Entrada de usuario',
    'plataforma': 'Cualquier sistema operativo', 'region': 'Global', 'autor': 'Hackers con conocimientos tecnicos',
    'vectores_ataque': 'Formularios web, entradas de usuario, comandos de shell ', 'IOC(Indicadores de compromiso)': 'Ejecucion de comandos no autorizados, cambios en la base de datos, errores inesperados en las aplicaciones', 'IF(impacto financiero)': 'Perdida de datos, daños a la base de datos, costos de recuperacion, posibles multas regulatorias', 'Perdida_datos': 'Datos almacenados en la base de datos, informacion del sistema de credenciales de acceso', 
    'funcion': 'Inyectar codigo malicioso en entradas de usuario para ejecutar comandos en el servidor', 'objetivo': 'obtener acceso no autorizado',
    'uso_cpu': 'Variable', 'duracion': 'Variable', 'ruta': 'Entradas de ususario', 'nivel': 3},
    
    {'id': 13, 'nombre': 'Ataque de canal lateral', 'categoria': 'obtencion de informacion', 'fecha_creacion': '07-12-2023', 'tipo_transmision': 'Hardware',
    'plataforma': 'Cualquier sistema operativo', 'region': 'Global', 'autor': 'Grupos de hackers avanzados',
    'vectores_ataque': 'Monitoreo de la actividad del sistema, analisis de trafico de red', 'IOC(Indicadores de compromiso)': 'Fluctuaciones inusuales en el consumo de energia, emisiones electromagneticas anomalas, tiempos de ejecucion variables', 'IF(impacto financiero)': 'Perdida de propiedad intelectual, costos de investigacion y desarollo de nuevos sistemas de proteccion', 'Perdida_datos': 'Claves de cifrado, secretos comerciales, cualquier informacion que pueda esxtraerse de los datos del canal', 
    'funcion': 'Extraer informacion confidencial a traves de la medicion de caracteristicas fisicas del sistema', 'objetivo': 'obtener claves de cifrado',
    'uso_cpu': 'Variable', 'duracion': 'Continua', 'ruta': 'Hardware', 'nivel': 4},
    
    {'id': 14, 'nombre': 'Rootkit de arranque', 'categoria': 'Malware', 'fecha_creacion': '05-12-2023', 'tipo_transmision': 'firmaware',
    'plataforma': 'Sistema operativo', 'region': 'Global', 'autor': 'Grupos de hackers avanzados',
    'vectores_ataque': 'Firmaware, BIOS', 'IOC(Indicadores de compromiso)': 'Archivos ocultos, procesos ocultos, cambios en el MBR, modificaciones en controladores del dispositivo, dificultad para instalar un software de seguridad', 'IF(impacto financiero)': 'Cosotos de recuperacion, perdida de productividad, posibles multas regulatorias', 'Perdida_datos': 'Toda la informacion almacenada en el sistema comprometido, incluyendo datos personales, financieros, registros del sistema y cualquier otro archivo', 
    'funcion': 'Infecta el firmaware del sistema para obtener persistencia y control total del dispositivo', 'objetivo': 'Mantener el acceso a largo plazo y evitar la deteccion',
    'uso_cpu': '1-30%', 'duracion': 'Permanente', 'ruta': 'Firmaware del sistema', 'nivel': 4},
    
    {'id': 15, 'nombre': 'Watering hole', 'categoria': 'Ingnieria social', 'fecha_creacion': '08-12-2023', 'tipo_transmision': 'Web',
    'plataforma': 'Cualquier sistema operativo', 'region': 'Global', 'autor': 'Grupos de hackers avanzados',
    'vectores_ataque': 'Sitios web comprometidos', 'IOC(Indicadores de compromiso)': 'Redireccionamientos a sitios web maliciosos, descargas de archivos inesperadas, cambios en el comportamiento del navegador', 'IF(impacto financiero)': 'Perdida de propiedad intelectual, costos de recuperacion', 'Perdida_datos': 'Credenciales de inicio de sesion, cookies de sesion, informacion personal, datos corporativos', 
    'funcion': 'Infectar sistios web legitimos para comprometer visitantes', 'objetivo': 'infectar dispositivos  de ususarios objetivo',
    'uso_cpu': '1-30%', 'duracion': 'Variable', 'ruta': 'Sitios web comprometidos', 'nivel': 3},
    
    {'id': 16, 'nombre': 'Ataque de supply chain', 'categoria': 'Compromiso de terceros', 'fecha_creacion': '09-12-2023', 'tipo_transmision': 'Software, Hardware',
    'plataforma': 'Cualquier sistema operativo', 'region': 'Global', 'autor': 'Grupos de hackers patrocinados',
    'vectores_ataque': 'Cadena de suministros de hardware y software', 'IOC(Indicadores de compromiso)': 'Software con puertas traseras, componentes de hardware comporometidos, cambios en el comportamiento del sistema', 'IF(impacto financiero)': 'Perdidas financieras significativas, costos legales', 'Perdida_datos': 'Propiedad intelectal, datos de clientes, informacion confidencial de la empresa', 
    'funcion': 'Comprometer el software o el hardware del proveedor para infectar a sus clientes', 'objetivo': 'Distribuir malware a gran escala',
    'uso_cpu': 'Variable', 'duracion': 'Prolongada', 'ruta': 'Cadena de suministros de software', 'nivel': 4},
    
    {'id': 17, 'nombre': 'Ataque de sim swapping', 'categoria': 'Suplantacion de identidad', 'fecha_creacion': '10-12-2023', 'tipo_transmision': 'Redes moviles',
    'plataforma': 'Dispositivos moviles', 'region': 'Global', 'autor': 'cibercriminales individuales o grupos',
    'vectores_ataque': 'Proveedores de servicios moviles', 'IOC(Indicadores de compromiso)': 'Perdida de acceso al numero de telefono, transacciones fraudulentas, llamadas no reconocidas', 'IF(impacto financiero)': 'Perdida financiera por transacciones fraudulentas, costos de recuperacion de cuentas', 'Perdida_datos': 'Acceso a cuentas de correo electronico, redes sociales, banca en linea, y cualquier otra cuenta', 
    'funcion': 'Transferir el numero de telefono de una victima a un dispositivo  controlado por el atacante', 'objetivo': 'obemer acceso a cuentas en linea y cometer fraude',
    'uso_cpu': '1-25%', 'duracion': 'Variable', 'ruta': 'Proveedor de servicios moviles', 'nivel': 3},
    
    {'id': 18, 'nombre': 'Ransoware de doble extorsion', 'categoria': 'Ransomware', 'fecha_creacion': '06-12-2023', 'tipo_transmision': 'Red',
    'plataforma': 'Cualquier sistema operativo', 'region': 'Global', 'autor': 'Grupos de ransomware como LockBit, REvil',
    'vectores_ataque': 'Red, archivos locales', 'IOC(Indicadores de compromiso)': 'Cifrado de archivos, mensajes de rescate, publicacion de datos robados', 'IF(impacto financiero)': 'Costos de rescate, perdidas de datos, costos legales', 'Perdida_datos': 'Todos los datos cifrados, ademas de datos adicionales que pueden ser filtrados publicamente sino se paga el rescate', 
    'funcion': 'Cifra los archivos de la victuma y amenaza con publicarlos si no se paga el rescate', 'objetivo': 'Obtener ganancias financieras, dañar la reputacion de la victima',
    'uso_cpu': '80-100%', 'duracion': 'Variable', 'ruta': 'Red de archivos locales', 'nivel': 4},
    
    {'id': 19, 'nombre': 'Adware', 'categoria': 'Malware', 'fecha_creacion': '11-12-2023', 'tipo_transmision': 'Software y sitios web',
    'plataforma': 'Cualquier sistema operativo', 'region': 'Global', 'autor': 'Creadores de malware, redes publicitarias ilegales', 
    'vectores_ataque': 'Anuncios en linea, descarga de software, paquetes de software', 'IOC(Indicadores de compromiso)': 'Publicidad no deseada, disminucion del rendimiento del sistema, redireccionamientos a sistios web maliciosos', 'IF(impacto financiero)': 'Perdida de productividad, costos de eliminacion', 'Perdida_datos': 'No causa una perdida directa de datos, pero puede recopilar in formacion sobre los habitos de navegacion del ususario y venderla a terceros',
    'funcion': 'Mostrar anuncios no solicitados en el dispositivo del usuario', 'objetivo': 'Generar ingresos a traves de clics en anuncios',
    'uso_cpu': '1-15%', 'duracion': 'Continua', 'ruta': 'Navegador web y aplicaciones', 'nivel': 1},
    
    {'id': 20, 'nombre': 'Chipgate', 'categoria': 'Compromisos de terceros', 'fecha_creacion': '18-12-2023', 'tipo_transmision': 'Hardware',
    'plataforma': 'Cualquier sistema operativo', 'region': 'Global', 'autor': 'Estados-nacion y grupos de hackers avanzados',
    'vectores_ataque': 'Hardware comprometido', 'IOC(Indicadores de compromiso)': 'Comportamiento inusual del dispositivo, rendimiento degradado, deteccion de componentes no autorizados', 'IF(impacto financiero)': 'Costos de reemplazo de harware, perdida de confianza con los proveedores, espionaje industrial', 'Perdida_datos': 'Cualquier dato almacenado en el dispositivo comprometido, incluyendo informacion personal, corporativa y gubernamental', 
    'funcion': 'Inyectar puertas traseras en chips durante el proceso de fabricacion', 'objetivo': 'espionaje industrial, sabotaje y control a largo plazo de sistemas criticos',
    'uso_cpu': '1-100%', 'duracion': 'Persistente', 'ruta': 'Cadena de suministros de hardware', 'nivel': 4},
    
    {'id': 21, 'nombre': 'Ransomware industrial', 'categoria': 'Extorsion', 'fecha_creacion': '20-12-2023', 'tipo_transmision': 'Redes industriales y redes SCADA',
    'plataforma': 'Sistemas de control insdutrial(SCADA), ICS', 'region': 'Global', 'autor': 'Grupos de ransomware especializados',
    'vectores_ataque': 'Sistemas de control industrial(SCADA)', 'IOC(Indicadores de compromiso)': 'Disrupcion en los procesos industriales, cambios en los registros de eventos, cifrado de archivos en sistemas industriales, Presencia de malware en dispositivos industriales', 'IF(impacto financiero)': 'Disrupcion de procesos industriales, parada de produccion, daños a los equipos', 'Perdida_datos': 'Datos de produccion, registros de mantenimiento, planos de diseño de informacion confidencial de la empresa', 
    'funcion': 'Cifrar datos de un sistema industrial y exigir un rescate para restaurar el acceso', 'objetivo': 'Causar interrupciones en servicios esenciales(energia, agua, transporte)',
    'uso_cpu': '75-100%', 'duracion': 'Variable', 'ruta': 'Redes industriales', 'nivel': 4},
    
    {'id': 22, 'nombre': 'Deepfake', 'categoria': 'Ingenieria social', 'fecha_creacion': '21-12-2023','tipo_transmision': 'Redes sociales',
    'plataforma': 'Redes sociales, aplicaciones de mensajeria', 'region': 'Global', 'autor': 'Individuos, grupos, estados-nacion', 
    'vectores_ataque': 'Redes sociales, plataformas de video, sitios web', 'IOC(Indicadores de compromiso)': 'Incoherencia en los movimientos faciales, problemas de iluminacion, falta de sincronizacion entre audio y video', 'IF(impacto financiero)': 'Videos o audios falsos, difamacion, manipulacion de la opinion publica', 'Perdida_datos': 'Reputacion de individuos y organizaciones, confianza en la informacion, resultado de elecciones, seguridad nacional', 
    'funcion': 'Crear contenido falso, como videos o audios, para engañar a las personas', 'objetivo': 'Difundir desinformacion, manipula la opinion publica, cometer fraude',
    'uso_cpu': '70-100%', 'duracion': 'Variable', 'ruta': 'Redes sociales, aplicaciones de mensajeria', 'nivel': 3},
    
    {'id': 23, 'nombre': 'Watering hole para la industria farmaceutica', 'categoria': 'ingenieria social', 'fecha_creacion': '22-12-2023', 'tipo_transmision': 'Paginas web de la insutria farmaceutica',
     'plataforma': 'Sitios web de la industria', 'region': 'Global', 'autor': 'Grupos de espionaje insutrial ',
    'vectores_ataque': 'Sitios web de la industria farmaceutica', 'IOC(Indicadores de compromiso)': 'Infecciones dirigidas a investigadores, robos de propiedad intelectual', 'IF(impacto financiero)': 'Perdida de propiedad intelectual, ventajas competitivas', 'Perdida_datos': 'Formulas farmaceuticas, datos de investigacion, informacion de pacientes, secretos comerciales', 
    'funcion': 'Infectar sitios web utilizados por la industria farmaceutica para robar propiedad intelectual', 'objetivo': 'Robo de secretos comerciales, ventaja competitiva',
    'uso_cpu': '10-20%', 'duracion': 'Variable', 'ruta': 'Sitios web de la industria farmaceutica', 'nivel': 4},
    
    {'id': 24, 'nombre': 'Waterfox', 'categoria': 'Malware', 'fecha_creacion': '25-12-2023', 'tipo_transmision': 'Descarga, explotacion',
    'plataforma': 'Windows, MacOs', 'region': 'Global', 'autor': 'Grupos de cibercriminales',
    'vectores_ataque': 'Explotacion de vulnerabilidades en navegadores, ingenieria social', 'IOC(Indicadores de compromiso)': 'Procesos inusuales, consumo excesivo de recursos, redireccionamientos', 'IF(impacto financiero)': 'Perdida de productividad, robo de datos', 'Perdida_datos': 'Perdida de productividad',
    'funcion': 'Secuestro del navegador', 'objetivo': 'robo de credenciales',
    'uso_cpu': '50-100%', 'duracion': 'Alto', 'ruta': 'Navegador', 'nivel': 4},
    
    {'id': 25, 'nombre': 'Evil Twin', 'categoria': 'Ataque de red', 'fecha_creacion': '26-12-2023', 'tipo_transmision': 'Wi-Fi',
    'plataforma': 'Todos los sistemas operativos', 'region': 'Global', 'autor': 'Hackers individuales',
    'vectores_ataque': 'Creaciones de redes Wi-Fi falsas', 'IOC(Indicadores de compromiso)': 'Interceptacion de trafico, autenticacion en redes falsas', 'IF(impacto financiero)': 'Robo de credenciales, ataques de pishing', 'Perdida_datos': 'Robo de credenciales',
    'funcion': 'Robo de datos', 'objetivo': 'ataques de MITM',
    'uso_cpu': '1-15%', 'duracion': 'Continuo', 'ruta': 'Capa de enlace de datos', 'nivel': 3},
    
    {'id': 26, 'nombre': 'Keylogger', 'categoria': 'Spyware', 'fecha_creacion': '27-12-2023', 'tipo_transmision': 'Software',
    'plataforma': 'Cualquier sistema operativo', 'region': 'Global', 'autor': 'Cibercriminales individuales',
    'vectores_ataque': 'Registro de pulsaciones de teclas', 'IOC(Indicadores de compromiso)': 'Desempeño lento del sistema, procesos desconocidos', 'IF(impacto financiero)': 'Robo de informacion personal', 'Perdida_datos': 'Robo de contraseñas',
    'funcion': 'Acceso al software', 'objetivo': 'Robo de credenciales',
    'uso_cpu': '1-20%', 'duracion': 'Continuo', 'ruta': 'Kernel, controladores de teclado', 'nivel': 3},
    
    {'id': 27, 'nombre': 'ataque de sim swapping con criptomoneda', 'categoria': 'Suplatacion de identidad', 'fecha_creacion': '04-01-2024', 'tipo_transmision': 'Redes moviles',
    'plataforma': 'Cualquier sistema operativo', 'region': 'Global', 'autor': 'cibercriminales especializado',
    'vectores_ataque': 'Ingenieria social, corrupcion de empleados de operadores moviles', 'IOC(Indicadores de compromiso)': 'Perdida de acceso a numero de telefono', 'IF(impacto financiero)': 'transacciones fraudulentas, perdida financiera', 'Perdida_datos': 'robo de identidad',
    'funcion': 'Acceso de cuentas', 'objetivo': 'Robo de criptomoneda',
    'uso_cpu': '1-25%', 'duracion': 'Temporal', 'ruta': 'Redes moviles', 'nivel': 4},
    
    {'id': 28, 'nombre': 'Ataque de supply chain de firmaware', 'categoria': 'Compromiso de terceros', 'fecha_creacion': '03-01-2023', 'tipo_transmision': 'Hardware',
    'plataforma': 'Cualquier sistema operativo', 'region': 'Global', 'autor': 'Estados-nacion',
    'vectores_ataque': 'Compromiso de la cadena de suministros de hardware', 'IOC(Indicadores de compromiso)': 'Comportamiento anormal del dispositivo, dificultad para detectar y eliminar el malware', 'IF(impacto financiero)': 'Perdida de control de dispositivos, espionaje industrial', 'Perdida_datos': 'Dispositivos loT, servidores',
    'funcion': 'infeccion del proveedor', 'objetivo': 'Control a largo plazo de dispositivos',
    'uso_cpu': '1-100%', 'duracion': 'Permanente', 'ruta': 'Firmaware', 'nivel': 5},
    
    {'id': 29, 'nombre': 'Waterholing', 'categoria': 'Ingenieria social', 'fecha_creacion': '05-01-2024', 'tipo_transmision': 'Web',
    'plataforma': 'Cualquier sistema operativo', 'region': 'Global', 'autor': 'Grupos de cibercriminales organizados',
    'vectores_ataque': 'Explotacion de vulnerabilidades en sistios web financieros, pishing', 'IOC(Indicadores de compromiso)': 'Redireccionamientos a sitios falsos, descargas de malwares', 'IF(impacto financiero)': 'Perdida financiera, daño a la reputacion', 'Perdida_datos': 'Credenciales de acceso, informacion financiera',
    'funcion': 'Robo de credencial', 'objetivo': 'fraude financiero',
    'uso_cpu': '1-20%', 'duracion': 'Continua', 'ruta': 'Sitios web', 'nivel': 4},
    
    {'id': 30, 'nombre': 'Ataque de dia cero', 'categoria': 'Explotacion', 'fecha_creacion': '06-01-2024', 'tipo_transmision': 'Software',
    'plataforma': 'Cualquier sistema operativo', 'region': 'Global', 'autor': 'Hackers avanzados',
    'vectores_ataque': 'Vulnerabilidades desconocidas', 'IOC(Indicadores de compromiso)': 'Comportamiento anormal del software, fallas del sistema', 'IF(impacto financiero)': 'Interrupcion del servicio', 'Perdida_datos': 'Datos de servicios',
    'funcion': 'Obtener acceso no autorizado', 'objetivo': 'causar daño',
    'uso_cpu': '1-100%', 'duracion': 'Temporal', 'ruta': 'Software vulnerable', 'nivel': 5},
    
    {'id': 31, 'nombre': 'Ransomware de doble extorsion con fuga de datos', 'categoria': 'Ransomware', 'fecha_creacion': '07-01-2024', 'tipo_transmision': 'Red',
    'plataforma': 'Cualquier sistema operativo', 'region': 'Global', 'autor': 'Grupos de ransomware organizados',
    'vectores_ataque': 'Cifrado de archivos, filtracion de datos', 'IOC(Indicadores de compromiso)': 'Mensajes de rescate, publicacion de datos robados en la dark web', 'IF(impacto financiero)': 'Pago de rescate, daños y perjuicios y multas regulatorias', 'Perdida_datos': 'Todos los datos cifrados, datos publicados en la dark web',
    'funcion': 'Obtener rescate', 'objetivo': 'causar daño',
    'uso_cpu': '80-100%', 'duracion': 'Continua', 'ruta': 'Archivos del sistema, servidores de archivos', 'nivel': 5},
    
    {'id': 32, 'nombre': 'Ataque de cache poisoning', 'categoria': 'Envenamiento de cache', 'fecha_creacion': '12-01-2024', 'tipo_transmision': 'DNS',
    'plataforma': 'Servidores DNS', 'region': 'Global', 'autor': 'Hackers con conocimientos de redes',
    'vectores_ataque': 'Modificacion de registros DNS', 'IOC(Indicadores de compromiso)': 'Redireccionamientos a sitios maliciosos', 'IF(impacto financiero)': 'Perdida de datos, daño a la reputacion', 'Perdida_datos': 'cache',
    'funcion': 'Credenciales de acceso', 'objetivo': 'Robo de credenciales, pishing',
    'uso_cpu': '1-20%', 'duracion': 'Continua', 'ruta': 'Servidores DNS', 'nivel': 3},
    
    {'id': 33, 'nombre': 'Ataque de pass-the-hash', 'categoria': 'Escalada de privilegios', 'fecha_creacion': '13-01-2024', 'tipo_transmision': 'Redes corporativas',
    'plataforma': 'Dominios Active Directory', 'region': 'Empresas', 'autor': 'Hackers con conocimientos de Active Directory',
    'vectores_ataque': 'Robo de hashes de contraseñas, utilizacion de herramientas de cracking', 'IOC(Indicadores de compromiso)': 'Acceso a cuentas con privilegios elevados', 'IF(impacto financiero)': 'Perdida de control de sistemas, robo de datos', 'Perdida_datos': 'Identidad virtual',
    'funcion': 'suplantacion de identidad', 'objetivo': 'Obtener acceso a sistemas con mayores privilegios',
    'uso_cpu': '1-10%', 'duracion': 'Variable', 'ruta': 'Dominios Active Directory', 'nivel': 4},
    
    {'id': 34, 'nombre': 'Ataque de zerologon', 'categoria': 'Explotacion de vulnerabilidades', 'fecha_creacion': '14-01-2024', 'tipo_transmision': 'Protocolo SMB',
    'plataforma': 'Windows', 'region': 'Global', 'autor': 'Grupos de hackers avanzados',
    'vectores_ataque': 'Explotacion de vulnerabilidades CVE-2020-1472', 'IOC(Indicadores de compromiso)': 'Acceso no autenticado a sistemas Windows', 'IF(impacto financiero)': 'Robo de datos, control remoto de sistemas', 'Perdida_datos': 'Informacion personal',
    'funcion': 'Credenciales de administrador de dominios Active Directory', 'objetivo': 'Obtener acceso a dominios Active Directory',
    'uso_cpu': '1-20%', 'duracion': 'Permanente', 'ruta': 'Protocolo SMB', 'nivel': 5},
    
    {'id': 35, 'nombre': 'Ataque de replay de credenciales', 'categoria': 'Interceptacion', 'fecha_creacion': '10-01-2024', 'tipo_transmision': 'Red',
    'plataforma': 'Cualquier sistema operativo', 'region': 'Global', 'autor': 'Hackers individuales',
    'vectores_ataque': 'Interceptacion de trafico, almacenamiento de credenciales', 'IOC(Indicadores de compromiso)': 'Repeticiones de sesiones, acceso no autorizado', 'IF(impacto financiero)': 'Perdida financiera, daño a la reputacion', 'Perdida_datos': 'control de cuenta, informacion personal',
    'funcion': 'Credenciales de acceso', 'objetivo': 'Obtener acceso no autorizado',
    'uso_cpu': '1-15%', 'duracion': 'Variable', 'ruta': 'Capa de red', 'nivel': 3},
    
    {'id': 36, 'nombre': 'Ataque de inyeccion de SQL ciega', 'categoria': 'Inyeccion', 'fecha_creacion': '11-01-2024', 'tipo_transmision': 'Aplicaciones Web',
    'plataforma': 'InterWeb', 'region': 'Global', 'autor': 'Hackers con conocimientos tecnicos',
    'vectores_ataque': 'Analisis de la respuesta del servidor', 'IOC(Indicadores de compromiso)': 'Robo de datos, modificacion de datos', 'IF(impacto financiero)': 'N/A', 'Perdida_datos': 'Todo tipo de documentos',
    'funcion': 'Ejecuccion de comandos de manera remota', 'objetivo': 'Obtener acceso a la base de datos',
    'uso_cpu': '1-100%', 'duracion': 'Variable', 'ruta': 'Base de datos', 'nivel': 4},
    
    {'id': 37, 'nombre': 'Ataque de sim swapping con criptomoneda(variable)', 'categoria': 'Suplantacion de identidad', 'fecha_creacion': '18-01-2024', 'tipo_transmision': 'Redes moviles',
    'plataforma': 'Culaquier sistema operativo', 'region': 'Global', 'autor': 'Cibercriminales especializados',
    'vectores_ataque': 'Ingenieria social, sim swapping, pishing', 'IOC(Indicadores de compromiso)': 'Perdida de acceso al numero de telefono, transacciones fraudulentas', 'IF(impacto financiero)': 'Perdida financiera, robo de identidad', 'Perdida_datos': 'Control de usuario en servicio de llamada y mensajeria',
    'funcion': 'Acceso a cuentas en linea', 'objetivo': 'Robo de criptomonedas',
    'uso_cpu': '10-20%', 'duracion': 'Temporal', 'ruta': 'Redes moviles, aplicaciones de mensajeria', 'nivel': 4},
    
    {'id': 38, 'nombre': 'Ransomware como servicio(RaaS)', 'categoria': 'Ransomware', 'fecha_creacion': '02-02-2024', 'tipo_transmision': 'Varias',
    'plataforma': 'Cualquier sistem operativo', 'region': 'Global', 'autor': 'Grupos cibercriminales',
    'vectores_ataque': 'Afiliacion a redes de ransomware', 'IOC(Indicadores de compromiso)': 'Cifrado de archivos, mensajes de rescate', 'IF(impacto financiero)': 'Perdida financiera, dañoa la reputacion', 'Perdida_datos': 'Todos los datos cifrados',
    'funcion': 'Cifrar archivos', 'objetivo': 'Extorsionar a las victimas',
    'uso_cpu': '1-100%', 'duracion': 'Permanente', 'ruta': 'Depende del vector de ataque', 'nivel': 4},
    
    {'id': 39, 'nombre': 'Ataque de contenedores', 'categoria': 'Explotacion', 'fecha_creacion': '05-02-2024', 'tipo_transmision': 'Red, contenedores',
    'plataforma': 'Cualquier sistema operativo', 'region': 'Global', 'autor': 'Grupos de hackers',
    'vectores_ataque': 'Explotacion de vulnerabilidades en contenedores, configuracion correcta', 'IOC(Indicadores de compromiso)': 'Procesos inusuales en contenedores, aumento en los uso de recursos', 'IF(impacto financiero)': 'Perdida de datos interrupcion de servicios', 'Perdida_datos': 'Datos confidenciales almacenados en contenedores',
    'funcion': 'Obtener acceso no autorizado a contenedores', 'objetivo': 'Ejecutar codigo malicioso',
    'uso_cpu': '1-100%', 'duracion': 'Temporal', 'ruta': 'Docke, Kubernetes', 'nivel': 4},
    
    {'id': 40, 'nombre': 'Ataque de watering hole dirigido a la industria energetica', 'categoria': 'Ingenieria social', 'fecha_creacion': '09-02-2024', 'tipo_transmision': 'Web',
    'plataforma': 'Cualquier sistema operativo', 'region': 'Global', 'autor': 'Grupos de espionaje industrial',
    'vectores_ataque': 'Explotacion de vulnerabilidades en sitios web de la industria energetica', 'IOC(Indicadores de compromiso)': 'Redireccionamiento a sitios maliciosos, descargas de malwares', 'IF(impacto financiero)': 'Perdida de propiedad intelectual, daños a reputacion, interrupcion de servicios', 'Perdida_datos': 'Datos confidenciales de la industria energetica, planos de infraestructura',
    'funcion': 'Robo de propiedad intelectual', 'objetivo': 'sabotaje',
    'uso_cpu': '1-20%', 'duracion': 'Continua', 'ruta': 'Sitios web comprometidos', 'nivel': 4},
    
    {'id': 41, 'nombre': 'Ataque de pishing de CEO dirigido a proveedores', 'categoria': 'Ingenieria social', 'fecha_creacion': '07-02-2024', 'tipo_transmision': 'Correo electronico',
    'plataforma': 'Cualquier sistema operativo', 'region': 'Global', 'autor': 'Cibercriminales',
    'vectores_ataque': 'Suplantacion de identidad de ejecutivos, solicitudes de pago falsas', 'IOC(Indicadores de compromiso)': 'Transferencias bancarias no autorizadas, cambios en los proveedores', 'IF(impacto financiero)': 'Perdida financieras significativas', 'Perdida_datos': 'informacion financiera, datos de proveedores',
    'funcion': 'Interrupcion de la cadena de suministros', 'objetivo': 'Robo de fondos',
    'uso_cpu': '5-20%', 'duracion': 'Una vez', 'ruta': 'Correo electronico', 'nivel': 4},
    
    {'id': 42, 'nombre': 'Ataque de side-channel a servicios en la nube', 'categoria': 'Obtencion de informacion', 'fecha_creacion': '11-02-2024', 'tipo_transmision': 'Nube',
    'plataforma': 'Servicios de la nube(AWS, Azure, GCP)', 'region': 'Global', 'autor': 'Investigadores cibercriminales avanzados',
    'vectores_ataque': 'Monitoreo de patrones de trafico, analisis de tiempos de respuesta', 'IOC(Indicadores de compromiso)': 'Filtracion de informacion sensible, descifrado de claves', 'IF(impacto financiero)': 'Perdida de datos confidenciales, violacion a la privacidad', 'Perdida_datos': 'Informacion personal y sensible',
    'funcion': 'Decodificacion de claves', 'objetivo': 'Obtener informacion confidencial',
    'uso_cpu': '1-100%', 'duracion': 'Continua', 'ruta': 'Trafico de red, tiempos de respuesta', 'nivel': 5},
    
    {'id': 43, 'nombre': 'Ataque de pishing especifico para la nube', 'categoria': 'Ingenieria social', 'fecha_creacion': '13-02-2024', 'tipo_transmision': 'Correo electronico, aplicaciones de colaboracion',
    'plataforma': 'Plataformas de la nube(Office 365, G Suite)', 'region': 'Global', 'autor': 'cibercriminales',
    'vectores_ataque': 'Suplantacion de identidad, enlaces maliciosos', 'IOC(Indicadores de compromiso)': 'Credenciales robadas, acceso no autorizado a cuentas de la nube', 'IF(impacto financiero)': 'Perdida de datos, daño a la reputacion', 'Perdida_datos': 'Informacion privada',
    'funcion': 'Falsificacion y suplantar identidad', 'objetivo': 'Obtener acceso a cuentas de la nube',
    'uso_cpu': '1-10%', 'duracion': 'Continua', 'ruta': 'Correo electronico, aplicaciones de colaboracion', 'nivel': 3},
    
    {'id': 44, 'nombre': 'Ataque de inyecccion de SQL en base de datos de la nube', 'categoria': 'Inyeccion', 'fecha_creacion': '14-02-2024', 'tipo_transmision': 'Aplicaciones web',
    'plataforma': 'Base de datos de la nube(AWS RDS, Azure SQL)', 'region': 'Global', 'autor': 'Hackers con conocimientos tecnicos',
    'vectores_ataque': 'Explotacoin de vulnerabilidades en aplicaciones web', 'IOC(Indicadores de compromiso)': 'Modificacion de datos de la base de datos, ejecucion de comandos arbitrarios', 'IF(impacto financiero)': 'Perdida de datos, daño la base de datos', 'Perdida_datos': 'Claves y codigos',
    'funcion': 'Obtener acceso a la base de datos', 'objetivo': 'modificar o eliminar datos',
    'uso_cpu': '1-100%', 'duracion': 'Temporal', 'ruta': 'Base de datos de la nube', 'nivel': 4},
    
    {'id': 45, 'nombre': 'Ataque de inyeccion de comando en funciones de Lambda', 'categoria': 'Inyeccion', 'fecha_creacion': '15-02-2024', 'tipo_transmision': 'HTTP',
    'plataforma': 'AWS Lambda', 'region': 'Global', 'autor': 'Hackers con conocimientos tecnicos',
    'vectores_ataque': 'Explotacion de vulnerabilidades en funciones Lambda, Inyeccion de comandos no autorizados', 'IOC(Indicadores de compromiso)': 'Ejecucion de comandos no autorizados, cambios en la configuracion de la funcion', 'IF(impacto financiero)': 'Perdida de datos, secuestro de la funcion', 'Perdida_datos': 'Perdida del control en funcion',
    'funcion': 'Obtener acceso a recursos  del sistema subadyacente', 'objetivo': 'Ejecutar comandos Lambda',
    'uso_cpu': '1-100%', 'duracion': 'Temporal', 'ruta': 'Entorno de ejecucion de Lambda', 'nivel': 4},
    
    {'id': 46, 'nombre': 'Ataque de denegacion de servidores a funcion Serverless', 'categoria': 'Denegacion de servicio', 'fecha_creacion': '16-02-2024', 'tipo_transmision': 'HTTP',
    'plataforma': 'Plataformas serverless(AWS Lambda, Azure Functions)', 'region': 'Global', 'autor': 'Grupos de Hackers, competidores',
    'vectores_ataque': 'Envio de un gran numero de solicitudes, explotacion de vulnerabilidades', 'IOC(Indicadores de compromiso)': 'Aumento de trafico, latencia elevada, errores 502/503', 'IF(impacto financiero)': 'Perdida de ingresos, daño a la reputacion', 'Perdida_datos': 'No hay perdida directa de datos',
    'funcion': 'Sobrecargar el servidor', 'objetivo': 'Interrupcion del servicio',
    'uso_cpu': '50-100%', 'duracion': 'Mientras dure el ataque', 'ruta': 'Capa de aplicacion', 'nivel': 3},
    
    {'id': 47, 'nombre': 'Ataque de exfiltracion de datos a traves de funciones Serveless', 'categoria': 'Exfiltracion de datos', 'fecha_creacion': '17-02-2024', 'tipo_transmision': 'HTTP',
    'plataforma': 'Plataformas serveless(AWS Lambda, Azure Functions)', 'region': 'Global', 'autor': 'Cibercriminales',
    'vectores_ataque': 'Explotacion de vulnerabilidades en funciones serverless, configuracion incorrecta de permisos', 'IOC(Indicadores de compromiso)': 'Trasnferencia de datos a servidores externos, aumento del trafico de salida', 'IF(impacto financiero)': 'Perdida de datos confidenciales, daños a la reputacion', 'Perdida_datos': 'Datos confidenciales',
    'funcion': 'Ingreso Ilegal', 'objetivo': ' Robo de datos',
    'uso_cpu': '1-100%', 'duracion': 'Continua o Intermitente', 'ruta': 'Red, almacenamiento interno', 'nivel': 4},
    
    {'id': 48, 'nombre': 'Ataque de side-channel a funciones Serverless', 'categoria': 'Obtencion de informacion', 'fecha_creacion': '18-02-2024', 'tipo_transmision': 'Nube',
    'plataforma': 'Plataformas serverless(AWS Lambda, Azure Functions)', 'region': 'Global', 'autor': 'Investigadores, cibercriminales avanzados',
    'vectores_ataque': 'Monitoreo de patrones de ejecucion de funciones, analisis de tiempos de respuesta', 'IOC(Indicadores de compromiso)': 'Filtracion de informacion sensible, descifrado de claves', 'IF(impacto financiero)': 'Daño a la reputacion', 'Perdida_datos': 'Perdida de datos confidenciales, violacion a la privacidad',
    'funcion': 'Ejecuion de comandos de forma remota', 'objetivo': 'obtener informacion sensible',
    'uso_cpu': '1-100%', 'duracion': 'Continua', 'ruta': 'Entorno de ejecucion de funciones', 'nivel': 4},
    
    {'id': 49, 'nombre': 'Ataque de inyeccion de dependencia en funciones Serverless', 'categoria': 'Inyeccion', 'fecha_creacion': '19-02-2024', 'tipo_transmision': 'HTTP',
    'plataforma': 'Pltaformas serverless(AWS Lambda, Azure Functions)', 'region': 'Global', 'autor': 'Hckers con conocimientos tecnicos',
    'vectores_ataque': 'Explotacion de vulnerabilidades en bibliotecas y frameworks utilizados por las funciones', 'IOC(Indicadores de compromiso)': 'Ejecucion de codigo arbitrario, acceso a recursos del sistema', 'IF(impacto financiero)': 'Secuestro de la funcion', 'Perdida_datos': 'Perdida de datos sobre la funcion',
    'funcion': 'Acceder a la interfaz de una funcion', 'objetivo': 'Obtener acceso a recursos del sistema subadyacente',
    'uso_cpu': '1-100%', 'duracion': 'Temporal', 'ruta': 'Entorno de ejecucion de funciones', 'nivel': 4},
    
    {'id': 50, 'nombre': 'Ataque de demegacion de servicio a base de datos', 'categoria': 'Denegacion de servicio', 'fecha_creacion': '22-02-2024', 'tipo_transmision': 'Bases de datos',
    'plataforma': 'Culaquier sistema operativo', 'region': 'Global', 'autor': 'Hackers, competidores',
    'vectores_ataque': 'Envio de gran numero de consultas, explotacion de vulnerabilidades', 'IOC(Indicadores de compromiso)': 'Disminucion del rendimiento de la base de datos, indisponibilidad  del servicio', 'IF(impacto financiero)': 'Perdida de ingresos, daño la reputacion', 'Perdida_datos': 'Perdida del soporte en la base de datos, no hay perdida directa de datos',
    'funcion': 'Saturar el sistema de la base de datos', 'objetivo': 'Interrupcion del servicio',
    'uso_cpu': '80-100%', 'duracion': 'Mientras dure el ataque', 'ruta': 'Base de datos', 'nivel': 3},
    
    {'id': 51, 'nombre': 'NetWalker', 'categoria': 'Ransomware', 'fecha_creacion': '01-01-2019', 'tipo_transmision': 'Descarga',
    'plataforma': 'Windows', 'region': 'Global', 'autor': 'Grupo de hackers NetWalker',
    'vectores_ataque': 'Pishing, explotar vilnerabilidades', 'IOC(Indicadores de compromiso)': 'Procesos sospechosos en ejecucion, conexion de red a servidores desconocidos, claves de registro modificadas, mensajes de rescate en el escritorio', 'IF(impacto financiero)': 'Perdidas millonarias para empresas y organizadores', 'Perdida_datos': 'Encriptado de archivos, posible perdida de datos si no se paga el rescate',
    'funcion': 'Encriptar archivos y exigir un rescate para su recuperacion', 'objetivo': 'obtener ganancias financieras',
    'uso_cpu': '80-100%', 'duracion': 'Continua', 'ruta': 'Red', 'nivel': 4},
    
    {'id': 52, 'nombre': 'REvil(Sodinokibi)', 'categoria': 'Ransmoware', 'fecha_creacion': '01-01-2019', 'tipo_transmision': 'Descarga',
    'plataforma': 'Windows, Linux', 'region': 'Global', 'autor': 'Grupo de hackers REvil',
    'vectores_ataque': 'Pishing, explotacion de vulnerabilidades, ataque de fuerza bruta', 'IOC(Indicadores de compromiso)': 'Archivos encriptados con extensiones especificas(ej.revil)', 'IF(impacto financiero)': 'Perdidas millonarias para empresas y organizaciones', 'Perdida_datos': 'Encriptacion de archivos, posible perdida de datos si no se paga rescate',
    'funcion': 'Encriptar archivos y exigir un rescate para su recuperacion', 'objetivo': 'Obtener ganancias financieras',
    'uso_cpu': '80-100%', 'duracion': 'Continua', 'ruta': 'Red', 'nivel': 4},

    {'id': 53, 'nombre': 'Maze', 'categoria': 'Ransomware', 'fecha_creacion': '01-01-2019', 'tipo_transmision': 'Descarga',
    'plataforma': 'Windows', 'region': 'Global', 'autor': 'Grupo de hackers Maze',
    'vectores_ataque': 'Pishing, Explotar vulnerabilidades', 'IOC(Indicadores de compromiso)': 'Procesos sospechoso en ejecucion, claves de registro modificadas, mensajes de rescate en el escritorio o en el archivo de texto', 'IF(impacto financiero)': 'Perdidas millonarias para empresas y organizaciones', 'Perdida_datos': 'Emcriptacion de datos, posible perdida de datos si no se pagan el rescate',
    'funcion': 'Encriptar archivos y exigir un rescate para su recuperacion, y amenazar con publicar datos si no se paga el rescate', 'objetivo': 'obtener ganancias financieras y dañar la reputacion de la victima',
    'uso_cpu': '80-100%', 'duracion': 'Continua', 'ruta': 'Red', 'nivel': 4},

    {'id': 54, 'nombre': 'WannaCry', 'categoria': 'Ransomware', 'fecha_creacion': '01-01-2017', 'tipo_transmision': 'Gusano',
    'plataforma': 'Windows', 'region': 'Global', 'autor': 'Shadow Brokers(Se cree robado a la nasa)',
    'vectores_ataque': 'Explotacion de vilnerabilidades EternalBlue en Windows', 'IOC(Indicadores de compromiso)': 'Archivos encriptados con la extension .wcry, Procesos sospechosos', 'IF(impacto financiero)': 'Millones de dolares en perdidas, interrupcion de servicios', 'Perdida_datos': 'Encriptacion de archivos, posible perdida si no se paga el rescate',
    'funcion': 'Encriptar archivos y exigir un rescate para su recuperacion', 'objetivo': 'obtener ganancias financieras',
    'uso_cpu': '80-100%', 'duracion': 'Continua o intermitente', 'ruta': 'Redes locales y a traves de internet', 'nivel': 4},

    {'id': 55, 'nombre': 'Emotet', 'categoria': 'Troyano bancario', 'fecha_creacion': '01-01-2014', 'tipo_transmision': 'Correo electronico, archivos adjuntos maliciosos',
    'plataforma': 'Windows', 'region': 'Global', 'autor': 'Grupos de Hackers Emotet',
    'vectores_ataque': 'Correos electronicos con archivos adjuntos maliciosos', 'IOC(Indicadores de compromiso)': 'Comportamiento inusual del sistema, Procesos sospechosos, Trafico de red inusual, Robo de credenciales bancarias', 'IF(impacto financiero)': 'Robo de fondos de cuentas bancarias', 'Perdida_datos': 'Robo de credenciales, posible acceso a informacion personal',
    'funcion': 'Robar credenciales bancarias y otra informacion sensible', 'objetivo': 'ontener ganacias finacieras',
    'uso_cpu': '1-100%', 'duracion': 'Intermitente', 'ruta': 'Correo electronico y redes', 'nivel': 4},

    {'id': 56, 'nombre': 'Exploir de dia cero generico', 'categoria': 'Explotacion de vulnerabilidades', 'fecha_creacion': '01-01-2024', 'tipo_transmision': 'Todas',
    'plataforma': 'Cualquier sistema operativo', 'region': 'Global', 'autor': 'Investigadores o atacantes',
    'vectores_ataque': 'Aprovechamiento de vulnerabilidades desconocidas', 'IOC(Indicadores de compromiso)': 'Comportamiento inusual del sistema, fallos inesperados, actividad sospechosa en la red', 'IF(impacto financiero)': 'Variable', 'Perdida_datos': 'Potencial robo o modificacion de datos',
    'funcion': 'Aprovechar una vulnerabilidad desconocida para tomar control de un sistema o ejecutar codigo malicioso', 'objetivo': 'Robar datos, dañar sistemas, obtener acceso no autorizado',
    'uso_cpu': '1-100%', 'duracion': 'Temporal', 'ruta': 'Todas', 'nivel': 4},

    {'id': 57, 'nombre': 'Spyware', 'categoria': 'Software espia', 'fecha_creacion': '01-01-1990', 'tipo_transmision': 'Instalacion directa',
    'plataforma': 'Cualquier sistema operativo', 'region': 'Global', 'autor': 'Variados',
    'vectores_ataque': 'Ingenieria social, descargas de software malicioso', 'IOC(Indicadores de compromiso)': 'lentitud del sistema, presencia de software desconocido, comportamiento inusual del sistema', 'IF(impacto financiero)': 'Robo de informacion personal, financiera, etc', 'Perdida_datos': 'Robo de informacion sensible',
    'funcion': 'Esoiar la actividad del usuario', 'objetivo': 'Robar informacion personal, financiera o de navegacion',
    'uso_cpu': '1-10%', 'duracion': 'Continua', 'ruta': 'Varia', 'nivel': 3},

    {'id': 58, 'nombre': 'Soofing', 'categoria': 'Ingenieria social, suplantacion de identidad', 'fecha_creacion': '01-01-1990', 'tipo_transmision': 'Manipulacoin de informacion de identificacion',
    'plataforma': 'Cualquier sistema operativo', 'region': 'Global', 'autor': 'Variados',
    'vectores_ataque': 'Correo electronicos, sitios web falsos, llamdas telefonicas, sms', 'IOC(Indicadores de compromiso)': 'solicitud de informacion inusuales, comunicacion inesperada, informacion de contacto sospechosa', 'IF(impacto financiero)': 'Robo de informacion, acceso no autorizado, perdidas economicas', 'Perdida_datos': 'Robo de informacion personal, financiera o confidencial',
    'funcion': 'Hacerse pasar por otra persona o entidad', 'objetivo': 'Obtener informacion, acceso o realizar acciones fraudulentas',
    'uso_cpu': '1-10%', 'duracion': 'Variable', 'ruta': 'Variable', 'nivel': 3},

    {'id': 59, 'nombre': 'DDos Amplificado', 'categoria': 'Ataque de denegacion de servicio', 'fecha_creacion': '01-01-2012', 'tipo_transmision': 'Explotacion de sistios vulnerables',
    'plataforma': 'Servicios en linea', 'region': 'Global', 'autor': 'Variados',
    'vectores_ataque': 'Servidores DNS, Servidores NTP, otros servicios con capacidad de respuesta amplificada', 'IOC(Indicadores de compromiso)': 'Lentitud o inaccesibilidad de servicios en linea, trafico de red inusualmente alto, Multiples solicitudes desde direcciones IP sospechosas', 'IF(impacto financiero)': 'Perdidas por interrupcion de servicios, daño a la reputacion', 'Perdida_datos': 'No hay perdida de datos directamente',
    'funcion': 'inundar un objetivo con trafico malicioso amplificado', 'objetivo': 'Interrumpir el servicio, dañar la reputacion, extorsionar',
    'uso_cpu': '80-100%', 'duracion': 'Horas a dias', 'ruta': 'Internet', 'nivel': 4},

    {'id': 60, 'nombre': 'ToxicPanda', 'categoria': 'Troyano bancario para Android', 'fecha_creacion': '01-01-2024', 'tipo_transmision': 'Se disfraza de aplicacines legitimas de Android',
    'plataforma': 'Android', 'region': 'China y se esta propagando al Globo', 'autor': 'Desconocido',
    'vectores_ataque': 'Distribuviona traves de tiendas de aplicaciones de terceros, Ingenieria social para engañar a los usuarios', 'IOC(Indicadores de compromiso)': 'Aplicaciones de banca o Google Chrome con comportamiento inusual, Transacciones bancarias no autorizadas, Solicitudes de permisos inusuales por parte de aplicaciones', 'IF(impacto financiero)': 'Robo de fondos de cuentas bancarias', 'Perdida_datos': 'Robo de credenciales bancarias',
    'funcion': 'Evadir la seguridad bancaria tradicional y realizar retiros no autorizados', 'objetivo': 'Robar fondos directamente de las cuentas bancarias de los usuarios',
    'uso_cpu': '1-100%', 'duracion': 'Temporal', 'ruta': 'Descargas', 'nivel': 4}
]

# Llamar a la función para agregar las entradas únicas
agregar_entradas_unicas('clasificacion.csv', nuevas_entradas)

# Ahora recarga el archivo CSV actualizado
df = pd.read_csv('clasificacion.csv')

# Mostrar información básica del DataFrame actualizado
print(df.info())
print(df.head())

# Continuar con el preprocesamiento y entrenamiento del modelo
# Definir características y etiqueta
X = df.drop(columns=['nivel'])  # Características
y = df['nivel']  # Etiqueta (variable objetivo)

# Identificar columnas numéricas y categóricas
num_features = X