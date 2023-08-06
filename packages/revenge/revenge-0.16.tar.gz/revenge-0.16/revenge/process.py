
from . import Colorer
import logging
logging.basicConfig(level=logging.WARN)

logger = logging.getLogger(__name__)

import frida
import colorama
colorama.init()

import os
import sys
from termcolor import cprint, colored
from prettytable import PrettyTable
import time

import atexit
import signal
import json
import pprint
from copy import copy

here = os.path.dirname(os.path.abspath(__file__))

class Process(object):

    def __init__(self, target, resume=False, verbose=False, load_symbols=None,
            device=None, envp=None):
        """

        Args:
            target (str, int, list): File name or pid to attach to. If target
                is a list, it will be set as argv.
            resume (bool, optional): Resume the binary if need be after loading?
            verbose (bool, optional): Enable verbose logging
            load_symbols (list, optional): Only load symbols from those modules
                in the list. Saves some startup time. Can use glob ('libc*')
            device (revenge.devices.*, optional): Define what device
                to connect to.
            envp (dict, optional): Specify what you want the environment
                pointer list to look like. Defaults to whatever the current
                envp is.

        Examples:
            .. code-block:: python3

                # Kick off ls
                p = revenge.Process("/bin/ls")

                # Kick off ls for /tmp with custom environment
                p = revenge.Process(["/bin/ls","/tmp/"], envp={'var1':'thing1'})
        """

        # Just variable to ensure we don't garbage collect
        self._scripts = []
        # Cache common module addrs
        self._module_by_addr_cache = {}
        self.session = None
        self.__file_name = None
        self.__file_type = None
        self.__entrypoint = None
        self._resume_addr = None
        self.__endianness = None
        self.__bits = None
        self._spawn_target = None
        self.verbose = verbose
        self.device = device or devices.LocalDevice()
        self._envp = envp
        self.target = target

        if not isinstance(load_symbols, (list, type, type(None))):
            load_symbols = [load_symbols]
        self._load_symbols = load_symbols

        self.memory = Memory(self)
        self.threads = Threads(self)
        self.modules = Modules(self)
        self.techniques = Techniques(self)

        atexit.register(self._at_exit)
        self.start_session()

        if self.run_script_generic(r"""send(Java.available)""", raw=True, unload=True)[0][0]:
            self.java = Java(self)

        # ELF binaries start up in ptrace, which causes some issues, shim at entrypoint so we can remove ptrace
        if self._spawned_pid is not None and self.file_type == 'ELF':

            # Set breakpoint at entry
            self.memory[self.entrypoint].breakpoint = True

            # Set breakpoints at exit calls
            for c in [':exit', ':_exit']:
                self.memory[c].breakpoint = True

            # Resume to remove ptrace
            self.device.device.resume(self._spawned_pid)

            #time.sleep(0.2)

        if self.device_platform == 'linux':
            try:
                str(self.threads)
            except IndexError:
                logger.error("Can't enumerate threads. Please check sysctl kernel.yama.ptrace_scope=0 or run as root.")

        # Resume file if need be
        if resume:

            # If we are using a resume variable
            if self.memory[self.entrypoint].breakpoint:
                self.memory[self.entrypoint].breakpoint = False
            
            else:
                self.device.device.resume(self._spawned_pid)


    def pause_at(self, location):
        """Pause at a given point in execution."""

        pause_location = self._resolve_location_string(location)
        self.run_script_generic('pause_at2.js', replace={"FUNCTION_ADDRESS_HERE": hex(pause_location)})

    def quit(self):
        """Call to quit your session without exiting. Do NOT continue to use this object after.
        
        If you spawned the process, it will be killed. If you attached to the
        process, frida will be cleaned out, detatched, and the process should
        continue normally.
        """
        self._at_exit()

    def _at_exit(self):
        """Called to clean-up at exit."""

        # TODO: Remove this once pytest fixes their at_exit issue
        logging.getLogger().setLevel(logging.WARN)

        try:

            # Remove breakpoints
            for addr in copy(self.memory._active_breakpoints):
                logger.debug("Removing breakpoint: " + hex(addr))
                self.memory[addr].breakpoint = False

            # Remove function replacements
            for addr in copy(self.memory._active_replacements):
                self.memory[addr].replace = None

            # Remove any on_enter interceptors
            for addr in copy(self.memory._active_on_enter):
                self.memory[addr].on_enter = None

            # Remove any instruction traces
            for t in self.threads:
                if t.trace is not None:
                    t.trace.stop()

            self.run_script_generic("""Interceptor.detachAll()""", raw=True, unload=True)

            # Unallocate our memory
            for addr in copy(self.memory._allocated_memory):
                logger.debug("Unallocating memory: " + hex(addr))
                self.memory[addr].free()

            # Unload our scripts
            for script, text in self._scripts:
                logger.debug("Unloading Script: %s", text)

                try:
                    script.unload()
                except frida.InvalidOperationError:
                    # Already unloaded probably
                    pass

            logger.debug("Done unloading")

        except (frida.InvalidOperationError, frida.TransportError) as e:
            # Looks like the program terminated. Possibly finished execution before we finished cleanup.
            if 'detached' in e.args[0] or 'closed' in e.args[0]:
                return

        # If we spawned it, kill it
        try:
            if self._spawned_pid is not None:
                return self.device.device.kill(self._spawned_pid)

        except (frida.PermissionDeniedError, frida.ProcessNotFoundError) as e:
            # This can indicate the process is already dead.
            try:
                next(x for x in self.device.device.enumerate_processes() if x.pid == self._spawned_pid)
                logger.error("Device kill permission error, with process apparently %d still alive.", self._spawned_pid)
                raise e
            except StopIteration:
                return

        # Unload anything we loaded first
        #for script in self._scripts:
        #    script.unload()

        try:

            # Genericall unstalk everything
            for thread in self.threads:
                if thread.trace is not None:
                    thread.trace.stop()
                #self.run_script_generic("Stalker.unfollow({tid})".format(tid=thread.id), raw=True, unload=True)
        
        except frida.InvalidOperationError:
            # Session is already detached.
            pass

        # Detach our session
        self.session.detach()

    
    def start_session(self):

        self._spawned_pid = None

        if self._spawn_target is not None:
            print("Spawning file\t\t\t... ", end='', flush=True)
            self._spawned_pid = self.device.device.spawn(self._spawn_target, argv=self.argv, envp=self._envp)
            cprint("[ DONE ]", "green")

        print('Attaching to the session\t... ', end='', flush=True)

        try:
            # Default attach to what we just spawned
            self.session = self.device.device.attach(self._spawned_pid or self.target)
        except frida.ProcessNotFoundError:
            logger.error('Could not find that target process to attach to!')
            exit(1)

        print(colorama.Fore.GREEN + '[ DONE ]' + colorama.Style.RESET_ALL)

    def target_type(self, x):
        # Maybe it's PID
        try:
            return int(x)

        # Probably process name
        except:
            return x

    def load_js(self, name):
        with open(os.path.join(here, "js", name), "r") as f:
            return f.read().strip()

    def get_module_by_addr(self, addr):

        addr = common.auto_int(addr)

        try:
            return self._module_by_addr_cache[addr]
        except:
            pass

        for module in self.modules:
            base = module.base
            size = module.size

            if addr >= base and addr <= base+size:
                self._module_by_addr_cache[addr] = module.name # Add to cache
                return module.name

        return None

    def run_script_generic(self, script_name, raw=False, replace=None,
            unload=False, runtime='duk', on_message=None, timeout=None,
            context=None, onComplete=None, include_js=None):
        """Run scripts that don't require anything special.
        
        Args:
            script_name (str): What script to load from the js directory
            raw (bool, optional): Should the script_name actually be considered
                the script contents?
            replace (dict, optional): Replace key strings from dictionary with
                value into script.
            unload (bool, optional): Auto unload the script. Set to true if the
                script is fully synchronous.
            runtime (str, optional): Runtime to use for this script, either
                'duk' or 'v8'.
            on_message(callable, optional): Set the on_message handler to this
                instead.
            timeout (int, optional): Modify timeout (default is 60 seconds).
                Note, this will cause the script to run async. 0 == no timeout
            context (Context, optional): Execute this script under a given
                context.
            onComplete (str, optional): If defined, this method will pause
                until the given onComplete string is returned. Basically
                allowing run_script_generic to return all things from an async
                script.
            include_js (tuple, optional): If defined, the given js files will
                be loaded into the script before the main script. This is to
                be used for shared functionality. 

        Returns:
            tuple: msg, data return from the script
        """


        msg = []
        data = []
        if include_js is None:
            include_js = ("dispose.js", "send_batch.js", "timeless.js", "telescope.js")

        # HACK: Using list for completed to make passing data back from async
        # function simpler.
        completed = [] # For use with async scripts

        if not on_message is None and not callable(on_message):
            logger.error('on_message handler must be callable.')
            return None

        def on_msg(m, d):

            if m['type'] == 'error':
                logger.error("Script Run Error: " + pprint.pformat(m['description']))
                logger.debug(pprint.pformat(m))
                return
            
            # Async is done
            if onComplete is not None and m['payload'] == onComplete:
                completed.append(True)
                return

            logger.debug("on_message: {}".format([m,d]))

            msg.append(m['payload'] if 'payload' in m else None)
            data.append(d)

        on_message = on_msg if on_message is None else on_message

        js = ""

        if include_js is not None:

            if not isinstance(include_js, (tuple, list)):
                include_js = (include_js,)

            for js_file in include_js:
                js += self.load_js(js_file) + "\n"


        if not raw:
            js += self.load_js(script_name)
        else:
            js += script_name

        if replace is not None:
            assert type(replace) == dict, "Unexpected replace type of {}".format(type(replace))

            for key, value in replace.items():
                js = js.replace(key, value)

        if timeout is not None:
            js = "setTimeout(function() {" + js + "}," + str(timeout) + ")"
            # Forcing unload to false since we don't know if it's done.
            unload = False

        # Let context decide when to run this.
        if context is not None:
            # Processing is done, let context know.
            return context.run_script_generic(script_name)

        logger.debug("Running script: %s", js)

        script = self.session.create_script(js, runtime=runtime)

        script.on('message', on_message)

        try:
            script.load()
        except Exception as e:
            logger.error("Error running script! " + str(e))
            script.unload()
            return

        # If we're async, wait until we're done
        # This needs to happen before unlink so we ensure we get all messages
        while onComplete is not None and completed == []:
            time.sleep(0.01)
        
        if unload:
            # TODO: Maybe not do this for every unload? Not sure performance impact...
            try:
                script.exports.dispose()
            except frida.core.RPCException as e:
                # We're OK if this didn't exist.
                if "unable to find method" not in e.args[0]:
                    raise
            script.unload()
        else:
            # Inserting instead of appending since earlier scripts need to be unloaded later
            self._scripts.insert(0, [script, js])


        return msg, data

    def _resolve_location_string(self, location):
        """Take location string and resolve it into an integer address."""
        #assert type(location) is str, "Invalid call to resolve_location_string with type {}".format(type(location))
        if isinstance(location, int):
            return types.Pointer(location)

        return self.modules.lookup_symbol(location)

    def __repr__(self):
        attrs = ['Process', self.file_name + ":" + str(self.pid)]
        return '<' + ' '.join(attrs) + '>'

    ############
    # Property #
    ############

    @property
    def argv(self):
        """list: argv for this process instantitation."""
        return self.__argv

    @argv.setter
    def argv(self, argv):
        if not isinstance(argv, (list, tuple)): raise RevengeInvalidArgumentType("argv must be list or tuple type.")
        self.__argv = argv

    @property
    def device_platform(self):
        """Wrapper to discover the device's platform."""

        def message(x, y):
            self.device_platform = x['payload']

        try:
            return self.__device_platform
        except:
            pass

        js = "send(Process.platform)"
        script = self.session.create_script(js)
        script.on('message', message)
        script.load()
        return self.__device_platform

    @device_platform.setter
    def device_platform(self, platform):
        self.__device_platform = platform

    @property
    def pid(self):
        return self.session._impl.pid

    @property
    def entrypoint(self):
        """int: Returns the entrypoint for this running program."""
        mod = self.modules[self.file_name]

        if self.__entrypoint is None:
            if self.file_type == 'ELF':
                self.__entrypoint = types.Pointer(int(self.run_script_generic("""send(Memory.readPointer(ptr(Number(Process.getModuleByName('{}').base) + 0x18)))""".format(self.file_name), raw=True, unload=True)[0][0],16))
                
                if mod.elf.type_str == 'DYN':
                    self.__entrypoint = types.Pointer(self.__entrypoint + mod.base)

            else:
                logger.warn('entrypoint not implemented for file of type {}'.format(self.file_type))
                return None
            
        # TODO: Windows?
        # TODO: Mac?

        return self.__entrypoint

    @property
    def endianness(self):
        """Determine which endianness this binary is. (little, big)"""

        if self.__endianness != None:
            return self.__endianness

        if self.device_platform == 'windows':
            # TODO: Technically assumption, but like 99% of the time it's right.
            self.__endianness = 'little'

        elif self.file_type == 'ELF':
            endianness = self.run_script_generic("""send(ptr(Number(Process.enumerateModulesSync()[0].base) + 5).readS8())""", raw=True, unload=True)[0][0]
            self.__endianness = 'little' if endianness == 1 else 'big'

        else:
            logger.warn("Unhandled endianness check for ({}, {}), assuming little".format(self.file_type, self.device_platform))

        return self.__endianness

    @property
    def file_type(self):
        """Guesses the file type."""

        # TODO: Android processes we attach to can't getModuleByName for their file name...
        # Maybe use "app_process64" instead... Or resolve the first module and go with that..
        if isinstance(self.device, devices.AndroidDevice):
            return "ELF"

        # TODO: Update this with other formats. PE/COFF/MACHO/etc
        if self.__file_type is None:
            if self.run_script_generic("""send('bytes', Process.getModuleByName('{}').base.readByteArray(4))""".format(self.file_name), raw=True, unload=True)[1][0] == b'\x7fELF':
                self.__file_type = 'ELF'
            elif self.run_script_generic("""send('bytes', Process.getModuleByName('{}').base.readByteArray(2))""".format(self.file_name), raw=True, unload=True)[1][0] == b'MZ':
                self.__file_type = "PE"
            else:
                self.__file_type = 'Unknown'

        return self.__file_type

    @property
    def file_name(self):
        """str: The base file name."""
        # TODO: This assumes the base module is always first...
        if self.__file_name is None:
            self.__file_name = self.run_script_generic("""send(Process.enumerateModulesSync())""", raw=True, unload=True)[0][0][0]['name']

        return self.__file_name

    @property
    def bits(self):
        """int: How many bits is the CPU?"""
        if self.__bits == None:
            self.__bits = self.run_script_generic("""send(Process.pointerSize);""", raw=True, unload=True)[0][0] * 8
        
        return self.__bits

    @property
    def arch(self):
        """str: What architecture? (x64, ia32, arm, others?)"""
        try:
            return self.__arch
        except:
            known_arch = ['x64', 'ia32', 'arm']
            arch = self.run_script_generic("""send(Process.arch);""", raw=True, unload=True)[0][0]

            if arch not in known_arch:
                raise Exception("Unknown arch returned from Frida: {}".format(arch))
            self.__arch = arch
            return self.__arch

    @property
    def verbose(self):
        """bool: Output extra debugging information."""
        return self.__verbose

    @verbose.setter
    def verbose(self, verbose):
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
            #logger.setLevel(logging.DEBUG)
        self.__verbose = verbose

    @property
    def target(self):
        """str, int: Target for this session."""
        return self.__target

    @target.setter
    def target(self, target):

        # target set will implicitly set argv
        if isinstance(target, (list, tuple)):
            self.argv = list(target)
            target = target[0]

        else:
            # Place holder until we resolve target
            self.argv = [target]


        # Check if this is a pid
        try:
            p = next(x for x in self.device.device.enumerate_processes() if x.pid == common.auto_int(target))
            target = p.pid
            self.__file_name = p.name
            self.argv[0] = p.name

        except (StopIteration, ValueError):
            pass

        if isinstance(target, str):
            full_path = os.path.abspath(target)
            self.__file_name = os.path.basename(full_path)

            # If this string points to an actual file, we will launch it later
            if os.path.isfile(full_path):
                self._spawn_target = full_path
            

        self.__target = target

    @property
    def alive(self):
        """bool: Is this process still alive?"""
        try:
            next(True for x in self.device.device.enumerate_processes() if x.pid == self.pid)
            return True
        except StopIteration:
            return False

    @property
    def device(self):
        """frida.core.Device: Frida device object for this connection."""
        return self.__device

    @device.setter
    def device(self, device):
        assert isinstance(device, devices.BaseDevice), "Device must be an instantiation of one of the devices defined in revenge.devices."
        self.__device = device
        """
        if isinstance(device, devices.LocalDevice):
            self.__device = device.device

        elif isinstance(device, devices.AndroidDevice):
            self.__device = device.device

        else:
            error = "Unexpected/unhandled device type of {}".format(type(device))
            logger.error(error)
            raise Exception(error)
        """
    
    @property
    def BatchContext(self):
        """Returns a BatchContext class for this process.

        Example:
            .. code-block:: python3

                with process.BatchContext() as context:
                    something(context=context)

        """
        return lambda *args, **kwargs: BatchContext(self, *args, **kwargs)

    @property
    def _envp(self):
        """dict: This holds the USER SPECIFIED environment variables. If you
        do not specify envp, this will be empty but your program will still
        have the default environment."""
        return self.__envp

    @_envp.setter
    def _envp(self, envp):
        if not isinstance(envp, (dict, type(None))):
            raise RevengeInvalidArgumentType("_envp must be instance of dict or None. Got type {}".format(type(envp)))

        self.__envp = envp


from . import common, types, config, devices
from .memory import Memory
from .threads import Threads
from .modules import Modules
from .java import Java
from .contexts import BatchContext
from .exceptions import *
from .techniques import Techniques

# Doc fixups
Process.BatchContext.__doc__ += BatchContext.__init__.__doc__
Process.__doc__ = Process.__init__.__doc__

def sigint_handler(sig, frame):
    sys.exit()

signal.signal(signal.SIGINT, sigint_handler)

def main():
    signal.signal(signal.SIGINT, sigint_handler)

    global process
    process = Process()

    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
