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
		if( not os.path.isdir('isengard\\working')):
			os.mkdir('isengard\\working')
		Repo.clone_from("git://github.com/bumpaneer/skin.unity.git", "isengard\\working\\repo", branch='Isengard')
		shutil.rmtree('isengard\\working\\repo\\.git', onerror=del_rw)
		os.remove('isengard\\working\\repo\\.gitattributes')
		os.remove('isengard\\working\\repo\\.gitignore')
		e = minidom.parse('isengard\\working\\repo\\addon.xml')
		addoninfo = e.getElementsByTagName('addon')
		addonid = addoninfo[0].attributes['id'].value
		addonversion = addoninfo[0].attributes['version'].value
		filestring = 'isengard\\working\\' + addonid + '-' + addonversion + '.zip'
		newdir = 'isengard\\working\\' + addonid
		if( not os.path.isdir('isengard\\' + addonid)):
			os.mkdir('isengard\\' + addonid)
		if(os.path.exists('isengard\\working\\repo\\addon.xml')):
			shutil.copy2('isengard\\working\\repo\\addon.xml', 'isengard\\' + addonid)
		if(os.path.exists('isengard\\working\\repo\\fanart.jpg')):
			shutil.copy2('isengard\\working\\repo\\fanart.jpg', 'isengard\\' + addonid)
		if(os.path.exists('isengard\\working\\repo\\addon.xml')):
			shutil.copy2('isengard\\working\\repo\\icon.png', 'isengard\\' + addonid)
		if(os.path.exists('isengard\\working\\repo\\changelog.txt')):
			shutil.copy2('isengard\\working\\repo\\changelog.txt', 'isengard\\' + addonid + '\\changelog-' + addonversion + '.txt')
		if(os.path.isdir('isengard\\working\\repo\\_screenshots')):
			if(os.path.exists('isengard\\' + addonid + '\\screenshots.zip')):
				os.remove('isengard\\' + addonid + '\\screenshots.zip')
			os.mkdir(newdir)
			shutil.move('isengard\\working\\repo\\_screenshots', newdir + '\\_screenshots')
			os.chdir('isengard\\working\\')
			zipscreen = zipfile.ZipFile('screenshots.zip', 'w', zipfile.ZIP_DEFLATED)
			zipdir(addonid, zipscreen)
			zipscreen.close()
			os.chdir('..\\..')
			shutil.rmtree(newdir, onerror=del_rw)
			shutil.move('isengard\\working\\screenshots.zip', 'isengard\\' + addonid)
		theproc = subprocess.Popen(["TexturePacker.exe", "-dupecheck -input isengard\\working\\repo\\media\\ -output isengard\\working\\Textures.xbt"])
		theproc.communicate()
		shutil.rmtree('isengard\\working\\repo\\media', onerror=del_rw)
		os.mkdir('isengard\\working\\repo\\media')
		shutil.move('isengard\\working\\Textures.xbt', 'isengard\\working\\repo\\media')
		os.rename('isengard\\working\\repo', newdir)
		zipf = zipfile.ZipFile(filestring, 'w', zipfile.ZIP_DEFLATED)
		os.chdir('isengard\\working\\')
		zipdir(addonid, zipf)
		zipf.close()
		os.chdir('..\\..')
		shutil.rmtree(newdir, onerror=del_rw)
		shutil.copy2(filestring, 'isengard\\' + addonid)
		shutil.rmtree('isengard\\working', onerror=del_rw)
		os.chdir('isengard\\')
		nextproc = subprocess.Popen([sys.executable, "addons_xml_generator.py"])
		nextproc.communicate()
		os.chdir('..')