from huesdk import huesdk


if __name__ == '__main__':
    username = "XP9WYleKCM-rJVhXmspW9RJdSps-vc7JQNsyOaqc"
    bridge_ip = '192.168.1.12'
    hue = huesdk.Hue(username=username, bridge_ip=bridge_ip)
    print(hue.get_groups())

    hue.get_groups()[0].on()
    hue.get_groups()[0].red()


    lights = hue.get_lights()
    print(lights)
    # lights[0].on()
    # lights[1].on()
    # lights[2].on()
    # lights[3].on()
    # lights[3].off()
    # lights[3].green()
    print(lights[0].name)
    print(lights[1].name)
    print(lights[2].name)
    print(lights[3].name)
    # lights[3].set_name('desk')
