import PySimpleGUI as sg
from fill_in_gaps import FillInGaps
import os

sg.theme('Dark Blue 3')

class GUI:

	def __init__(self):
		self.fig = FillInGaps()
		column = [
			[sg.Text("Select an input .odt file")],
			[
				sg.In(size=(80, 1), enable_events=True, key="-FILE IN-"),
				sg.FileBrowse(),
			],
			[sg.Text("Please put a valid .odt file.", size=(80, 1), key="-FILE WARNING-", text_color="red", visible=False),],
			[sg.Text("Loaded successfully!", size=(80, 1), key="-FILE SUCCESS-", text_color="green", visible=False),],
			[sg.Text("", size=(80, 6), key="-TEXT GAPS-"),],
			[sg.Text("", size=(80, 1), key="-GAPS-"),],
			[sg.Button("Show", key="-SHOW-", disabled=True),],
			[sg.Button("Next", key="-NEXT-", disabled=True),],
			[sg.Text("Threshold on word frequencies to ignore (eg. 'abalone'=0.07 and 'est'=15085). Put -1 to ignore all words from the dictionnary.", size=(80, 2)),],
			[sg.InputText("10", size=(6, 1), key="-THRESHOLD-", enable_events=True),],
			[sg.Text("Please put a number (eg. 1387.4, 0.05, -1, etc...)", size=(80, 1), key="-THRESHOLD WARNING-", text_color="red", visible=False),],
		]
		layout = [
			[sg.Column(column)]
		]
		self.window = sg.Window("Fill in gaps", layout)
		self.threshold_valid = True
		self.filein_valid = False

	def run(self):
		do_init = True
		event_timeout = 1
		while True:
			event, values = self.window.read(event_timeout)
			if do_init:
				self.trigger_threshold_event(values)
				do_init = False
				event_timeout = None

			if event == "Exit" or event == sg.WIN_CLOSED:
				break

			elif event == "-FILE IN-":
				try:
					self.filein_valid = os.path.exists(values["-FILE IN-"])
				except:
					self.filein_valid = False
				self.filein_valid = self.filein_valid and values["-FILE IN-"].endswith(".odt")
				if self.filein_valid:
					try:
						self.fig.load_file(values["-FILE IN-"])
					except:
						self.filein_valid = False
				self.window["-SHOW-"].update(disabled=not self.filein_valid)
				self.window["-NEXT-"].update(disabled=not self.filein_valid)
				self.window["-FILE WARNING-"].update(visible=not self.filein_valid)
				self.window["-FILE SUCCESS-"].update(visible=self.filein_valid)
			elif event == "-NEXT-":
				text, text_gaps, gaps = self.fig.draw_text()
				self.window["-TEXT GAPS-"].update(text_gaps)
				self.window["-GAPS-"].update(' / '.join(gaps), visible=False)

			elif event == "-SHOW-":
				self.window["-GAPS-"].update(visible=True)

			elif event == "-THRESHOLD-":
				self.trigger_threshold_event(values)

	def trigger_threshold_event(self, values):
		try:
			threshold = float(values["-THRESHOLD-"])
		except ValueError:
			self.threshold_valid = False
		else:
			self.threshold_valid = True
			self.fig.freq_max = threshold
		self.window["-THRESHOLD WARNING-"].update(visible=not self.threshold_valid)

def main():
	gui = GUI()
	gui.run()

if __name__ == '__main__':
	main()