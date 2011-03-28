import anydbm, time from time, glob from glob, shutil, random, os

class Lights:
	def flash(self, which = 'caps', times = 3):
		return true

	def on(self, which = 'caps'):
		return true

	def off(self, which = 'caps'):
		return true

class DriveHistory:
	def __init__(self, filename = 'drive_history'):
		self.db = anydbm.open(filename, 'c')

	def ok_to_use(self, drive_id):
		if(drive_id in self.db):
			return int(self.db[drive_id]) < (time() - 60 * 60 * 8)
		else:
			return true
	
	def mark(self, drive_id):
		self.db[drive_id] = time()
	
	def transfer_history():
		return true

def get_random_diff_file(files_1, files_2):
	random.shuffle(files_1)
	for filename in files_1:
		if filename not in files_2:
			return filename
	raise Exception('No diff!')

def unmount(drive):
	return os.system('unmount '+drive)

drive_history = DriveHistory()
lights = Lights()
drive_id = os.environ.get('DEVNAME')
storage = '/storage/'
drive = os.environ.get('DEVNAME')
error_led = 'caps'
ok_led = 'scroll'

if(drive_history.ok_to_use(drive_id)):
	files_on_disk = glob(drive + '/*.mp3')
	files_stored = glob(storage)
	try:
		lights.on(ok_led)
		file_in = get_random_diff_file(files_on_disk, files_stored)
		file_out = get_random_diff_file(files_stored, files_on_disk)
		copy(file_in, storage)
		copy(file_out, drive)
		drive_history.mark(drive_id)
		unmount(drive)
		lights.off(ok_led)
	else:
		unmount(drive)
		lights.flash(error_led)
else:
	unmount(drive)
	lights.flash(error_led)