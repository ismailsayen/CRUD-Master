def load_env(path)
  File.readlines(path).each do |line|
    next if line.strip.empty?
    next if line.strip.start_with?("#")

    key, value = line.strip.split("=", 2)
    ENV[key] = value if key && value
  end
end
load_env(".env")

Vagrant.configure("2") do |config|
  
  config.vm.define "billing" do |billing|
    billing.vm.post_up_message="--------------billing------------------ "
    billing.vm.box = "ubuntu/jammy64"
    billing.vm.hostname="billing"
    billing.vm.network "private_network", ip: "192.168.56.11"
    billing.vm.synced_folder "srcs/billing-app/", "/home/vagrant/billing-app", type: "rsync",
      rsync__exclude: [
        "envs",
        "__pycache__"
      ]
    billing.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      vb.cpus = 1
    end
    
    billing.vm.provision "shell" do |sh|
      sh.path = "scripts/billing_setup.sh"
      sh.env = {
        BILLING_DATABASE_URL: ENV['BILLING_DATABASE_URL'],
        USER_DB:ENV['USER_DB'],
        PASSWORD_DB:ENV['PASSWORD_DB'],
        RABBITMQ_USER: ENV['RABBITMQ_USER'],
        RABBITMQ_PASS: ENV['RABBITMQ_PASS'],
        RABBITMQ_HOST: ENV['RABBITMQ_HOST'],
        RABBITMQ_VHOST: ENV['RABBITMQ_VHOST'],
        RABBITMQ_PORT: ENV['RABBITMQ_PORT'],
        RABBITMQ_QUEUE: ENV['RABBITMQ_QUEUE']
      }
    end
  end

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
        RABBITMQ_VHOST: ENV['RABBITMQ_VHOST'],
        RABBITMQ_QUEUE: ENV['RABBITMQ_QUEUE']
      }
    end
  end



end

