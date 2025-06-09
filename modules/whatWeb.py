import subprocess
import modules.const as const

def enum(url):
    result = []
    try:
        print(f"{const.CYAN}[+] Scanning HTTP with Whatweb")
        whatWeb = subprocess.run(["whatweb", "--color", "never", url], capture_output=True, text=True)
        whatWeb = whatWeb.stdout.split(",")
                
        result.append(f"\nWhatweb\n--------------")
                
        for item in whatWeb:
            result.append(item.strip())
            print(f"{const.GREEN} [i] {item.strip()}")
        
        return result
    except:
            print(f"{const.RED}[x] Whatweb scan failed{const.RESET}")
    
    