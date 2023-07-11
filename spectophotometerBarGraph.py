import serial
import matplotlib.pyplot as plt
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

# Configure la conexión en serie
ser = serial.Serial('COM4', 9600)

# Crear listas vacías para almacenar los datos
x_data = []
y_data = []

# Configurar el estilo de la gráfica de Matplotlib
plt.style.use('dark_background')

# Crear la figura de Matplotlib
fig = Figure()
ax = fig.add_subplot(111)
line, = ax.plot([], [], drawstyle='steps-pre', linewidth=2)  # Crear una gráfica vacía
ax.set_xlim(350, 750)  # Establecer los límites del eje x

# Crear un archivo para guardar los datos
filename = 'serial_data_lineal.txt'
file = open(filename, 'w')

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(800, 600))
        
        # Crear el lienzo de dibujo de Matplotlib
        self.canvas = FigureCanvas(self, -1, fig)
        
        # Crear los botones
        baseline_btn = wx.Button(self, label='Baseline')
        single_btn = wx.Button(self, label='Single')
        continuous_btn = wx.Button(self, label='Continuous')
        
        # Establecer un tamaño mínimo más grande para los botones
        baseline_btn.SetMinSize((120, 40))
        single_btn.SetMinSize((120, 40))
        continuous_btn.SetMinSize((120, 40))
        
        # Crear el diseño de la ventana
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        
        # Crear un sizer horizontal para los botones
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(baseline_btn, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        btn_sizer.AddSpacer(20)  # Agregar espacio entre los botones
        btn_sizer.Add(single_btn, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        btn_sizer.AddSpacer(20)  # Agregar espacio entre los botones
        btn_sizer.Add(continuous_btn, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        
        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER)
        self.SetSizer(sizer)
        
        # Vincular eventos a los botones
        baseline_btn.Bind(wx.EVT_BUTTON, self.on_baseline_btn)
        single_btn.Bind(wx.EVT_BUTTON, self.on_single_btn)
        continuous_btn.Bind(wx.EVT_BUTTON, self.on_continuous_btn)
        
        # Configurar el temporizador para actualizar la gráfica en tiempo real
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer)
        self.timer.Start(100)  # Actualizar cada 100 ms
    
    def on_baseline_btn(self, event):
        # Lógica para el botón Baseline
        print('Baseline button clicked')
    
    def on_single_btn(self, event):
        # Lógica para el botón Single
        print('Single button clicked')
    
    def on_continuous_btn(self, event):
        # Lógica para el botón Continuous
        print('Continuous button clicked')
    
    def on_timer(self, event):
        try:
            # Leer una línea de datos del puerto serie
            data = ser.readline().decode().strip()

            # Dividir los datos en valores x e y
            values = data.split(',')
            if len(values) != 2:
                return

            x, y = map(float, values)

            # Comprobar si el ciclo se repite
            if x_data and x < x_data[-1]:
                # Borrar los datos y restablecer las listas
                line.set_data([], [])
                x_data.clear()
                y_data.clear()

            # Agregar los datos a las listas
            x_data.append(x)
            y_data.append(y)

            # Actualizar la gráfica
            line.set_data(x_data, y_data)
            ax.relim()
            ax.autoscale_view()

            # Set labels and title
            ax.set_xlabel('Wavelength (nm)')
            ax.set_ylabel('Absorbance (a.u.)')
            ax.set_title('Absorbance vs. Wavelength')

            # Redibujar la gráfica
            self.canvas.draw()

            # Guardar los datos en el archivo de texto
            file.write(f'{x},{y}\n')

        except serial.SerialException:
            print('Error: No se pudo abrir el puerto serie.')

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, 'Spectophotometer Linear Graph')
        frame.Show()
        return True

app = MyApp(redirect=False)
app.MainLoop()

ser.close()
file.close()
