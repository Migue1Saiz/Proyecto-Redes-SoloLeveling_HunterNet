class Router:
    def __init__(self, name):
        self.commands = []
        self.name = name
        self._add_command("!")
        self._add_command("!")
        self._add_command("!")
        self._add_command("en")
        self._add_command("conf t")
    
    def ospf(self, area: int):
        self._add_command("router ospf 1")
        self._add_command(f"network 0.0.0.0 255.255.255.255 area {area}")


    def _add_command(self, command: str):
        self.commands.append(command)

    def add_cable(self, destiny_router, interface: str, ip_address: str, network_address: str):
        self._add_command(f"!{destiny_router}")
        self._add_command(f"interface fa0/{interface}")
        self._add_command("no switchport")
        self._add_command(f"ip address {ip_address} 255.255.255.252")
        self._add_command(f"no shutdown")
        self._add_command("exit")
        self._add_command("router ospf 1")
        self._add_command(f"network {network_address} 0.0.0.3 area 0")
        self._add_command("!")

    def add_hsrp_receiver(self, spot_3: int):
        self._add_command("! Adding hsrp receiver")
        self._add_command("vlan 10")
        self._add_command("interface fa0/4") # To the PC
        self._add_command("switchport mode access")
        self._add_command("switchport access vlan 10")
        self._add_command("interface range fa0/1-3") # Goes to the trio
        self._add_command("switchport trunk encapsulation dot1q")
        self._add_command("switchport mode trunk")
        self._add_command("!")

    def add_hsrp_three_to_switch(self, spot_3: int, spot_4: int, priority: int):
        # Configure the fisical port that communicates with the country lan
        self._add_command("ip routing")
        self._add_command("int fa0/10") # Interface connected to the receiver
        self._add_command("switchport trunk encapsulation dot1q")
        self._add_command("switchport mode trunk")
        self._add_command("no shutdown")

        # Configure the virtual interface
        self._add_command("int vlan 10")
        self._add_command(f"ip address 192.168.{spot_3}.{spot_4} 255.255.255.0")
        self._add_command(f"standby 10 ip 192.168.{spot_3}.2")
        self._add_command(f"standby 10 priority {priority}")
        self._add_command("standby 10 preempt")
        self._add_command("no shutdown")
        self._add_command("router ospf 1")
        self._add_command(f"network 192.168.{spot_3}.0 0.0.0.255 area {spot_3}")
        self._add_command("!")

    def add_gre_tunnel(self, tunnel_id: int, tunnel_ip: str, source_interface: str, dest_wan_ip: str):
        self._add_command(f"! Configuración de Tunel GRE {tunnel_id}")
        self._add_command(f"interface Tunnel {tunnel_id}")

        self._add_command(f"ip address {tunnel_ip} 255.255.255.252")
        self._add_command(f"tunnel source fa0/{source_interface}")
        self._add_command(f"tunnel destination {dest_wan_ip}")
        
        self._add_command("ip mtu 1400")
        self._add_command("ip tcp adjust-mss 1360")
        
        self._add_command("ip ospf 1 area 0")
        
        self._add_command("no shutdown")
        self._add_command("exit")
        self._add_command("!")
    
    def print_commands(self):
        for command in self.commands:
            print(command)
    
    def dump_commands(self):
        with open(f"Seoul/Configuration/Generated/{self.name}.txt", "w") as f:
            f.write("\n\n\n")
            f.write("\n".join(self.commands))
            f.write("\n\n\n")




cable_4_mod = 0
cable_3_mod = 0

core_router_list = ["Core_1", "Core_2", "Core_3", "Core_4", "Core_5", "Core_6", "Core_7", "Core_8", "Core_9"]
core_routers = {}
countries = ["Tokyo", "Jeju", "Seoul", "Paris", "Washington"]
country_router_list = ["1", "2", "3"]
country_routers = {}
country_receivers = {}

for core_router in core_router_list:
    core_routers[core_router] = Router(core_router)

for country in countries:
    country_receivers[f"{country}_receiver"] = Router(f"{country}_receiver")
    for country_router in country_router_list:
        country_routers[f"{country}_{country_router}"] = Router(f"{country}_{country_router}")





    
def generate_mesh_wiring_commands(core_routers: dict[str, Router], country_routers: dict[str, Router]):
    core_interface = 1
    cable_4_mod = 0
    cable_3_mod = 0
    for country_router in country_routers.keys():
        country_interface = 1
        core_interface += 1

        for core_router in core_routers.keys():
            network_address = f"10.0.{cable_3_mod}.{cable_4_mod * 4}"
            core_ip = 1 + cable_4_mod * 4
            country_ip = 2 + cable_4_mod * 4

            # Cableado de las microredes al core
            core_routers[core_router].add_cable(country_router, core_interface, f"10.0.{cable_3_mod}.{core_ip}", network_address)
            country_routers[country_router].add_cable(core_router, country_interface, f"10.0.{cable_3_mod}.{country_ip}", network_address)
            country_interface += 1
            cable_4_mod += 1

            if cable_4_mod == 63:
                cable_4_mod = 0
                cable_3_mod += 1
    
    country_router = "Ethernet"
    country_routers[country_router] = Router(country_router)
    country_interface = 1
    for core_router in core_routers.keys():
        network_address = f"10.0.{cable_3_mod}.{cable_4_mod * 4}"
        core_ip = 1 + cable_4_mod * 4
        country_ip = 2 + cable_4_mod * 4
        
        # Cableado de las microredes al core
        if country_router == "Ethernet":
            core_routers[core_router].add_cable(country_router, 1, f"10.0.{cable_3_mod}.{core_ip}", network_address)
        else:
            core_routers[core_router].add_cable(country_router, core_interface, f"10.0.{cable_3_mod}.{core_ip}", network_address)

        country_routers[country_router].add_cable(core_router, country_interface, f"10.0.{cable_3_mod}.{country_ip}", network_address)
        country_interface += 1
        if cable_4_mod == 63:
            cable_4_mod = 0
            cable_3_mod += 1


def generate_hsrp_commands(country_routers: dict[str, Router]): # Doesnt take into account ethernet
    counter = 3
    subnet = 20
    priority = 140
    for country_router in country_routers:
        if subnet != 40:
            country_routers[country_router].add_hsrp_three_to_switch(subnet, counter, priority)
        priority -= 20
        counter +=1

        if counter > 5:
            counter = 3
            subnet += 10
            priority = 140

def generate_receiver_hsrp_commands(country_receivers: dict[str, Router]):
    spot_3 = 10
    for key in country_receivers.keys():
        spot_3 += 10
        if key != "Seoul_receiver":
            country_receivers[key].add_hsrp_receiver(spot_3)

    

generate_mesh_wiring_commands(core_routers, country_routers) 
generate_hsrp_commands(country_routers)
generate_receiver_hsrp_commands(country_receivers)




def print_cores():
    for key in core_routers:
        print(f"\n{key}\n\n")
        print(core_routers[key].print_commands())

def print_countries():
    for key in country_routers:
        print(f"\n{key}\n\n")
        print(country_routers[key].print_commands())

def print_receivers():
    for key in country_receivers.keys():
        print(f"\n{key}\n\n")
        print(country_receivers[key].print_commands())

for core in core_routers.keys():
    core_routers[core].dump_commands()
for country_router in country_routers.keys():
    country_routers[country_router].dump_commands()
for country_receiver in country_receivers.keys():
    country_receivers[country_receiver].dump_commands()