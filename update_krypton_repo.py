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
		if( not os.path.isdir('krypton\\working')):
			os.mkdir('krypton\\working')
		Repo.clone_from("git://github.com/bumpaneer/skin.unity.git", "krypton\\working\\repo", branch='Krypton')
		shutil.rmtree('krypton\\working\\repo\\.git', onerror=del_rw)
		os.remove('krypton\\working\\repo\\.gitattributes')
		os.remove('krypton\\working\\repo\\.gitignore')
		e = minidom.parse('krypton\\working\\repo\\addon.xml')
		addoninfo = e.getElementsByTagName('addon')
		addonid = addoninfo[0].attributes['id'].value
		addonversion = addoninfo[0].attributes['version'].value
		filestring = 'krypton\\working\\' + addonid + '-' + addonversion + '.zip'
		newdir = 'krypton\\working\\' + addonid
		if( not os.path.isdir('krypton\\' + addonid)):
			os.mkdir('krypton\\' + addonid)
		if(os.path.exists('krypton\\working\\repo\\addon.xml')):
			shutil.copy2('krypton\\working\\repo\\addon.xml', 'krypton\\' + addonid)
		if(os.path.exists('krypton\\working\\repo\\resources\\fanart.jpg')):
			shutil.copy2('krypton\\working\\repo\\resources\\fanart.jpg', 'krypton\\' + addonid)
		if(os.path.exists('krypton\\working\\repo\\resources\\icon.png')):
			shutil.copy2('krypton\\working\\repo\\resources\\icon.png', 'krypton\\' + addonid)
		if(os.path.exists('krypton\\working\\repo\\changelog.txt')):
			shutil.copy2('krypton\\working\\repo\\changelog.txt', 'krypton\\' + addonid + '\\changelog-' + addonversion + '.txt')
		if(os.path.isdir('krypton\\working\\repo\\resources')):
			if(os.path.exists('krypton\\' + addonid + '\\screenshots.zip')):
				os.remove('krypton\\' + addonid + '\\screenshots.zip')
			os.mkdir(newdir)
			shutil.move('krypton\\working\\repo\\resources', newdir + '\\resources')
			os.chdir('krypton\\working\\')
			zipscreen = zipfile.ZipFile('screenshots.zip', 'w', zipfile.ZIP_DEFLATED)
			zipdir(addonid, zipscreen)
			zipscreen.close()
			os.chdir('..\\..')
			shutil.rmtree(newdir, onerror=del_rw)
			shutil.move('krypton\\working\\screenshots.zip', 'krypton\\' + addonid)
		theproc = subprocess.Popen(["TexturePacker.exe", "-dupecheck -input krypton\\working\\repo\\media\\ -output krypton\\working\\Textures.xbt"])
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