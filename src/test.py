import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

# Generating the sequence of LED states for the "train"... there
# probably exist a better way to do this...
num_leds = 8
led_states = []
for i in range(num_leds+1):
    led_states.append(2**i-1)
for i in reversed(led_states):
    led_states.append(i)
led_states.pop(num_leds)
led_states.pop(num_leds*2-2)

print(led_states)

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
    i = 0
    while i < len(led_states)-1:
        await ClockCycles(dut.clk, 1000)
        dut._log.info(f"waiting for led_state={led_states[i]} {int(dut.leds.value)}")
        if int(dut.leds.value) == led_states[i+1]:
            i = i + 1
            dut._log.info(f"transition hit! :)")
            continue
        assert int(dut.leds.value) == led_states[i]

    dut._log.info("sim done")


