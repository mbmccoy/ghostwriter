IMAGE = ghostwriter

.PHONY: test pigpio-daemon install-pigpio pi-setup pi-packages venv requirements

pigpio-daemon: install-pigpio
	sudo cp pigpio/util/pigpiod /etc/init.d
	sudo chmod +x /etc/init.d/pigpiod
	sudo update-rc.d pigpiod defaults
	sudo service pigpiod start

install-pigpio: pigpio/.pigpio-installed

download-pigpio: pigpio/pigpio-master

pi-setup: venv pigpio-daemon pi-packages requirements

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
	&& pip install wheel \
	&& touch venv/.installed

requirements: venv opencv requirements.txt venv/.requirements-installed
venv/.requirements-installed: requirements.txt
	. venv/bin/activate \
	&& pip install -r requirements.txt \
	&& touch venv/.requirements-installed


requirements-ci: venv venv/.requirements-ci-installed
venv/.requirements-ci-installed: requirements-ci.txt
	. venv/bin/activate \
	&& pip install -r requirements-ci.txt \
	&& touch venv/.requirements-ci-installed

test: venv requirements.txt
	. venv/bin/activate \
	&& pytest tests


lint:
	. venv/bin/activate \
	&& black --check ghostwriter tests

lint-fix:
	. venv/bin/activate \
	&& black ghostwriter tests


opencv: venv venv/.opencv-installed

venv/.opencv-installed:
	./scripts/install_opencv.sh \
	&& . venv/bin/activate \
	&& pip install ./build/opencv/build/python_loader \
	&& touch venv/.opencv-installed


clean:
	rm -rf build
