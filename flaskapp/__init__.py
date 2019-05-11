from flask import Flask, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flaskapp.forms import GetServerProcessesForm
from paramiko import SSHClient, BadHostKeyException, AuthenticationException, SSHException
from socket import error

app = Flask(__name__)
app.config['SECRET_KEY'] = '6737628cb0b13ce0c676dfde280ba245'

@app.route("/", methods=['GET', 'POST'])
def home():
	form = GetServerProcessesForm()
	username = form.username.data
	password = form.password.data
	server = form.server.data
	processes = []
	if server:
		ssh = SSHClient()
		ssh.load_system_host_keys()
		try:
			ssh.connect(server, username=username, password=password)
		except (BadHostKeyException, AuthenticationException, SSHException, error) as e:
			flash('Spajanje na server nije uspjelo.', 'danger')
			return render_template('home.html', form=form, processes=processes)
		stdin, stdout, stderr = ssh.exec_command('top -b -n 1')
		lines = stdout.readlines()[7:]	#the first 7 lines are unnecessary info
		for line in lines:
			l = line.split()
			process = {
				'pid': l[0],
				'cpu': l[8],
				'command': l[11]
			}
			processes.append(process)
	return render_template('home.html', form=form, processes=processes)
