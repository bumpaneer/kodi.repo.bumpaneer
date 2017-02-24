import os
import zipfile
from git import Repo
import hashlib
import shutil
import stat
import xml.etree.ElementTree as ET
from pathlib import Path
import sys
import subprocess

def zipdir(path, zip):
	for root, dirs, files in os.walk(path):
		for file in files:
			zip.write(os.path.join(root, file))

def del_rw(action, name, exc):
	os.chmod(name, stat.S_IWRITE)
	os.remove(name)

def generate_md5_file( file ):
	# create a new md5 hash
	hash_md5 = hashlib.md5()
	with open(file, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_md5.update(chunk)
	m = hash_md5.hexdigest()
	# append file name
	m = m + "  " + os.path.basename(file)
	# save file
	try:
		save_file( m.encode( "UTF-8" ), file=file + ".md5" )
	except Exception as e:
		# oops
		print("An error occurred creating " + file + ".md5 file!\n%s" % e)

def save_file( data, file ):
	try:
		# write data to the file (use b for Python 3)
		open( file, "wb" ).write( data )
	except Exception as e:
		# oops
		print("An error occurred saving %s file!\n%s" % ( file, e ))

if __name__ == '__main__':
		if( not os.path.isdir('krypton\\working')):
			os.mkdir('krypton\\working')
		Repo.clone_from("git://github.com/bumpaneer/skin.unity.git", "krypton\\working\\repo", branch='Krypton')
		shutil.rmtree('krypton\\working\\repo\\.git', onerror=del_rw)
		os.remove('krypton\\working\\repo\\.gitattributes')
		os.remove('krypton\\working\\repo\\.gitignore')
		e = ET.parse('krypton\\working\\repo\\addon.xml').getroot()
		addonid = e.get('id')
		addonversion = e.get('version')
		filestring = 'krypton\\working\\' + addonid + '-' + addonversion + '.zip'
		newdir = 'krypton\\working\\' + addonid
		if( not os.path.isdir('krypton\\' + addonid)):
			os.mkdir('krypton\\' + addonid)
		else:
			for root, dirs, files in os.walk('krypton\\' + addonid, topdown=False):
				for name in files:
					if( not name.endswith('.zip') and not name.endswith('.md5')):
						os.remove(os.path.join(root, name))
				for name in dirs:
					os.rmdir(os.path.join(root, name))
		for asset in e.findall(".//*[@point='xbmc.addon.metadata']/assets/*"):
			assetdir = os.path.dirname(asset.text).replace('/', '\\')
			assetfile = os.path.basename(asset.text)
			if(os.path.exists('krypton\\working\\repo\\' + assetdir + '\\' + assetfile)):
				path = Path('krypton\\' + addonid + '\\' + assetdir)
				path.mkdir(parents=True, exist_ok=True)
				shutil.copy2('krypton\\working\\repo\\' + assetdir + '\\' + assetfile, 'krypton\\' + addonid + '\\' + assetdir)
		if(os.path.exists('krypton\\working\\repo\\addon.xml')):
			shutil.copy2('krypton\\working\\repo\\addon.xml', 'krypton\\' + addonid)
		theproc = subprocess.Popen(["krypton\\TexturePacker.exe", "-dupecheck -input krypton\\working\\repo\\media\\ -output krypton\\working\\Textures.xbt"])
		theproc.communicate()
		shutil.rmtree('krypton\\working\\repo\\media', onerror=del_rw)
		os.mkdir('krypton\\working\\repo\\media')
		shutil.move('krypton\\working\\Textures.xbt', 'krypton\\working\\repo\\media')
		os.rename('krypton\\working\\repo', newdir)
		zipf = zipfile.ZipFile(filestring, 'w', zipfile.ZIP_DEFLATED)
		os.chdir('krypton\\working\\')
		zipdir(addonid, zipf)
		zipf.close()
		os.chdir('..\\..')
		shutil.rmtree(newdir, onerror=del_rw)
		shutil.copy2(filestring, 'krypton\\' + addonid)
		shutil.rmtree('krypton\\working', onerror=del_rw)
		os.chdir('krypton\\')
		nextproc = subprocess.Popen([sys.executable, "addons_xml_generator.py"])
		nextproc.communicate()
		os.chdir('..')
		if(os.path.exists('krypton\\' + addonid + '\\' + addonid + '-' + addonversion + '.zip')):
			generate_md5_file('krypton\\' + addonid + '\\' + addonid + '-' + addonversion + '.zip')
		if(os.path.exists('krypton\\' + addonid + '\\addon.xml')):
			os.remove('krypton\\' + addonid + '\\addon.xml')