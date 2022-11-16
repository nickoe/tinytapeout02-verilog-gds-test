#!/usr/bin/env python3


from litex.build.generic_platform import *
from litex.build.sim import SimPlatform
from litex.build.sim.config import SimConfig
from litex.soc.cores.led import LedChaser
from litex.soc.integration.builder import *
# from amaranth.compat import *
from migen import *

_io = [
    ("io_in", 0, Pins(8)),
    ("io_out", 0, Pins(8)),
]


_io_sim = [
    ("sys_clk", 0, Pins(1)),
    ("sys_rst", 0, Pins(1)),
    ("io_in", 0, Pins(8)),
    ("io_out", 0, Pins(8)),
]


class MyPlatform(GenericPlatform):
    def __init__(self):
        GenericPlatform.__init__(self, device="tapeout", io=_io, name="user_module_nickoe")

class TinyTapeoutPlatform(SimPlatform):
    def __init__(self):
        SimPlatform.__init__(self, device="SIM", io=_io_sim, name="sim")


class MyModule(Module):
    def __init__(self, platform, sys_clk_freq, simhack=False):
        print("NICK DEBUG MyModule")
        io_in = platform.request_all("io_in")

        # SoC attributes ---------------------------------------------------------------------------
        self.platform     = platform
        self.sys_clk_freq = sys_clk_freq
        self.constants    = {}
        self.csr_regions  = {}

        # CRG --------------------------------------------------------------------------------------
        if simhack:
            self.submodules.crg = CRG(clk=platform.request("sys_clk"), rst=platform.request("sys_rst"))
        else:
            self.submodules.crg = CRG(clk=io_in[0], rst=io_in[1])


        # Leds -------------------------------------------------------------------------------------
        ledchaser = LedChaser(
            pads         = platform.request_all("io_out"),
            sys_clk_freq = sys_clk_freq)
        self.submodules.leds = ledchaser
        # control of brightness...
        # TODO make inputs control brightness with this pwm signal
        ledchaser.add_pwm(default_width=900, default_period=1024, with_csr=False)

        #self.add_csr("leds")

        #self.comb += ledchaser.mode.eq(1)

        #platform.request("io_out", 0),

        # Disable / enable PWM
        self.comb += ledchaser.pwm.enable.eq(io_in[2])


        # new matching in newer litex?
        #platform.request_remaining("io_in")


        # Only in SimPlatform, has to be enabled for tracing to run
        if platform.device == "SIM":
            self.comb += platform.trace.eq(1)


def main():
    sys_clk_freq = int(10e3)

    # Verilog for tapeout ----------------------------------------------------------------------
    non_sim_platform = MyPlatform()
    non_sim_platform.name = "user_module_nickoe"
    my_mod = MyModule(non_sim_platform, sys_clk_freq, simhack=False)
    v_output = non_sim_platform.get_verilog(fragment=my_mod, name=non_sim_platform.name)
    v_output.write(f"src/{non_sim_platform.name}.v")
    exit(0)

    # Simulation platform ----------------------------------------------------------------------
    platform = TinyTapeoutPlatform()
    sim = MyModule(platform, sys_clk_freq, simhack=True)
    sim_config = SimConfig()
    sim_config.add_clocker("sys_clk", freq_hz=sys_clk_freq)
    #sim_config.add_clocker("io_in0[0]", freq_hz=sys_clk_freq)
    platform.build(sim, sim_config=sim_config, interactive=True, build_dir="./litex_out", run=True,
                   trace=True,
                   trace_fst=True,
                   trace_start=0,
                   trace_end=-1,
                   )


if __name__ == "__main__":
    # Run with args --trace-fst --trace --trace-end 10000000000000
    main()
