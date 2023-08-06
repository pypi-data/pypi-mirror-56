from setuptools import setup

with open('README.md', encoding = 'utf-8') as f:
	readme = f.read()

with open('requirements.txt', encoding = 'utf-8') as f:
	req = f.read().strip().split("\n")

setup(
	name					= 'YChat',
	version					= '0.1.2',
	url 					= 'https://github.com/FFTYYY/YChat',
	description				= 'A simple chatroom program.',
	long_description		= readme ,
	install_requires 		= req , 
	license					= 'MIT License',
	author					= 'Yang Yongyi',
	author_email 			= 'yongyiyang17@fudan.edu.cn',
	python_requires			= '>=3.6',
	packages				= ['YChat'],
	entry_points			= {'console_scripts': [
			'YChat-server=YChat.entry:run_server_cli' ,
			'YChat-client=YChat.entry:run_client_gui' ,
		]}
)
