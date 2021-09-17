"""
Module is responsible for hardware interrupt
handling dedicated to micrOS framework.
- Setting up interrupt memory buffer from config
- Configure time based and external interrupts

- Time based IRQ:
    - Simple (timer0) with fix period callback
    - Advanced (timer1) - time stump ! LM function;
            0-6:0-24:0-59:0-59!system heartbeat; etc.

Designed by Marcell Ban aka BxNxM
"""
#################################################################
#                            IMPORTS                            #
#################################################################
from machine import Pin
from ConfigHandler import cfgget, console_write
from InterpreterCore import execLMPipe
from LogicalPins import physical_pin
if cfgget('cron'):
    # Only import when enabled - memory usage optimization
    from Scheduler import scheduler

#################################################################
#            CONFIGURE INTERRUPT MEMORY BUFFER                  #
#################################################################


def emergency_mbuff():
    emergency_buff_kb = cfgget('irqmembuf')
    if cfgget('extirq') or cfgget("timirq"):
        from micropython import alloc_emergency_exception_buf
        console_write("[IRQ] Interrupts was enabled, alloc_emergency_exception_buf={}".format(emergency_buff_kb))
        alloc_emergency_exception_buf(emergency_buff_kb)
    else:
        console_write("[IRQ] Interrupts disabled, skip alloc_emergency_exception_buf configuration.")

#################################################################
#                       TIMER INTERRUPT(S)                      #
#################################################################

#############################################
#    [TIMER 0] TIMIRQ CBFs - LM executor    #
#############################################


def enableInterrupt():
    """
    Set task pool executor in interrupt timer0
    Input: timirq(bool), timirqseq(ms), timirqcbf(str)
    """
    console_write("[IRQ] TIMIRQ SETUP: {} SEQ: {}".format(cfgget("timirq"), cfgget("timirqseq")))
    console_write("|- [IRQ] TIMIRQ CBF:{}".format(cfgget('timirqcbf')))
    if cfgget("timirq"):
        from machine import Timer
        # INIT TIMER IRQ with callback function wrapper
        lm_str = cfgget('timirqcbf')
        timer = Timer(0)
        timer.init(period=int(cfgget("timirqseq")), mode=Timer.PERIODIC,
                   callback=lambda timer: execLMPipe(lm_str))


#############################################
#    [TIMER 1] TIMIRQ CRON - LM executor    #
#############################################

def timirq_cbf_sched(tasks, seq):
    """
    Input:
        tasks: str
        seq: sec (int)
    """
    try:
        # Execute CBF LIST from local cached config with timirqseq in sec
        scheduler(tasks, seq)
    except Exception as e:
        console_write("[IRQ] TIMIRQ (cron) callback: {} error: {}".format(tasks, e))


def enableCron():
    """
    Set time stump based scheduler aka cron in timer1
    Input: cron(bool), cronseq(ms), crontasks(str)
    """
    console_write("[IRQ] CRON IRQ SETUP: {} SEQ: {}".format(cfgget(cfgget('cron')), cfgget("cronseq")))
    console_write("|- [IRQ] CRON CBF:{}".format(cfgget('crontasks')))
    if cfgget("cron") and cfgget('crontasks').lower() != 'n/a':
        from machine import Timer
        # INIT TIMER 1 IRQ with callback function wrapper
        lm_str = cfgget('crontasks')
        sample = int(cfgget("cronseq")/1000)
        timer = Timer(1)
        timer.init(period=int(cfgget("cronseq")), mode=Timer.PERIODIC,
                   callback=lambda timer: timirq_cbf_sched(lm_str, sample))


#################################################################
#                  EVENT/EXTERNAL INTERRUPT(S)                  #
#################################################################
# trigger=Pin.IRQ_FALLING   signal HIGH to LOW
# trigger=Pin.IRQ_RISING    signal LOW to HIGH
#################################################################


def initEventIRQs():
    """
    EVENT INTERRUPT CONFIGURATION - multiple
    """
    irqdata = ((cfgget("irq1"), cfgget("irq1_trig"), cfgget("irq1_cbf")),
               (cfgget("irq2"), cfgget("irq2_trig"), cfgget("irq2_cbf")),
               (cfgget("irq3"), cfgget("irq3_trig"), cfgget("irq3_cbf")),
               (cfgget("irq4"), cfgget("irq4_trig"), cfgget("irq4_cbf")))

    for i, data in enumerate(irqdata):
        irq, trig, cbf = data
        console_write("[IRQ] EXTIRQ SETUP - EXT IRQ{}: {} TRIG: {}".format(i+1, irq, trig))
        console_write("|- [IRQ] EXTIRQ CBF: {}".format(cbf))
        pin = physical_pin('irq{}'.format(i+1))       # irq1, irq2, etc.
        if irq and pin:
            trig = trig.strip().lower()
            # Init event irq with callback function wrapper
            pin_obj = Pin(pin, Pin.IN, Pin.PULL_UP)
            # [IRQ] - event type setup
            if trig == 'down':
                pin_obj.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: execLMPipe(cbf))
                return
            if trig == 'both':
                pin_obj.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=lambda pin: execLMPipe(cbf))
                return
            pin_obj.irq(trigger=Pin.IRQ_RISING, handler=lambda pin: execLMPipe(cbf))


#################################################################
#                         INIT MODULE                           #
#################################################################


emergency_mbuff()
