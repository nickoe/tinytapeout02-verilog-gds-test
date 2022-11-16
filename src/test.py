import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

# Generating the sequence of LED states for the "train"... there
# probably exist a better way to do this...
num_leds = 8
led_states = []
for i in range(num_leds):
    led_states.append(2**i-1)
for i in reversed(led_states):
    led_states.append(i)
led_states.pop(num_leds)
led_states.pop(num_leds*2-2)



@cocotb.test()
async def test_user_module_nickoe(dut):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.fork(clock.start())

    dut._log.info("reset")
    dut.rst.value = 1
    await ClockCycles(dut.clk, 10)
    dut.rst.value = 0
    dut._log.info("reset released")
    for i in range(10):
        dut._log.info("clocking for a bit")
        await ClockCycles(dut.clk, 10000)
    dut._log.info("sim done")


