IMAGE = ghostwriter

.PHONY: test pigpio-daemon install-pigpio pi-setup pi-packages venv

pigpio-daemon: install-pigpio
	sudo cp pigpio/util/pigpiod /etc/init.d
	sudo chmod +x /etc/init.d/pigpiod
	sudo update-rc.d pigpiod defaults
	sudo service pigpiod start

install-pigpio: pigpio/.pigpio-installed

download-pigpio: pigpio/pigpio-master

pi-setup: pigpio-daemon pi-packages

pigpio/pigpio-master:
	mkdir -p pigpio \
	&& cd pigpio \
	&& wget https://github.com/joan2937/pigpio/archive/master.zip \
	&& unzip master.zip \
	&& cd pigpio-master \
	&& make

pigpio/.pigpio-installed: download-pigpio
	mkdir -p pigpio \
	&& cd pigpio/pigpio-master \
	&& make \
	&& sudo make install \
	&& touch pigpio/.pigpio-installed

pi-packages: pigpio/.pi-packages-installed
pigpio/.pi-packages-installed:
	mkdir -p pigpio && \
	sudo apt install python-setuptools python3-setuptools \
	&& touch pigpio/.pi-packages-installed

venv: venv/.installed

venv/.installed:
	sudo apt-get install -y python3-venv \
	&& python3 -m venv venv \
	&& . venv/bin/activate \
	&& pip install -r requirements.txt \
	&& touch venv/.installed

requirements: requirements.txt
	. venv/bin/activate \
	&& pip install -r requirements.txt \
	&& touch venv/.installed

test: venv requirements.txt
	. venv/bin/activate \
	&& pytest tests

lint:
	black --check ghostwriter tests

lint-fix:
	black ghostwriter tests
