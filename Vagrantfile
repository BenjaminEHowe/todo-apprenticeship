# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.provision "shell", privileged: false, inline: <<-SHELL 
    sudo apt-get update
    sudo apt-get upgrade -y
    sudo apt-get autoremove -y
    sudo apt-get install -y python3 python3-pip python3-virtualenv
    sudo ln -s /usr/bin/python3 /usr/bin/python
    # below is important on Windows otherwise filesystem issues occur (e.g. "OError: [Errno 26] Text file busy")
    cp -r /vagrant ~/todo
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3
  SHELL
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.trigger.after [:provision] do |t|
    t.name = "Reboot after provisioning"
    t.run = { :inline => "vagrant reload" }
  end
  config.trigger.after :up do |trigger|
    trigger.name = "Launching App"
    trigger.info = "Running the To-Do App" 
    trigger.run_remote = {privileged: false, inline: "
      cd ~/todo
      poetry install
      nohup poetry run flask run --host=0.0.0.0 > /vagrant/.vagrant/log.txt 2>&1 &
    "}
  end
end
