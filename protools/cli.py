import os
import subprocess

from rich import print as rprint
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, Task, BarColumn, TimeRemainingColumn, TimeElapsedColumn, SpinnerColumn, ProgressColumn, TextColumn
from rich.table import Table
from rich.text import Text

from rich_LogConsole import LogConsoleScroll


def buf2json(cmd, localpath, inf, outf, progress, log, warn):
    if not os.path.isdir(inf):
        warn.log(f"[magenta]{inf}[/magenta] [bold red]文件夹不存在[/bold red]")
        return
    if not os.path.isdir(outf):
        try:
            os.mkdir(outf)
        except:
            warn.log(f"[bold red]创建 [magenta]{outf}[/magenta] 文件夹失败[/bold red]")
            return
    bufs = os.listdir(inf)
    task = progress.add_task(f"{inf} to {outf}...", total=len(bufs))
    for buf in bufs:
        name, fmt = tuple(buf.rsplit(".", 1))
        logline = Text()
        logline.append(Text(f'{inf}/{name}.{fmt}', style="magenta"))
        logline.append(' -> ')
        logline.append(Text(f'{outf}/{name}.json', style="magenta"))
        log.log(logline)
        fi = open(f'{inf}/{buf}', 'rb')
        fo = open(f'{outf}/{name}.json', 'wb')
        try:
            popen = subprocess.Popen([localpath+'bin/'+cmd, '--decode_raw'], stdin=fi, stdout=fo, stderr=subprocess.PIPE)
            popen.wait()
            err = popen.communicate()[1]
            if err:
                logline.append('\t')
                logline.append(Text(err.decode().strip(), style="red"))
                warn.log(logline)
        except Exception as err:
            logline.append('\t')
            logline.append(Text(err, style="red"))
            warn.log(logline)
        fi.close()
        fo.close()
        progress.update(task, advance=1)
    progress.remove_task(task)


def proto2python(cmd, localpath, inf, outf, progress, log, warn):
    if not os.path.isdir(inf):
        warn.log(f"[magenta]{inf}[/magenta] [bold red]文件夹不存在[/bold red]")
        return
    if not os.path.isdir(outf):
        try:
            os.mkdir(outf)
        except:
            warn.log(f"[bold red]创建 [magenta]{outf}[/magenta] 文件夹失败[/bold red]")
            return
    protos = os.listdir(inf)
    task = progress.add_task(f"{inf} to {outf}...", total=len(protos))
    for proto in protos:
        name, fmt = tuple(proto.rsplit(".", 1))
        logline = Text()
        logline.append(Text(f'{inf}/{name}.{fmt}', style="magenta"))
        logline.append(' -> ')
        logline.append(Text(f'{outf}/{name}_pb2.py', style="magenta"))
        log.log(logline)
        try:
            popen = subprocess.Popen([localpath+'bin/'+cmd, '--proto_path', f'{inf}', '--python_out', f'{outf}', f'{proto}'], stderr=subprocess.PIPE)
            popen.wait()
            err = popen.communicate()[1]
            if err:
                logline = Text()
                logline.append(Text(f'{inf}/{name}.{fmt}', style="magenta"))
                logline.append(' -> ')
                logline.append(Text(f'{outf}/{name}_pb2.py', style="magenta"))
                logline.append('\t')
                logline.append(Text(err.decode().strip(), style="red"))
                warn.log(logline)
        except Exception as err:
            logline = Text()
            logline.append(Text(f'{inf}/{name}.{fmt}', style="magenta"))
            logline.append(' -> ')
            logline.append(Text(f'{outf}/{name}_pb2.py', style="magenta"))
            logline.append('\t')
            logline.append(Text(err, style="red"))
            warn.log(logline)
        progress.update(task, advance=1)
    progress.remove_task(task)


