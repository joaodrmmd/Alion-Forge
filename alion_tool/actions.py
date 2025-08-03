import subprocess

# Mapeia um ID para uma tupla contendo (Nome do Botão, Função a ser chamada)
# Isso torna a adição de novos botões muito mais fácil no futuro.
COMMAND_ACTIONS = {
    "restore_point": ("Create Restore Point", "Checkpoint-Computer -Description 'AlionV2 Restore Point' -RestorePointType 'MODIFY_SETTINGS'"),
    "spotify_activation": ("Spotify Activation", "$scriptURL='https://spotx-official.github.io/run.ps1'; $tempFile=[System.IO.Path]::Combine($pwd.Path, 'temp_script_' + (Get-Date -Format 'HH-mm-ss') + '_' + (Get-Random) + '.ps1'); (New-Object System.Net.WebClient).DownloadFile($scriptURL, $tempFile); & $tempFile; Remove-Item $tempFile -Force; Pause"),
    "kms_activation": ("KMS Activation", "irm https://get.activated.win | iex"),
    "optimization": ("Otimization", "irm https://christitus.com/win | iex"),
    "download_quickcpu": ("Download QuickCPU", "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')); choco install -y wget; wget -O \\\"$env:USERPROFILE\\Downloads\\QuickCPU.zip\\\" 'https://www.coderbag.com/assets/downloads/cpm/currentversion/QuickCpuSetup64.zip' ; Start-Process explorer.exe $env:USERPROFILE\\Downloads"),
    "disk_cleanup": ("Disk Cleanup", "Start-Process cleanmgr -ArgumentList '/sagerun:1' -Wait; Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('Disk cleanup is complete!', 'Notification')"),
    "ahoy": ("Ahoy!", "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')); choco install -y wget; wget -O \\\"$env:USERPROFILE\\Downloads\\Ahoy!.zip\\\" 'https://www.mediafire.com/folder/idotcbblq5o2l/Ahoy!' ; Start-Process explorer.exe $env:USERPROFILE\\Downloads"),
    "nvidia_drivers": ("NVIDIA Drivers", "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')); choco install -y wget; wget -O \\\"$env:USERPROFILE\\Downloads\\Nvidia Driver.zip\\\" 'https://us.download.nvidia.com/GFE/GFEClient/3.28.0.417/GeForce_Experience_v3.28.0.417.exe' ; Start-Process explorer.exe $env:USERPROFILE\\Downloads"),
    "amd_drivers": ("AMD Drivers", "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')); choco install -y wget; wget -O \\\"$env:USERPROFILE\\Downloads\\AMD Driver.zip\\\" 'https://drivers.amd.com/drivers/installer/24.10/whql/amd-software-adrenalin-edition-24.8.1-minimalsetup-240829_web.exe' ; Start-Process explorer.exe $env:USERPROFILE\\Downloads"),
    "discord_nitro": ("Discord Nitro - Windows", "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')); choco install -y wget; wget -O \\\"$env:USERPROFILE\\Downloads\\DiscordNitro.zip\\\" 'https://github.com/Vencord/Installer/releases/latest/download/VencordInstaller.exe' ; Start-Process explorer.exe $env:USERPROFILE\\Downloads"),
}

def run_powershell_command(command_string: str) -> tuple[bool, str]:
    """
    Executa um comando PowerShell e retorna um status de sucesso e a saída.
    Retorna: (sucesso: bool, saida: str)
    """
    try:
        # Usamos capture_output para pegar o stdout e stderr
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command_string],
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8' # Garante a codificação correta
        )
        output = result.stdout if result.stdout else "Comando executado com sucesso, sem saída no console."
        return True, output
    except FileNotFoundError:
        return False, "Erro: 'powershell' não foi encontrado. Certifique-se de que está instalado e no PATH do sistema."
    except subprocess.CalledProcessError as e:
        # Se o comando falhar, retorna o erro
        error_message = f"Erro ao executar o comando:\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}"
        return False, error_message
