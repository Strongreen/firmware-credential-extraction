import os
import subprocess
from rich import print

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

import sys
if len(sys.argv) < 2:
    print("[red][!] Uso: python script.py <arquivo_do_firmware>[/red]")
    sys.exit(1)

firmware = sys.argv[1]
output_dir = "extracted_firmware"

os.makedirs(output_dir, exist_ok=True)

print("[cyan][+] Analisando o firmware com binwalk...[/cyan]")
print(run_command(f"binwalk {firmware}"))

print("[yellow][+] Extraindo o conteúdo do firmware...[/yellow]")
print(run_command(f"binwalk -Me {firmware} -C {output_dir}"))

print("[green][+] Procurando por credenciais e palavras-chave interessantes...[/green]")
credentials_found = run_command(f"grep -riE 'password|admin|root|key|token' {output_dir}")

with open("credentials_found.txt", "w") as file:
    file.write(credentials_found)

if credentials_found.strip():
    print("[red][!] Credenciais encontradas! Confira o arquivo credentials_found.txt[/red]")
else:
    print("[yellow][-] Nenhuma credencial óbvia encontrada. Tente analisar manualmente.[/yellow]")

print("[cyan][+] Análise concluída! Confira a pasta:[/cyan]", output_dir)
