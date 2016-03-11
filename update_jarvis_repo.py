import os
import zipfile
from git import Repo
import shutil
import stat
from xml.dom import minidom
import sys
import subprocess

def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))

def del_rw(action, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)
		
if __name__ == '__main__':
		if( not os.path.isdir('jarvis\\working')):
			os.mkdir('jarvis\\working')
		Repo.clone_from("git://github.com/bumpaneer/skin.unity.git", "jarvis\\working\\repo", branch='Jarvis')
		shutil.rmtree('jarvis\\working\\repo\\.git', onerror=del_rw)
		os.remove('jarvis\\working\\repo\\.gitattributes')
		os.remove('jarvis\\working\\repo\\.gitignore')
		e = minidom.parse('jarvis\\working\\repo\\addon.xml')
		addoninfo = e.getElementsByTagName('addon')
		addonid = addoninfo[0].attributes['id'].value
		addonversion = addoninfo[0].attributes['version'].value
		filestring = 'jarvis\\working\\' + addonid + '-' + addonversion + '.zip'
		newdir = 'jarvis\\working\\' + addonid
		if( not os.path.isdir('jarvis\\' + addonid)):
			os.mkdir('jarvis\\' + addonid)
		if(os.path.exists('jarvis\\working\\repo\\addon.xml')):
			shutil.copy2('jarvis\\working\\repo\\addon.xml', 'jarvis\\' + addonid)
		if(os.path.exists('jarvis\\working\\repo\\fanart.jpg')):
			shutil.copy2('jarvis\\working\\repo\\fanart.jpg', 'jarvis\\' + addonid)
		if(os.path.exists('jarvis\\working\\repo\\addon.xml')):
			shutil.copy2('jarvis\\working\\repo\\icon.png', 'jarvis\\' + addonid)
		if(os.path.exists('jarvis\\working\\repo\\changelog.txt')):
			shutil.copy2('jarvis\\working\\repo\\changelog.txt', 'jarvis\\' + addonid + '\\changelog-' + addonversion + '.txt')
		if(os.path.isdir('jarvis\\working\\repo\\_screenshots')):
			if(os.path.exists('jarvis\\' + addonid + '\\screenshots.zip')):
				os.remove('jarvis\\' + addonid + '\\screenshots.zip')
			os.mkdir(newdir)
			shutil.move('jarvis\\working\\repo\\_screenshots', newdir + '\\_screenshots')
			os.chdir('jarvis\\working\\')
			zipscreen = zipfile.ZipFile('screenshots.zip', 'w', zipfile.ZIP_DEFLATED)
			zipdir(addonid, zipscreen)
			zipscreen.close()
			os.chdir('..\\..')
			shutil.rmtree(newdir, onerror=del_rw)
			shutil.move('jarvis\\working\\screenshots.zip', 'jarvis\\' + addonid)
		theproc = subprocess.Popen(["TexturePacker.exe", "-dupecheck -input jarvis\\working\\repo\\media\\ -output jarvis\\working\\Textures.xbt"])
		theproc.communicate()
		shutil.rmtree('jarvis\\working\\repo\\media', onerror=del_rw)
		os.mkdir('jarvis\\working\\repo\\media')
		shutil.move('jarvis\\working\\Textures.xbt', 'jarvis\\working\\repo\\media')
		os.rename('jarvis\\working\\repo', newdir)
		zipf = zipfile.ZipFile(filestring, 'w', zipfile.ZIP_DEFLATED)
		os.chdir('jarvis\\working\\')
		zipdir(addonid, zipf)
		zipf.close()
		os.chdir('..\\..')
		shutil.rmtree(newdir, onerror=del_rw)
		shutil.copy2(filestring, 'jarvis\\' + addonid)
		shutil.rmtree('jarvis\\working', onerror=del_rw)
		os.chdir('jarvis\\')
		nextproc = subprocess.Popen([sys.executable, "addons_xml_generator.py"])
		nextproc.communicate()
		os.chdir('..')