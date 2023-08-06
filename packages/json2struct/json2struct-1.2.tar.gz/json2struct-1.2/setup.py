from setuptools import setup

setup(
	name='json2struct',
	version='1.2',
	description='Creating go structs from JSON files for easy unmarshaling.',
	url='https://github.com/jalavosus/json2struct',
	author='James Alavosus',
	author_email='alavosus.james@gmail.com',
	license='MIT',
	packages=['json2struct'],
	zip_safe=False,
	entry_points = {
  	"console_scripts": ["json2struct=json2struct.command_line:main"],
  }
)