def prepare():
    if __file__.rfind('/') != -1:
        localpath = __file__[:__file__.rfind('/') + 1]
    elif __file__.rfind('\\') != -1:
        localpath = __file__[:__file__.rfind('\\') + 1]
    else:
        rprint("[bold red]未知的系统路径表示形式，无法运行，请提交issue[/bold red]")
        rprint(f"[bold magenta]{__file__}[/bold magenta]")
        return
    import getopt
    import sys
    opts, _ = getopt.getopt(sys.argv[1:], "f:i:o:")
    funcs = [__ for (_, __) in opts if _ == '-f']
    if not len(funcs) == 1 or funcs[0] not in {'b2j', 'buf2json', 'p2p', 'proto2python'}:
        grid = Table.grid()
        grid.add_column(style="bold red")
        grid.add_column(style="bold red")
        grid.add_row("合法的[magenta]动作[/magenta]传入参数为：", "[magenta]1个[/magenta]动作(-f)")
        grid.add_row("", "[green]-f sample_func[/green]")
        grid.add_row("可选的[magenta]动作[/magenta]传入参数有：", "[magenta]b2j[/magenta]")
        grid.add_row("", "[green]-f b2j[/green]")
        grid.add_row("", "[magenta]buf2json[/magenta]")
        grid.add_row("", "[green]-f buf2json[/green]")
        grid.add_row("", "[magenta]p2p[/magenta]")
        grid.add_row("", "[green]-f p2p[/green]")
        grid.add_row("", "[magenta]proto2python[/magenta]")
        grid.add_row("", "[green]-f proto2python[/green]")
        rprint(grid)
        return
    func = funcs[0]
    import platform
    if platform.system().lower() in {'windows'}:
        if platform.machine().lower() in {'amd64'}:
            cmd = 'protoc-3.18.0-win64'
        elif platform.machine().lower() in {'x86'}:
            cmd = 'protoc-3.18.0-win32'
        else:
            rprint("[bold red]未知的操作系统环境，无法运行，请提交issue[/bold red]")
            rprint(f"[bold magenta]{platform.system()}[/bold magenta]")
            rprint(f"[bold magenta]{platform.machine()}[/bold magenta]")
            return
    elif platform.system().lower() in {'linux'}:
        if platform.machine().lower() in {'x86_64'}:
            cmd = 'protoc-3.18.0-linux-x86_64'
        elif platform.machine().lower() in {'i686'}:
            cmd = 'protoc-3.18.0-linux-x86_32'
        elif platform.machine().lower() in {'aarch_64'}:
            cmd = 'protoc-3.18.0-linux-aarch_64'
        elif platform.machine().lower() in {'ppcle_64'}:
            cmd = 'protoc-3.18.0-linux-ppcle_64'
        elif platform.machine().lower() in {'s390_64'}:
            cmd = 'protoc-3.18.0-linux-s390_64'
        else:
            rprint("[bold red]未知的操作系统架构，无法运行，请提交issue[/bold red]")
            rprint(f"[bold magenta]{platform.system()}[/bold magenta]")
            rprint(f"[bold magenta]{platform.machine()}[/bold magenta]")
            return
        import stat
        os.chmod(localpath + 'bin/' + cmd, stat.S_IXOTH | stat.S_IXGRP | stat.S_IXUSR)
    elif platform.system().lower() in {'darwin'}:
        if platform.machine().lower() in {'x86_64'}:
            cmd = 'protoc-3.18.0-osx-x86_64'
        else:
            rprint("[bold red]未知的操作系统架构，无法运行，请提交issue[/bold red]")
            rprint(f"[bold magenta]{platform.system()}[/bold magenta]")
            rprint(f"[bold magenta]{platform.machine()}[/bold magenta]")
            return
        import stat
        os.chmod(localpath + 'bin/' + cmd, stat.S_IXOTH | stat.S_IXGRP | stat.S_IXUSR)
    else:
        rprint("[bold red]未知的操作系统，无法运行，请提交issue[/bold red]")
        rprint(f"[bold magenta]{platform.system()}[/bold magenta]")
        rprint(f"[bold magenta]{platform.machine()}[/bold magenta]")
        return
    infs = [__ for (_, __) in opts if _ == '-i']
    outfs = [__ for (_, __) in opts if _ == '-o']
    if not len(infs) == len(outfs) and not len(outfs) == 1:
        grid = Table.grid()
        grid.add_column(style="bold red")
        grid.add_column(style="bold red")
        grid.add_row("合法的[magenta]文件夹[/magenta]传入参数为：", "[magenta]1个[/magenta]输入文件夹(-i)以及[magenta]1个[/magenta]输出文件夹(-o)")
        grid.add_row("", "[green]-i sample_in_folder -o sample_out_folder[/green]")
        grid.add_row("", "[magenta]x个[/magenta]输入文件夹(-i)以及[magenta]1个[/magenta]输出文件夹(-o)")
        grid.add_row("", "[green]-i sample_in_folder1 -i sample_in_folder2 -i sample_in_folder3 -o sample_out_folder[/green]")
        grid.add_row("", "[magenta]x个[/magenta]输入文件夹(-i)以及[magenta]x个[/magenta]输出文件夹(-o)，其中输入输出的顺序应当一一对应")
        grid.add_row("", "[green]-i sample_in_folder1 -i sample_in_folder2 -i sample_in_folder3 -o sample_out_folder1 -o sample_out_folder2 -o sample_out_folder3[/green]")
        rprint(grid)
        return
    layout, progress, log, warn = render()
    with Live(layout, refresh_per_second=10) as live:
        if func in {'b2j', 'buf2json'}:
            if len(infs) == len(outfs):
                for inf, outf in zip(infs, outfs):
                    buf2json(cmd, localpath, inf, outf, progress, log, warn)
            elif len(outfs) == 1:
                for inf in infs:
                    buf2json(cmd, localpath, inf, outfs[0], progress, log, warn)
        elif func in {'p2p', 'proto2python'}:
            if len(infs) == len(outfs):
                for inf, outf in zip(infs, outfs):
                    proto2python(cmd, localpath, inf, outf, progress, log, warn)
            elif len(outfs) == 1:
                for inf in infs:
                    proto2python(cmd, localpath, inf, outfs[0], progress, log, warn)
        log.log("[bold green]运行完毕")


class SpeedColumn(ProgressColumn):
    def __init__(self, *args):
        super().__init__()

    def render(self, task: "Task") -> Text:
        if task.speed is None:
            return Text("no speed", style="progress.data.speed")
        else:
            return Text(f"{task.speed:.2f}/s", style="progress.data.speed")


def render():
    layout = Layout()
    layout.split_column(
        Layout(name="progress", size=1),
        Layout(name="console"),
        Layout(name="warning"),
    )
    progress = Progress(
        SpinnerColumn(),
        "[bold blue]{task.description}",
        BarColumn(bar_width=None),
        "[progress.percentage]{task.percentage:>6.2f}%",
        "•",
        TextColumn("[progress.download]{task.completed}/{task.total}", justify='right'),
        "•",
        SpeedColumn(),
        "•",
        TimeElapsedColumn(),
        "•",
        TimeRemainingColumn(),
        expand=True, auto_refresh=False)
    layout["progress"].update(progress)
    log = LogConsoleScroll()
    layout["console"].update(Panel(log, title="日志"))
    warn = LogConsoleScroll()
    layout["warning"].update(Panel(warn, title="报错"))
    return layout, progress, log, warn


def main():
    prepare()
