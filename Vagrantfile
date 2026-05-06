Vagrant.configure("2") do |config|
  config.vm.define "api_gateway" do |api_gateway|
    api_gateway.vm.post_up_message="--------------api_gateway------------------ "
    api_gateway.vm.box = "ubuntu/trusty64"
    api_gateway.vm.hostname="api.gateway"
    api_gateway.vm.network "private_network", ip: "192.168.56.10"
    api_gateway.vm.synced_folder "srcs/api-gateway-app/", "/home/vagrant/api-gateway-app", type: "rsync",
      rsync__exclude: [
        "envs",
        "__pycache__"
      ]
    api_gateway.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      vb.cpus = 1
    end
  end
end
