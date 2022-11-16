import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

# Generating the sequence of LED states for the "train"...
num_leds = 8
led_states = []
for i in range(num_leds+1):
    led_states.append(2**i-1)
for i in range(1,len(led_states)-1):
    led_states.append(255 - led_states[i])
print(led_states)

@cocotb.test()
async def test_user_module_nickoe(dut):
    dut._log.info("start")
    #clock = Clock(dut.clk, 10, units="us")
    #cocotb.fork(clock.start())
    clk_10khz = Clock(dut.clk, 1, units='ms')
    cocotb.start_soon(clk_10khz.start())


    dut._log.info("reset")
    dut.rst.value = 1
    await ClockCycles(dut.clk, 10)
    dut.pwm_width.value = 2**6-1
    dut.rst.value = 0
    dut._log.info("reset released")
    i = 0
    while i < len(led_states):
        await ClockCycles(dut.clk, 1)
        next_idx = (i+1)%len(led_states)
        if int(dut.leds.value) == led_states[next_idx]:
            i = i + 1
            dut._log.info(f"transition hit! led_state={led_states[next_idx]} {int(dut.leds.value)} :)")
            continue
        assert int(dut.leds.value) == led_states[i]

    dut._log.info("clocking form some extra cycles")
    await ClockCycles(dut.clk, 100)

    dut._log.info("sim done")


