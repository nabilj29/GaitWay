import serial
import numpy as np
import csv
import time
import matplotlib.pyplot as plt
import datetime
from matplotlib.animation import FuncAnimation
import tkinter as tk
from PIL import Image, ImageTk

class RealTimeDataRecorder:
    def __init__(self):
        self.serial_port = 'COM5'
        self.baud_rate = 115200
        self.ser = serial.Serial(self.serial_port, self.baud_rate)
        self.filename = None
        self.data_array = []
        self.time_array = []
        self.fig = None
        self.ax = None
        self.t0 = None
        self.ani = None

    def start_recording(self):
        self.filename = "data_" + datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S") + ".csv"
        self.ser.reset_output_buffer()
        self.ser.reset_input_buffer()
        self.data_array = []
        self.time_array = []
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.set_title("Real-time data")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Force")
        self.t0 = time.time()

        def animate(i):
            data_array = []
            time_array = []
            try:
                data = self.ser.readline()
                data = data.decode("utf-8")
                data = data.strip()
                data = float(data)

                relative_time = time.time() - self.t0
                self.time_array.append(relative_time)
                self.data_array.append(data)

                self.ax.clear()
                self.ax.plot(self.time_array, self.data_array, label="Real-time data")
                self.ax.legend()

            except ValueError:
                print("Invalid data format")
            except KeyboardInterrupt:
                print("Finished recording")
                self.ser.close()
                return
            except:
                print("Error occurred")
                self.ser.close()
                return

        self.ani = FuncAnimation(self.fig, animate, interval=10)
        plt.show()

    def stop_recording(self):
        self.ani.event_source.stop()
        plt.close(self.fig)
        with open(self.filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Time (s)', 'Force'])
            for i in range(len(self.data_array)):
                writer.writerow([self.time_array[i], self.data_array[i]])
            
        #save the live graph recording here
        self.fig.savefig("raw_data_" + datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S") + ".png")
        
        self.ser.close()

class RealTimeDataRecorderGUI:
    def __init__(self, recorder):
        self.recorder = recorder
        self.window = tk.Tk()
        self.window.title("Real-time Data Recorder")
        self.window.geometry("800x600")
        self.window.configure(bg='white')


        self.title = tk.Label(self.window, text="Real-time Data Recorder", font=("Arial", 20), bg='white')
        self.title.pack(padx=50, pady=50, anchor=tk.CENTER)


        self.start_button = tk.Button(self.window, text="Start", command=self.recorder.start_recording, width=20, height=5)
        self.start_button.pack(padx=50, pady=50, anchor=tk.CENTER)
        self.stop_button = tk.Button(self.window, text="Stop", command=self.recorder.stop_recording, width=20, height=5)
        self.stop_button.pack(padx=50, pady=50, anchor=tk.CENTER)


    def run(self):
        self.window.mainloop()

def main():
    recorder = RealTimeDataRecorder()
    gui = RealTimeDataRecorderGUI(recorder)
    gui.run()

if __name__ == "__main__":
    main()
