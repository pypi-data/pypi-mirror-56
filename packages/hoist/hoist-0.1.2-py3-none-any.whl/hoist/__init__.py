import atexit

import aiohttp

__version__ = '0.1.2'

from pathlib import Path
from aiohttp import web
import asyncio
import json
import os
import sys
import uuid
from collections import namedtuple
from typing import Optional, Union
import webbrowser
import websockets
from jinja2 import Template

from . import util

ENV = 'env'
CMD = 'cmd'
REF = 'ref'
SEQ = 'seq'
PAR = 'par'

DEFAULT_SECTION = 'hoist.defaults'
CMD_KEYS = {CMD, REF, SEQ, PAR}
RESERVED_KEYS = CMD_KEYS | {ENV}

Command = namedtuple('Command', ['command', 'environ', 'alias'])
Parallel = namedtuple('Parallel', ['commands'])
Sequence = namedtuple('Sequence', ['commands'])
FlowType = Union[Parallel, Sequence]


def resolve_commands(config, input_arguments, command_name, parent_commands=None):
    parent_commands = list(parent_commands or [])

    command = util.nested_keys(config, command_name)
    if command is None:
        raise Exception(f'Command {command_name!r} not found')

    if len(CMD_KEYS & set(command)) != 1:
        raise Exception(f'Invalid command: {command}')

    if REF in command:
        command = dict(command)
        command[PAR] = [command.pop(REF)]

    if PAR in command:
        resolved = []
        for ref in command[PAR]:
            resolved.append(resolve_commands(
                config=config,
                input_arguments=input_arguments,
                command_name=ref,
                parent_commands=parent_commands + [command]
            ))
        return Parallel(commands=resolved)

    if SEQ in command:
        resolved = []
        for ref in command[SEQ]:
            resolved.append(resolve_commands(
                config=config,
                input_arguments=input_arguments,
                command_name=ref,
                parent_commands=parent_commands + [command]
            ))
        return Sequence(resolved)

    commands = [command] + parent_commands
    defaults = dict(util.nested_keys(config, DEFAULT_SECTION) or {})

    environment_variables = dict(defaults.pop(ENV, {}))
    input_variables = dict(defaults)

    for cmd in commands:
        for key in cmd:
            if key not in RESERVED_KEYS:
                input_variables[key] = cmd[key]
        environment_variables.update(cmd.get(ENV, {}))

    input_variables.update(input_arguments)

    for mapping in (environment_variables, input_variables):
        for key, value in mapping.items():
            if isinstance(value, str):
                mapping[key] = Template(value).render(env=os.environ)

    command_values = command[CMD]
    if not isinstance(command_values, list):
        command_values = [command_values]

    return Sequence(commands=[
        Command(
            command=Template(command_value).render(env=os.environ, **input_variables),
            environ=environment_variables,
            alias=input_variables.get('alias'),
        )
        for command_value in command_values
    ])


async def gather_stream(queue, connections):
    while True:
        message = await queue.get()
        if message is None:
            return

        for connection in set(connections):
            try:
                await connection.send(json.dumps(message))
            except:
                pass


async def stream_pipe(stream, out):
    while True:
        try:
            line = await stream.readline()
            line = line.decode().rstrip()
            await out(line)
            if not line:
                break
        except ValueError:
            pass


async def execute_command(command_data, loop, queue, processes):
    env = os.environ.copy()
    for key, value in command_data.environ.items():
        env[key] = str(value)

    process = await asyncio.create_subprocess_shell(
        command_data.command,
        loop=loop,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env,
        bufsize=0,
        limit=1024 * 128,
    )

    processes.append(process)

    def queue_output(type):
        async def out(message):
            output_message = dict(
                alias=command_data.alias or command_data.command,
                id=str(uuid.uuid4()),
                cmd=command_data.command,
                pid=process.pid,
                std=type,
                message=message,
            )
            await queue.put(output_message)

        return out

    await asyncio.gather(
        stream_pipe(process.stdout, queue_output(type='out')),
        stream_pipe(process.stderr, queue_output(type='err')),
    )

    processes.remove(process)


def init_loop():
    if sys.platform == 'win32':
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    return asyncio.get_event_loop()


async def serve_websockets(host, port, connections):
    async def consumer_handler(websocket, path):
        connections.add(websocket)
        try:
            print(f'Websocket connection established!')
            await websocket.recv()
        except websockets.exceptions.ConnectionClosed:
            print(f'Websocket connection closed!')
        finally:
            connections.remove(websocket)

    print(f'Opening socket: ws://{host}:{port}')
    await websockets.serve(consumer_handler, host, port)


async def check_signal(signal):
    while True:
        await asyncio.sleep(0.5)
        if signal():
            sys.exit(0)


async def iterate(command: Union[FlowType, Command], loop, queue, processes):
    if isinstance(command, Parallel):
        await asyncio.gather(*[
            iterate(command=child_command, loop=loop, queue=queue, processes=processes)
            for child_command in command.commands
        ])
    elif isinstance(command, Sequence):
        for child_command in command.commands:
            await iterate(command=child_command, loop=loop, queue=queue, processes=processes)
    elif isinstance(command, Command):
        await execute_command(command_data=command, loop=loop, queue=queue, processes=processes)


async def execute_workflow(command: Union[FlowType, Command], loop, queue, connections, signal):
    if connections is not None:
        print('Waiting for first websocket connection...')
        while not connections:
            await asyncio.sleep(0.1)

    processes = []
    atexit.register(lambda: exit_processes(processes))

    await iterate(command, loop, queue, processes)
    signal.append(None)


def exit_processes(processes: list):
    for process in processes:
        try:
            if process.poll() is None:
                process.kill()
        except:
            pass


def start_hoist(command: FlowType, host: str, port: Optional[int]):
    loop = init_loop()
    queue = asyncio.Queue()
    connections = set()
    signal = []
    webapp_port = util.find_free_port()
    browser_url = f'http://{host}:{webapp_port}/index.html?host={host}&port={port}'
    print(f'Opening browser: {browser_url}')
    webbrowser.open_new_tab(browser_url)
    loop.run_until_complete(
        asyncio.gather(
            serve_websockets(host=host, port=port, connections=connections),
            run_web_app(host=host, port=webapp_port),
            execute_workflow(command=command, loop=loop, queue=queue, connections=connections, signal=signal),
            gather_stream(queue=queue, connections=connections),
            check_signal(lambda: signal)
        )
    )


def log_workflow(command, indent=0):
    offset = indent * ' '
    if isinstance(command, (Parallel, Sequence)):
        print(offset, '-', type(command).__name__)
        for child in command.commands:
            log_workflow(child, indent + 2)
    else:
        print(offset, '*', command)


async def run_web_app(host, port):
    app = web.Application()
    app.router.add_static('/', path=str(Path(__file__).parent / 'web_files'))

    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner, host=host, port=port)
    await site.start()


def main():
    try:
        input_arguments = util.parse_args()
        config = util.load_config(input_arguments.pop('hoist_file'))
        hoist_addr, hoist_port = input_arguments.pop('hoist_addr'), input_arguments.pop('hoist_port')
        command_names = input_arguments.pop('command')

        all_commands = []
        for command_name in command_names:
            all_commands.append(resolve_commands(config, input_arguments, command_name))

        command = Sequence(all_commands)
        print('=' * 80)
        print()
        log_workflow(command=command)
        print()
        print('=' * 80)
        print()
        start_hoist(command=command, host=hoist_addr, port=hoist_port)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
