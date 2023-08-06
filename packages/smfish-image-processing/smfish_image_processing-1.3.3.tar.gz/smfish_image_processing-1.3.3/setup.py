import subprocess
from distutils.command.build import build as _build
import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

# This class handles the pip install mechanism.
class build(_build):  # pylint: disable=invalid-name
  sub_commands = _build.sub_commands + [("CustomCommands", None)]

CUSTOM_COMMANDS = [
	["libdir=`ls -1 build|grep \"lib\"`; cd build/$libdir/smfish_image_processing/ && javac -cp ij.jar ReaderROI.java ReaderROIList.java && touch finished"]]

class CustomCommands(setuptools.Command):
  """A setuptools Command class able to run arbitrary commands."""

  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def RunCustomCommand(self, command_list):
    print("Running command: %s" % command_list)
    p = subprocess.Popen(
        command_list,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    # Can use communicate(input='y\n'.encode()) if the command run requires
    # some confirmation.
    stdout_data, _ = p.communicate()
    print("Command output: %s" % stdout_data)
    if p.returncode != 0:
      raise RuntimeError(
          "Command %s failed: exit code: %s" % (command_list, p.returncode))

  def run(self):
    for command in CUSTOM_COMMANDS:
      self.RunCustomCommand(command)



setuptools.setup(
	name="smfish_image_processing",
	version="1.3.3",
	author="Qian Zhu",
	author_email="zqian@jimmy.harvard.edu",
	description="SmFISH image processing library including image stitching, rotation, scaling tools",
	long_description="Includes image processing that are commonly performed in spatial transcriptomics, such as image stitching, rotation, scaling operations, and read functions for Region-Of-Interest (ROI) files and Omero-TIFF image files",
	long_description_content_type="text/markdown",
	url="https://bitbucket.org/qzhu/smfish-image-processing",
	packages=setuptools.find_packages(),
	classifiers=(
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	),
	python_requires=">=3.5",
	package_data={"smfish_image_processing":  ["ij.jar", 
		"ReaderROI.java", "ReaderROI.class", 
		"ReaderROIList.java", "ReaderROIList.class"]},
	install_requires=[
		"scipy", "numpy", "pandas", "seaborn", "matplotlib"],
	cmdclass={
		"build": build,
		"CustomCommands": CustomCommands,
		}	
)
	
