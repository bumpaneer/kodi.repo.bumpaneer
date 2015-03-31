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
		if( not os.path.isdir('helix\\working')):
			os.mkdir('helix\\working')
		Repo.clone_from("git://github.com/bumpaneer/skin.unity.git", "helix\\working\\repo")
		shutil.rmtree('helix\\working\\repo\\.git', onerror=del_rw)
		os.remove('helix\\working\\repo\\.gitattributes')
		os.remove('helix\\working\\repo\\.gitignore')
		e = minidom.parse('helix\\working\\repo\\addon.xml')
		addoninfo = e.getElementsByTagName('addon')
		addonid = addoninfo[0].attributes['id'].value
		addonversion = addoninfo[0].attributes['version'].value
		filestring = 'helix\\working\\' + addonid + '-' + addonversion + '.zip'
		newdir = 'helix\\working\\' + addonid
		if( not os.path.isdir('helix\\' + addonid)):
			os.mkdir('helix\\' + addonid)
		if(os.path.exists('helix\\working\\repo\\addon.xml')):
			shutil.copy2('helix\\working\\repo\\addon.xml', 'helix\\' + addonid)
		if(os.path.exists('helix\\working\\repo\\fanart.jpg')):
			shutil.copy2('helix\\working\\repo\\fanart.jpg', 'helix\\' + addonid)
		if(os.path.exists('helix\\working\\repo\\addon.xml')):
			shutil.copy2('helix\\working\\repo\\icon.png', 'helix\\' + addonid)
		if(os.path.exists('helix\\working\\repo\\changelog.txt')):
			shutil.copy2('helix\\working\\repo\\changelog.txt', 'helix\\' + addonid + '\\changelog-' + addonversion + '.txt')
		if(os.path.isdir('helix\\working\\repo\\_screenshots')):
			os.mkdir(newdir)
			shutil.move('helix\\working\\repo\\_screenshots', newdir + '\\_screenshots')
			os.chdir('helix\\working\\')
			zipscreen = zipfile.ZipFile('screenshots.zip', 'w', zipfile.ZIP_DEFLATED)
			zipdir(addonid, zipscreen)
			zipscreen.close()
			os.chdir('..\\..')
			shutil.rmtree(newdir, onerror=del_rw)
			shutil.move('helix\\working\\screenshots.zip', 'helix\\' + addonid)
		theproc = subprocess.Popen(["TexturePacker.exe", "-dupecheck -input helix\\working\\repo\\media\\ -output helix\\working\\Textures.xbt"])
		theproc.communicate()
		shutil.rmtree('helix\\working\\repo\\media', onerror=del_rw)
		os.mkdir('helix\\working\\repo\\media')
		shutil.move('helix\\working\\Textures.xbt', 'helix\\working\\repo\\media')
		os.rename('helix\\working\\repo', newdir)
		zipf = zipfile.ZipFile(filestring, 'w', zipfile.ZIP_DEFLATED)
		os.chdir('helix\\working\\')
		zipdir(addonid, zipf)
		zipf.close()
		os.chdir('..\\..')
		shutil.rmtree(newdir, onerror=del_rw)
		shutil.copy2(filestring, 'helix\\' + addonid)
		shutil.rmtree('helix\\working', onerror=del_rw)
		os.chdir('helix\\')
		nextproc = subprocess.Popen([sys.executable, "addons_xml_generator.py"])
		nextproc.communicate()
		os.chdir('..')