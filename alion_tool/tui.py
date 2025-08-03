import webbrowser
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer, Static, Button, RichLog

# Importa as ações do nosso outro arquivo
from .actions import COMMAND_ACTIONS, run_powershell_command

# O banner ASCII
BANNER_ASCII = r"""
 [magenta]░▒▓██████▓▒░░▒▓█▓▒░     ░▒▓█▓▒░░▒▓██████▓▒░░▒▓███████▓▒░         ░▒▓████████▓▒░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓████████▓▒░
 ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
 ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░
 ░▒▓████████▓▒░▒▓█▓▒░     ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░         ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓█▓▒▒▓███▓▒░▒▓██████▓▒░
 ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
 ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
 ░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░      ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓████████▓▒░[/]
"""

class AlionApp(App):
    """Uma TUI para a ferramenta AlionV2 usando Textual."""

    CSS_PATH = None # Não usaremos CSS externo por enquanto
    TITLE = "AlionV2 Multi-tool - by r3du0x"
    SUB_TITLE = "Developed by r3du0x® 2025 | Alpha Ver."

    def compose(self) -> ComposeResult:
        """Cria o layout da aplicação."""
        yield Header()
        yield Static(BANNER_ASCII, id="banner")

        # Cria botões dinamicamente a partir do dicionário de ações
        with Horizontal(id="button-container"):
            with Vertical():
                for i, (action_id, (name, _)) in enumerate(COMMAND_ACTIONS.items()):
                    if i < 6: # Coluna 1
                        yield Button(name, id=action_id, variant="primary")
            with Vertical():
                for i, (action_id, (name, _)) in enumerate(COMMAND_ACTIONS.items()):
                    if i >= 6: # Coluna 2
                        yield Button(name, id=action_id, variant="primary")
                yield Button("Open Github", id="github", variant="default")

        yield RichLog(id="log", wrap=True, highlight=True)
        yield Footer()

    def on_mount(self) -> None:
        """Chamado quando a aplicação inicia."""
        log = self.query_one(RichLog)
        log.write("[bold green]Bem-vindo ao AlionV2![/] Selecione uma opção acima.")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Chamado quando um botão é pressionado."""
        button_id = event.button.id
        log = self.query_one(RichLog)
        log.clear()

        if button_id == "github":
            log.write("Abrindo o Github no seu navegador...")
            webbrowser.open("https://github.com/joaodrmmd/AlionV2")
            log.write("[bold green]Link aberto![/]")
            return

        if button_id in COMMAND_ACTIONS:
            action_name, command_str = COMMAND_ACTIONS[button_id]
            log.write(f"[bold]Executando:[/bold] {action_name}...")

            # Desativa os botões para evitar cliques duplos
            for btn in self.query(Button):
                btn.disabled = True

            # Executa o comando em um "worker" para não travar a interface
            self.run_worker(self.execute_command, command_str, action_name)

    def execute_command(self, command_str: str, action_name: str) -> None:
        """Worker para executar o comando em segundo plano."""
        success, output = run_powershell_command(command_str)

        # Quando o comando terminar, reativa os botões e mostra a saída na thread principal
        self.call_from_thread(self.finalize_command, success, output, action_name)

    def finalize_command(self, success: bool, output: str, action_name: str) -> None:
        """Atualiza a UI após a execução do comando."""
        log = self.query_one(RichLog)
        if success:
            log.write(f"[bold green]SUCESSO[/]: '{action_name}' finalizado.")
            log.write(output)
        else:
            log.write(f"[bold red]ERRO[/] ao executar '{action_name}':")
            log.write(output)

        # Reativa os botões
        for btn in self.query(Button):
            btn.disabled = False
