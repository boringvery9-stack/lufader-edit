import adafruit_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.channel_pressure import ChannelPressure
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
import busio
import board
import usb_midi

MIDI_AUX_TX_PIN = board.GP16
MIDI_AUX_RX_PIN = board.GP17

class MidiManager:
    def __init__(self):
        self.last_cc_values_sent = {}
        self.last_aftertouch_values_sent = {}
        self.last_at_values_per_slider = {}
        self.output_muted = False

        uart = busio.UART(
            MIDI_AUX_TX_PIN,
            MIDI_AUX_RX_PIN,
            baudrate=31250,
            timeout=0.001
        )
        self.midi = adafruit_midi.MIDI(
            midi_in=usb_midi.ports[0],
            midi_out=usb_midi.ports[1],
            in_channel=0,
            out_channel=0
        )
        self.trs_midi = adafruit_midi.MIDI(
            midi_in=uart,
            midi_out=uart,
            in_channel=0,
            out_channel=0,
            debug=False,
        )

    def receive_cc(self):
        msg = self.midi.receive()
        if msg is not None and isinstance(msg, ControlChange):
            return (msg.control, msg.channel + 1) 
        
        msg = self.trs_midi.receive()
        if msg is not None and isinstance(msg, ControlChange):
            return (msg.control, msg.channel + 1) 
        return None

    def receive_cc_or_at(self):
        msg = self.midi.receive()
        if msg is not None:
            if isinstance(msg, ControlChange):
                return ("CC", msg.control, msg.channel + 1)
            if isinstance(msg, ChannelPressure):
                return ("AT", msg.pressure, msg.channel + 1)
        
        msg = self.trs_midi.receive()
        if msg is not None:
            if isinstance(msg, ControlChange):
                return ("CC", msg.control, msg.channel + 1)
            if isinstance(msg, ChannelPressure):
                return ("AT", msg.pressure, msg.channel + 1)
        return None
    
    def flush_receive_buffer(self):
        while self.midi.receive() is not None:
            pass
        while self.trs_midi.receive() is not None:
            pass

    def has_cc_value_changed(self, cc_number, channel, cc_value):
        key = (cc_number, channel)
        return self.last_cc_values_sent.get(key, -1) != cc_value

    def send_cc(self, cc_list_with_channels, cc_value):
        if self.output_muted:
            return
        for cc_number, channel in cc_list_with_channels:
            if self.has_cc_value_changed(cc_number, channel, cc_value):
                key = (cc_number, channel)
                self.last_cc_values_sent[key] = cc_value
                cc_msg = ControlChange(cc_number, cc_value, channel=channel)
                self.midi.send(cc_msg, channel=channel)
                self.trs_midi.send(cc_msg, channel=channel)

    def get_last_cc_value_sent(self, cc_number, channel):
        key = (cc_number, channel)
        return self.last_cc_values_sent.get(key, 16)
    
    def has_aftertouch_value_changed(self, channel, pressure):
        return self.last_aftertouch_values_sent.get(channel, -1) != pressure
    
    def send_aftertouch(self, channels, pressure, slider_idx=0, page_idx=0, bank_idx=0):
        if self.output_muted:
            return
        slider_key = (slider_idx, page_idx, bank_idx)
        self.last_at_values_per_slider[slider_key] = pressure
        
        for channel in channels:
            if self.has_aftertouch_value_changed(channel, pressure):
                self.last_aftertouch_values_sent[channel] = pressure
                at_msg = ChannelPressure(pressure, channel=channel)
                self.midi.send(at_msg, channel=channel)
                self.trs_midi.send(at_msg, channel=channel)
    
    def get_last_at_value_per_slider(self, slider_idx, page_idx, bank_idx):
        key = (slider_idx, page_idx, bank_idx)
        return self.last_at_values_per_slider.get(key, 16)

    def send_note_pulse(self, channels, note_number, velocity=127):
        """發送 Note On 與 Note Off 的瞬間脈衝"""
        if self.output_muted:
            return
        for channel in channels:
            note_on_msg = NoteOn(note_number, velocity, channel=channel)
            note_off_msg = NoteOff(note_number, 0, channel=channel)
            
            self.midi.send(note_on_msg, channel=channel)
            self.trs_midi.send(note_on_msg, channel=channel)
            
            self.midi.send(note_off_msg, channel=channel)
            self.trs_midi.send(note_off_msg, channel=channel)

midi_manager = MidiManager()