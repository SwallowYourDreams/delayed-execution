#!/usr/bin/env python3
import time
import os
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QSettings
from threading import Thread

class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, verbose = False):
		# Inherited class __init__ method
		super(MainWindow, self).__init__()
		# Load external .ui file
		self.scriptDir = os.path.dirname(os.path.realpath(__file__)) + "/"
		uic.loadUi( self.scriptDir + "gui.ui", self)
		self.show()
		# Misc. variables
		self.buttonText = ["Start", "Stop"]
		self.verbose = verbose
		self.runTimer = False
		self.delay = None
		# Initialisation & functions
		self.settings = QSettings("ParaDice", "DelayedExecution")
		self.loadSettings()
		self.settingsDialogue = SettingsDialogue(self.settings, self.scriptDir)
		# Bind signals to elements
		# Menu
		self.actionQuit.triggered.connect(self.quit)
		self.actionSettings.triggered.connect(self.showDialogue)
		# UI
		self.pushButton_start.clicked.connect(self.run)
		self.spinBox_hours.valueChanged.connect(self.updateDelay)
		self.spinBox_minutes.valueChanged.connect(self.updateDelay)
		self.spinBox_seconds.valueChanged.connect(self.updateDelay)
		self.buttonGroup_command.buttonClicked.connect(self.toggleCommand)
		#Statusbar
		# Check for root privileges
		if os.geteuid() == 0:
			msg = 'Superuser privileges granted.'
		else:
			msg = 'No superuser privileges. Run script with "sudo" to obtain them.'
		self.label_root.setText(msg)
		


	def closeEvent(self, event):
		# Save settings on closing
		self.saveSettings()
		event.accept() # Let the window close

	def run(self):
		# Get values from input elements
		self.updateDelay()
		commandField = self.lineEdit_command.text()
		checked = self.buttonGroup_command.checkedButton().text().lower()
		# Determine command to be executed based on the text of the radio button that is checkd
		command = {
			"shutdown*": "sudo shutdown -h",
			"suspend": "systemctl suspend",
			"reboot*": "sudo shutdown -r",
			"command:": commandField # The colon is obligatory!
		}[checked]
		
		# Get current state, i.e. whether a timer is currently running or not. 0 = start, 1 = stop
		if self.updateButton() == 0: # Run
			self.runTimer = True
			if self.verbose:
				print("Timer started.")
			t = Thread(target = self.startTimer, args=(self.delay, command,))
			t.start()
		else: # Stop
			self.runTimer = False
			os.system("shutdown -c")
			if self.verbose:
				print("Timer stopped.")
			self.progressbar.reset()
			self.label_remainingTime.setText(self.getDelayString(self.delay))
	
	def showDialogue(self):
		self.settingsDialogue.show()
	def quit(self):
		sys.exit(0)
		
	def toggleCommand(self, button):
		enable = False
		if button.objectName() == "radioButton_command":
			enable = True
		self.lineEdit_command.setEnabled(enable)
			
		
	def saveSettings(self):
		# Clear file
		self.settings.clear()
		# Check if saving is enabled
		savingIsEnabled = self.settingsDialogue.savingIsEnabled()
		# If saving settings is enabled...
		if savingIsEnabled:
			currentSettings = self.getValues()
			# Save interval values (if enabled)
			if self.settingsDialogue.saveInterval():
				intervalKeys = ["hours", "minutes", "seconds"]
				for k in intervalKeys:
					self.settings.setValue(k, currentSettings[k])
			# Save command id (if enabled)
			if self.settingsDialogue.saveCommandId():
				self.settings.setValue("commandId", currentSettings["commandId"])
			# Save command from lineInput field (if enabled AND if command is not empty)
			if self.settingsDialogue.saveCommand():
				self.settings.setValue("saveCommand", True)
				self.settings.setValue("command", currentSettings["command"])
		# Preserve saveSettings value
		self.settings.setValue("saveSettings", savingIsEnabled)
	
	# Gets all values from the main window ui and returns them as a dictionary
	def getValues(self):
		values = {}
		# Interval
		values["hours"] = self.spinBox_hours.value()
		values["minutes"] = self.spinBox_minutes.value()
		values["seconds"] = self.spinBox_seconds.value()
		# Command radio button currently selected
		selectedButton = self.buttonGroup_command.checkedButton()
		values["commandId"] = self.buttonGroup_command.id(selectedButton)
		# Command input
		values["command"] = self.lineEdit_command.text()
		return values
	
	def updateDelay(self):
		# Get values from input elements
		v = self.getValues()
		self.delay = v["hours"] * 60 * 60 + v["minutes"] * 60 + v["seconds"] # Calculate delay in seconds
		self.updateTimer(self.delay)
	
	# Accepts a delay value in seconds and returns it formatted like this hh:mm:ss
	def getDelayString(self, delay):
		hours = self.addLeadingZero( str( int(delay/(60*60)) ) )
		minutes = self.addLeadingZero( str( int( delay % (60*60) / 60 ) ) )
		seconds = self.addLeadingZero( str( int(delay%60) ) )
		delayString = hours + ":" + minutes + ":" + seconds
		return delayString
	# Adds a leading zero for any string with length < 2
	def addLeadingZero(self, string):
		if len(string) < 2:
			string = "0" + string
		return string
	
	def updateButton(self):
		currentState = self.buttonText.index(self.pushButton_start.text())
		# Update button text
		newText = self.buttonText[ not currentState ] # Get new button text 
		self.pushButton_start.setText(newText) # Set new button text
		return currentState
		
	def loadSettings(self):
		if bool(self.settings.value("saveSettings")):
			# Interval
			if bool(self.settings.contains("hours")):
				self.spinBox_hours.setValue(int(self.settings.value("hours")))
				self.spinBox_minutes.setValue(int(self.settings.value("minutes")))
				self.spinBox_seconds.setValue(int(self.settings.value("seconds")))
			# Radio buttons
			if bool(self.settings.contains("commandId")):
				button = self.buttonGroup_command.button(int(self.settings.value("commandId")))
				button.setChecked(True)
				self.toggleCommand(button) # Enable command input field if command button is selected
			# Command text field
			if bool(self.settings.contains("saveCommand")) and bool(self.settings.value("saveCommand")):
				self.lineEdit_command.setText(self.settings.value("command"))
	
	#Update all progress-related UI elements
	def update(self, currentDelay):
		self.progressbar.setValue(self.delay - currentDelay) # update progressbar
		self.updateTimer(currentDelay)
	# Update only the timer that shows the remaining time
	def updateTimer(self, currentDelay):
		delayString = self.getDelayString(currentDelay)
		# update remainingTime label in GUI
		self.label_remainingTime.setText(delayString)
		self.label_remainingTime.adjustSize()
	
	# Start new timer
	def startTimer(self, delay, command):
		currentDelay = delay
		# Set progressbar max. value
		self.progressbar.setMaximum(delay)
		# Detect shutdown or reboot command
		shutdown = 0 # shutdown: 0 = no shutdown command; 1 = shutdown command, but not yet executed; # 2 = shutdown command that has been executed
		if "sudo shutdown" in command:
			shutdown = 1
			print("Shutdown!")
		while currentDelay > 0 and self.runTimer:
			# Wait for x seconds before executing shutdown command directly. This is necessary because
			# 1.) shutdown requires superuser privileges, which may expire before the delay is up. This problem is solved by executing the command directly.
			# 2.) shutdown does not support time delays in seconds. Therefore the script must handle the seconds and then execute the command as described in 1.)
			if shutdown == 1 and currentDelay %60 == 0: 
				timestr = " +" + str(int(currentDelay / 60)) # Delay in minutes as a string
				shutdown = 2
				print("Shutdown executed!")
				os.system(command + timestr) 
			self.update(currentDelay)
			if self.verbose:
				print(self.getDelayString(currentDelay))
			# Sleep and decrement
			currentDelay-=1
			time.sleep(1)
		# Command execution
		if not shutdown and self.runTimer:
			self.update(currentDelay) # Last update to show 100% progress / 00:00:00 in remaining time
			self.progressbar.reset()
			# Reset elements
			self.updateButton()
			os.system(command)

