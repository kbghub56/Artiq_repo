from artiq.experiment import *
import numpy as np
import time as tm

class AmplitudeRamp(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("urukul0_ch0")
        self.setattr_device("urukul0_cpld")
        # self.setattr_device("scheduler")
        self.lowerlim=0.0001
        self.setattr_argument("frequency", NumberValue(default=1, unit="MHz", ndecimals=6))
        self.setattr_argument("ramp_rate", NumberValue(default=1, ndecimals=6))
        self.setattr_argument("target_amplitude", NumberValue(default=0, min=self.lowerlim, max=1, ndecimals=6))
        self.setattr_argument("attenuation", NumberValue(default=0, unit="dB", min=0, max=10))
        self.setattr_argument("time_step", NumberValue(default=100 * ms, unit="ms", min=0))
        self.amplitude=self.get_dataset("UrukulCh0_RFamp")
        self.setattr_device("scheduler")
       # self.target_amplitude=round(self.target_amplitude





    # @kernel
    # def initialize_urukul(self):
    #     self.core.reset()
    #     self.urukul0_ch0.cpld.init()
    #     self.urukul0_ch0.init()
    #     self.urukul0_ch0.sw.on()
    #
    #     delay(5 * ms)

    @kernel
    def krun(self):
        self.core.reset()
        self.urukul0_ch0.cpld.init()
        self.urukul0_ch0.init()
       # amp = self.urukul0_ch0.get_amplitude()
        delay(1 * ms)
        self.urukul0_ch0.set(frequency=self.frequency,amplitude=self.amplitude)
        # if (self.amplitude==self.lowerlim):
        #     self.urukul0_ch0.sw.on()
        print(self.amplitude)
        delay(2*ms)
        #self.urukul0_ch0.sw.on()
        amp=self.amplitude
        delay(1*ms)
        # sign = (self.target_amplitude - self.urukul0_ch0.get_amplitude()) / np.abs(
        #     self.target_amplitude - self.urukul0_ch0.get_amplitude())
        # self.ramp = np.array([self.urukul0_ch0.get_amplitude() + i * self.ramp_rate * sign for i in range(
        #     int(np.abs(self.urukul0_ch0.get_ampltiude() - self.target_amplitude) / self.ramp_rate))])
        # self.ramp[-1] = self.target_amplitude

       # delay(10000 * ms)

        #self.initialize_urukul()
        #self.urukul0_ch0.sw.off()

        if self.target_amplitude > amp:
            #delay(10*ms)
            while amp < self.target_amplitude:
                #delay(10 * ms)
                # try:
                #     if self.scheduler.check_pause():
                #         self.core.comm.close()
                #         self.scheduler.pause()
                # except TerminationRequested:
                #     print("Terminated gracefully")
                #     return
            #    self.check_termination()

                ampplus=(amp + self.ramp_rate)
                self.urukul0_ch0.set(frequency=self.frequency,amplitude=ampplus)
                delay(1*ms)
                self.set_dataset("UrukulCh0_RFamp", ampplus, broadcast=True, persist=True)
                amp  =ampplus
                delay(self.time_step)

        else:

            while amp > self.target_amplitude:
                # try:
                #     if self.scheduler.check_pause():
                #         self.core.comm.close()
                #         self.scheduler.pause()
                # except TerminationRequested:
                #     print("Terminated gracefully")
                #     return
             #   self.check_termination()

                ampminus=(amp - self.ramp_rate)
                self.urukul0_ch0.set(frequency=self.frequency, amplitude=ampminus)
                delay(1 * ms)
                self.set_dataset("UrukulCh0_RFamp", ampminus, broadcast=True, persist=True)
                amp = ampminus
                delay(self.time_step)
                # self.urukul0_ch0.sw.off()
                # delay(1*ms)

        self.urukul0_ch0.set(frequency=self.frequency,amplitude=self.target_amplitude)
        delay(2 * ms)
        self.set_dataset("UrukulCh0_RFamp",self.target_amplitude, broadcast=True, persist=True )

    @rpc(flags={"async"})
    def check_termination(self):
        try:
            if self.scheduler.check_pause():
                self.core.comm.close()
                self.scheduler.pause()
        except TerminationRequested:
            print("Terminated gracefully")
            return

    def run(self):
        self.krun()







