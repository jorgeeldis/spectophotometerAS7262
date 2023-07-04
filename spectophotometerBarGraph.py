import serial
import matplotlib.pyplot as plt

# Set up the serial connection
ser = serial.Serial('COM4', 9600)  # Replace 'COM4' with the appropriate port name and baud rate

# Create empty lists to store the data
x_data = []
y_data = []

plt.style.use('dark_background')

# Set up the plot
plt.ion()  # Enable interactive mode
fig, ax = plt.subplots()

# Create a file to save the data
filename = 'serial_data_barra.txt'
file = open(filename, 'w')

# Continuously read and plot the serial data
while True:
    try:
        # Read a line of data from the serial port
        data = ser.readline().decode().strip()

        # Split the data into x and y values
        values = data.split(',')
        if len(values) != 2:
            continue

        x, y = map(float, values)

        # Check if the cycle repeats
        if x_data and x < x_data[-1]:
            # Clear the plot and reset the data lists
            ax.clear()
            x_data = []
            y_data = []

        # Append the data to the lists
        x_data.append(x)
        y_data.append(y)

        # Plot the bar graph
        ax.plot(x_data, y_data, drawstyle='steps-pre', linewidth=2)

        # Set the x-axis limits
        ax.set_xlim(400, 700)

        # Set labels and title
        ax.set_xlabel('Wavelength (nm)')
        ax.set_ylabel('Absorbance (a.u.)')
        ax.set_title('Absorbance vs. Wavelength of Low Oxygen Blood')

        # Save the data to the file
        file.write(f'{x},{y}\n')

        # Redraw the plot
        plt.draw()
        plt.pause(0.01)

    except KeyboardInterrupt:
        break

# Close the file and the serial connection
file.close()
ser.close()