def load_env()
  File.foreach(".env") do |line|
    if !line.start_with?("#")
      key, value = line.split('=', 2)
      ENV[key] = value
    end
  end
end

load_env()

Vagrant.configure("2") do |config|
  config.vm.define "api_gateway" do |api_gateway|
    api_gateway.vm.post_up_message="--------------api_gateway------------------ "
    api_gateway.vm.box = "ubuntu/jammy64"
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
    api_gateway.vm.provision "shell" do |sh|
      sh.path = "scripts/gateway_setup.sh"
      sh.env = {
        API_GATEWAY_PORT: ENV['API_GATEWAY_PORT'],
        API_GATEWAY_HOST: ENV['API_GATEWAY_HOST'],
        RABBITMQ_USER: ENV['RABBITMQ_USER'],
        RABBITMQ_PASS: ENV['RABBITMQ_PASS'],
        RABBITMQ_HOST: ENV['RABBITMQ_HOST'],
        RABBITMQ_PORT: ENV['RABBITMQ_PORT'],
      }
    end
  end
end

