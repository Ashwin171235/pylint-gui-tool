import click
import os
from rich.console import Console
from rich.text import Text
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from colorama import init, Fore, Style

console = Console()
init(autoreset=True)

@click.command()
@click.argument('filename')
@click.option('--ignore', '-i', default="", help="Comma-separated list of pylint warnings to ignore.")
@click.option('--mode', '-m', type=click.Choice(['lint', 'fix', 'full'], case_sensitive=False),
              default='full', help="Choose the mode: lint (pylint only), fix (autopep8 only), full (both).")
def review(filename, ignore, mode):
    """Analyze, auto-fix, and refactor Python code using pylint and autopep8."""

    log_file = "review_log.txt"

    if mode in ['lint', 'full']:
        console.print(Text("\n🔍 Running pylint analysis...\n", style="bold blue"))
        pylint_command = f"pylint {filename} > {log_file}"
        if ignore:
            pylint_command = f"pylint --disable={ignore} {filename} > {log_file}"
        os.system(pylint_command)

    if mode in ['fix', 'full']:
        console.print(Text("\n✨ Auto-fixing code using autopep8...\n", style="bold yellow"))
        os.system(f"autopep8 --in-place --aggressive --aggressive {filename}")

    if mode == 'full':
        console.print(Text("\n🔍 Running pylint analysis (After Fixes)...\n", style="bold blue"))
        pylint_command = f"pylint {filename} >> {log_file}"
        if ignore:
            pylint_command = f"pylint --disable={ignore} {filename} >> {log_file}"
        os.system(pylint_command)

    console.print(Text(f"\n✅ Code review completed! Results saved in '{log_file}'.", style="bold green"))

    generate_html_report()

def generate_html_report(log_file="review_log.txt", html_file="report.html"):
    """Convert log file into an HTML report with syntax highlighting."""
    
    if not os.path.exists(log_file) or os.stat(log_file).st_size == 0:
        console.print("[bold red]⚠️ No pylint output found! Skipping HTML report generation.[/bold red]")
        return

    with open(log_file, "r", encoding="utf-8") as log:
        log_content = log.read().strip()

    if not log_content:
        console.print("[bold red]⚠️ Log file is empty. Nothing to generate.[/bold red]")
        return

    console.print("[bold cyan]📄 Converting log file to HTML...[/bold cyan]")

    formatter = HtmlFormatter(full=True, style="monokai")
    highlighted_code = highlight(log_content, PythonLexer(), formatter)

    with open(html_file, "w", encoding="utf-8") as html_out:
        html_out.write(highlighted_code)

    console.print(f"\n📄 ✅ [bold cyan]HTML report generated: {html_file}[/bold cyan]")

if __name__ == "__main__":
    review()

# Additional colored output messages
print(Fore.CYAN + "🔍 Running pylint analysis..." + Style.RESET_ALL)
print(Fore.GREEN + "✅ Code review completed!" + Style.RESET_ALL)
print(Fore.YELLOW + "⚠️ Warning: No pylint output found!" + Style.RESET_ALL)