class SettingsDialogue(QtWidgets.QDialog):
	def __init__(self, settings ,scriptDir):
		# Inherited class __init__ method
		super(SettingsDialogue, self).__init__()
		self.settings = settings
		# Load external .ui file
		uic.loadUi(scriptDir + "settings.ui", self)
		# Read settings and set checkboxes accordingly
		saveSettings = bool(settings.value("saveSettings"))
		self.checkBox_saveSettings.setChecked(saveSettings)
		self.toggleSaving()
		if settings.contains("hours"):
			self.checkBox_interval.setChecked(True)
		if settings.contains("commandId"):
			self.checkBox_commandId.setChecked(True)
		if settings.contains("saveCommand") and bool(settings.value("saveCommand")):
			self.checkBox_command.setChecked(True)
		# Signals
		self.checkBox_saveSettings.clicked.connect(self.toggleSaving)
	
	# Checks whether saving the settings upon exiting the application is enabled and returns state
	def savingIsEnabled(self):
		return self.checkBox_saveSettings.isChecked()
	def saveInterval(self):
		return self.checkBox_interval.isChecked()
	def saveCommandId(self):
		return self.checkBox_commandId.isChecked()
	def saveCommand(self):
		return self.checkBox_command.isChecked()
		
	# Enables/disables saving the settings upon closing the application
	def toggleSaving(self):
		enable = self.checkBox_saveSettings.isChecked()
		# enable / disable the whole button group below saveSettings
		buttons = self.checkBox_group.buttons()
		for b in buttons:
			b.setEnabled(enable)
			if not enable: # If disabled, deselect all buttons
				b.setChecked(enable)

# Main method
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	# Main window
	w = MainWindow()
	sys.exit(app.exec_())
