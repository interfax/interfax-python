PLUGINS = %w(vagrant-auto_network vagrant-exec)

PLUGINS.reject! { |plugin| Vagrant.has_plugin? plugin }

unless PLUGINS.empty?
  print "The following plugins will be installed: #{PLUGINS.join ", "} continue? [y/n]: "
  if ['yes', 'y'].include? $stdin.gets.strip.downcase
    PLUGINS.each do |plugin|
      system("vagrant plugin install #{plugin}")
      puts
    end
  end
  puts "Please run again"
  exit 1
end

AutoNetwork.default_pool = "172.16.0.0/24"

$host_directory = File.expand_path(File.dirname(__FILE__))
$directory = "/home/vagrant/interfax"
$virtualenv = "/home/vagrant/env"

$provision = <<SCRIPT
#!/bin/sh

apt-get -y --force-yes install software-properties-common

[ ! -f /etc/apt/sources.list.d/fkrull-deadsnakes-trusty.list ] && sudo add-apt-repository ppa:fkrull/deadsnakes

# PACKAGES
if [ ! -f /root/.last-update ] || [ $(expr $(date +%s) / 60 / 60 / 24) -gt $(expr $(cat /root/.last-update) / 60 / 60 / 24) ]; then
  sudo apt-get -y update
  date +%s | sudo tee /root/.last-update > /dev/null
fi

apt-get -y --force-yes install python2.6 python2.7 python3.3 python3.4 python3.5 pypy python3-pip python-virtualenv git

# APPLICATION

[ ! -d #{$virtualenv} ] && su -c "virtualenv -p $(which python3) #{$virtualenv}" - vagrant

su -c "cd #{$directory} && #{$virtualenv}/bin/pip install -e ." - vagrant
su -c "cd #{$directory} && #{$virtualenv}/bin/pip install tox pytest wheel" - vagrant
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "puppetlabs/ubuntu-14.04-64-nocm"

  config.vm.network "private_network", :auto_network => true

  config.vm.synced_folder ".", $directory, :type => :nfs

  config.vm.provision "shell", :inline => $provision

  config.ssh.forward_agent = true

  config.vm.provider "vmware_fusion" do |v|
    v.vmx["memsize"] = "1024"
    v.vmx["numvcpus"] = "2"
  end

  config.hostsupdater.remove_on_suspend = true

  config.exec.commands "*", directory: $directory

  config.exec.commands "*", env: { "PATH" => "#{$virtualenv}/bin:$PATH" }

  config.exec.commands %w[make python py.test tox]
end