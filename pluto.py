import os
import subprocess
if __name__ == '__main__':

    #cmd = 'sudo rfkill block wifi'
    ris=''
    output = subprocess.run('rfkill', capture_output=True).stdout
    index=output.find(b'phy0   blocked')

    cmd='rfkill'
    r=os.system(cmd)
    print("gggg")
