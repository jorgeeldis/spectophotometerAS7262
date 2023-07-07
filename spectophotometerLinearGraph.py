import serial
import matplotlib.pyplot as plt
from matplotlib import style

# Configure la conexión en serie
ser = serial.Serial('COM4', 9600)

# Crear listas vacías para almacenar los datos
x_data = []
y_data = []

plt.style.use('dark_background')

# Configuramos la grafica
plt.ion() # Habilitar el modo interactivo
fig, ax = plt.subplots()
line, = ax.plot([], [])  # Crear una grafica vacía

# Establecer los límites del eje x
ax.set_xlim(400, 700)

# Crear un archivo para guardar los datos
filename = 'serial_data_lineal.txt'
file = open(filename, 'w')

# Leer y trazar continuamente los datos en serie
while True:
    try:

        # Leer una línea de datos del puerto serie
        data = ser.readline().decode().strip()

        # Dividir los datos en valores x e y
        values = data.split(',')
        if len(values) != 2:
            continue

        x, y = map(float, values)

        # Comprobar si el ciclo se repite
        if x_data and x < x_data[-1]:
            # Borrar la trama y restablecer las listas de datos
            line.set_data([], [])
            x_data = []
            y_data = []

        # Agregar los datos a las listas
        x_data.append(x)
        y_data.append(y)

        # Actualizamos la grafica
        line.set_data(x_data, y_data)
        ax.relim()
        ax.autoscale_view()

        # Establecer etiquetas y título
        ax.set_xlabel('Wavelength (nm)')
        ax.set_ylabel('Absorbance (a.u.)')
        ax.set_title('Absorbance vs. Wavelength')

         # Guardar los datos en el archivo de texto
        file.write(f'{x},{y}\n')

        # Redibujar la trama
        plt.draw()
        plt.pause(0.1)

    except KeyboardInterrupt:
        break

ser.close()
