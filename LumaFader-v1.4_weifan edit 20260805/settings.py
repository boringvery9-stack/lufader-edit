import json

class Settings:
    
    DEFAULT_GLOBAL_CHANNEL = 1 
    DEFAULT_GLOBAL_MESSAGE_TYPE = "CC"
    VALID_MESSAGE_TYPES = ("CC", "AT")

    VALID_LOOP_TYPES = ("loop", "hold")
    DEFAULT_LOOP_TYPE = "loop"
    DEFAULT_CC_RESOLUTION = 0   
    DEFAULT_TRIM_SILENCE = True
    DEFAULT_CC_RESET = True
    
    DEFAULT_GLOBAL_SLIDER_CHANNELS = ["", "", "", ""]
    DEFAULT_BANK_SLIDER_CHANNELS = [["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""]]

    DEFAULT_GLOBAL_CC_BANK = [0, 1, 2, 3]
    DEFAULT_PAGE_1_BANKS = [[4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15], [16, 17, 18, 19]]
    DEFAULT_PAGE_2_BANKS = [[20, 21, 22, 23], [24, 25, 26, 27], [28, 29, 30, 31], [32, 33, 34, 35]]
    DEFAULT_PAGE_3_BANKS = [[36, 37, 38, 39], [40, 41, 42, 43], [44, 45, 46, 47], [48, 49, 50, 51]]
    DEFAULT_PAGE_4_BANKS = [[52, 53, 54, 55], [56, 57, 58, 59], [60, 61, 62, 63], [64, 65, 66, 67]]
    DEFAULT_PAGE_BUTTONS = [[8, 9, 10, 11], [12, 13, 14, 15], [16, 17, 18, 19], [20, 21, 22, 23]]
    DEFAULT_BUTTON_CHANNELS = [["", "", "", ""], ["", "", "", ""], ["", "", "", ""], ["", "", "", ""]]
    DEFAULT_BUTTON_TYPES = [["CC", "CC", "CC", "CC"], ["CC", "CC", "CC", "CC"], ["CC", "CC", "CC", "CC"], ["CC", "CC", "CC", "CC"]]

    def __init__(self, settings_path="settings.json"):
        self.settings_path = settings_path
        self.settings = {}
        self.load_settings()

    def load_settings(self):
        try:
            with open(self.settings_path, 'r') as f:
                self.settings = json.load(f)
            if not self._validate_settings():
                print("Invalid settings in file. Using defaults.")
                self._use_defaults()
        except Exception as e:
            print(f"Error loading settings: {str(e)}. Using defaults.")
            self._use_defaults()
    
    def _validate_settings(self):
        required_keys = ["GLOBAL_CC_BANK", "PAGE_1_BANKS", "PAGE_2_BANKS", "PAGE_3_BANKS", "PAGE_4_BANKS"]
        for key in required_keys:
            if key not in self.settings: return False
        if not self._validate_cc_list(self.settings["GLOBAL_CC_BANK"], 4): return False
        for page_key in ["PAGE_1_BANKS", "PAGE_2_BANKS", "PAGE_3_BANKS", "PAGE_4_BANKS"]:
            if not self._validate_page_banks(self.settings[page_key]): return False
        gsc = self.settings.get("GLOBAL_SLIDER_CHANNELS")
        if gsc is not None and not self._validate_slider_channels(gsc): return False
        for page_num in range(1, 5):
            key = f"PAGE_{page_num}_BANK_SLIDER_CHANNELS"
            bsc = self.settings.get(key)
            if bsc is not None and not self._validate_bank_slider_channels(bsc): return False
        return True
    
    def _validate_cc_list(self, cc_list, expected_length):
        if not isinstance(cc_list, list) or len(cc_list) != expected_length: return False
        for cc in cc_list:
            if not isinstance(cc, int) or cc < 0 or cc > 127: return False
        return True
    
    def _validate_page_banks(self, banks):
        if not isinstance(banks, list) or len(banks) != 4: return False
        for bank in banks:
            if not self._validate_cc_list(bank, 4): return False
        return True

    def _validate_slider_channels(self, slider_channels):
        if not isinstance(slider_channels, list) or len(slider_channels) != 4: return False
        for val in slider_channels:
            if not self._is_empty_or_null(val) and not self._is_valid_channel_value(val): return False
        return True

    def _validate_bank_slider_channels(self, bank_slider_channels):
        if not isinstance(bank_slider_channels, list) or len(bank_slider_channels) != 4: return False
        for bank_row in bank_slider_channels:
            if not self._validate_slider_channels(bank_row): return False
        return True
    
    def _use_defaults(self):
        self.settings = {
            "GLOBAL_CHANNEL": self.DEFAULT_GLOBAL_CHANNEL,
            "GLOBAL_MESSAGE_TYPE": self.DEFAULT_GLOBAL_MESSAGE_TYPE,
            "GLOBAL_CC_BANK": list(self.DEFAULT_GLOBAL_CC_BANK),
            "GLOBAL_SLIDER_CHANNELS": list(self.DEFAULT_GLOBAL_SLIDER_CHANNELS),
            "PAGE_1_BANKS": [list(b) for b in self.DEFAULT_PAGE_1_BANKS],
            "PAGE_2_BANKS": [list(b) for b in self.DEFAULT_PAGE_2_BANKS],
            "PAGE_3_BANKS": [list(b) for b in self.DEFAULT_PAGE_3_BANKS],
            "PAGE_4_BANKS": [list(b) for b in self.DEFAULT_PAGE_4_BANKS],
            "PAGE_1_BUTTONS": [list(b) for b in self.DEFAULT_PAGE_BUTTONS],
            "PAGE_2_BUTTONS": [list(b) for b in self.DEFAULT_PAGE_BUTTONS],
            "PAGE_3_BUTTONS": [list(b) for b in self.DEFAULT_PAGE_BUTTONS],
            "PAGE_4_BUTTONS": [list(b) for b in self.DEFAULT_PAGE_BUTTONS],
            "PAGE_1_BUTTON_CHANNELS": [list(r) for r in self.DEFAULT_BUTTON_CHANNELS],
            "PAGE_2_BUTTON_CHANNELS": [list(r) for r in self.DEFAULT_BUTTON_CHANNELS],
            "PAGE_3_BUTTON_CHANNELS": [list(r) for r in self.DEFAULT_BUTTON_CHANNELS],
            "PAGE_4_BUTTON_CHANNELS": [list(r) for r in self.DEFAULT_BUTTON_CHANNELS],
            "PAGE_1_BUTTON_TYPES": [list(r) for r in self.DEFAULT_BUTTON_TYPES],
            "PAGE_2_BUTTON_TYPES": [list(r) for r in self.DEFAULT_BUTTON_TYPES],
            "PAGE_3_BUTTON_TYPES": [list(r) for r in self.DEFAULT_BUTTON_TYPES],
            "PAGE_4_BUTTON_TYPES": [list(r) for r in self.DEFAULT_BUTTON_TYPES],
            "PAGE_1_CHANNEL": None,
            "PAGE_2_CHANNEL": None,
            "PAGE_3_CHANNEL": None,
            "PAGE_4_CHANNEL": None,
            "PAGE_1_BANK_CHANNELS": None,
            "PAGE_2_BANK_CHANNELS": None,
            "PAGE_3_BANK_CHANNELS": None,
            "PAGE_4_BANK_CHANNELS": None,
            "PAGE_1_BANK_SLIDER_CHANNELS": [list(r) for r in self.DEFAULT_BANK_SLIDER_CHANNELS],
            "PAGE_2_BANK_SLIDER_CHANNELS": [list(r) for r in self.DEFAULT_BANK_SLIDER_CHANNELS],
            "PAGE_3_BANK_SLIDER_CHANNELS": [list(r) for r in self.DEFAULT_BANK_SLIDER_CHANNELS],
            "PAGE_4_BANK_SLIDER_CHANNELS": [list(r) for r in self.DEFAULT_BANK_SLIDER_CHANNELS],
            "PAGE_1_TYPE": None,
            "PAGE_2_TYPE": None,
            "PAGE_3_TYPE": None,
            "PAGE_4_TYPE": None,
            "PAGE_1_BANK_TYPES": None,
            "PAGE_2_BANK_TYPES": None,
            "PAGE_3_BANK_TYPES": None,
            "PAGE_4_BANK_TYPES": None,
            "LOOP_TYPE": self.DEFAULT_LOOP_TYPE,
            "CC_RESOLUTION": self.DEFAULT_CC_RESOLUTION,
            "TRIM_SILENCE": self.DEFAULT_TRIM_SILENCE,
            "CC_RESET": self.DEFAULT_CC_RESET,
        }
    
    def _is_empty_or_null(self, val):
        return val is None or val == "" or val == "null"
    
    def _save_settings(self):
        try:
            with open(self.settings_path, 'w') as f:
                json.dump(self.settings, f)
            return True
        except OSError as e:
            print(f"Error saving settings: {str(e)}")
            return False

    def save(self):
        return self._save_settings()

    def get_global_cc_bank(self):
        return self.settings["GLOBAL_CC_BANK"]
    
    def get_all_pages(self):
        return [self.settings["PAGE_1_BANKS"], self.settings["PAGE_2_BANKS"], self.settings["PAGE_3_BANKS"], self.settings["PAGE_4_BANKS"]]
    
    def _is_valid_single_channel(self, val):
        if isinstance(val, int): return 1 <= val <= 16
        if isinstance(val, str) and val.isdigit(): return 1 <= int(val) <= 16
        return False
    
    def _is_valid_channel_value(self, val):
        if self._is_empty_or_null(val): return True
        if val in ("GLOBAL", "PAGE"): return True
        if self._is_valid_single_channel(val): return True
        if isinstance(val, str) and "|" in val:
            parts = val.split("|")
            return all(self._is_valid_single_channel(p.strip()) for p in parts)
        return False
    
    def _parse_channels(self, val):
        if isinstance(val, int) and 1 <= val <= 16: return [val - 1]
        if isinstance(val, str):
            if val.isdigit() and 1 <= int(val) <= 16: return [int(val) - 1]
            if "|" in val:
                parts = val.split("|")
                channels = []
                for p in parts:
                    p = p.strip()
                    if p.isdigit() and 1 <= int(p) <= 16: channels.append(int(p) - 1)
                    else: return None
                if not channels: return None
                return sorted(set(channels))
        return None
    
    def _get_page_channels(self, page_idx):
        page_num = page_idx + 1
        page_channel_key = f"PAGE_{page_num}_CHANNEL"
        page_ch = self.settings.get(page_channel_key)
        if self._is_empty_or_null(page_ch) or page_ch in ("GLOBAL", "PAGE"): return self.get_global_channels()
        parsed = self._parse_channels(page_ch)
        if parsed is not None: return parsed
        return self.get_global_channels()
    
    def get_global_channels(self):
        ch = self.settings.get("GLOBAL_CHANNEL", self.DEFAULT_GLOBAL_CHANNEL)
        parsed = self._parse_channels(ch)
        if parsed is not None: return parsed
        return [0] 
    
    def get_resolved_channels(self, page_idx, bank_idx):
        page_num = page_idx + 1
        bank_channels_key = f"PAGE_{page_num}_BANK_CHANNELS"
        bank_channels = self.settings.get(bank_channels_key)
        if isinstance(bank_channels, list) and len(bank_channels) > bank_idx:
            bank_ch = bank_channels[bank_idx]
            if self._is_empty_or_null(bank_ch) or bank_ch == "PAGE": return self._get_page_channels(page_idx)
            if bank_ch == "GLOBAL": return self.get_global_channels()
            parsed = self._parse_channels(bank_ch)
            if parsed is not None: return parsed
        return self._get_page_channels(page_idx)
    
    def _is_valid_message_type(self, val):
        if self._is_empty_or_null(val): return True
        return val in self.VALID_MESSAGE_TYPES
    
    def get_global_message_type(self):
        msg_type = self.settings.get("GLOBAL_MESSAGE_TYPE", self.DEFAULT_GLOBAL_MESSAGE_TYPE)
        if msg_type in self.VALID_MESSAGE_TYPES: return msg_type
        return "CC"
    
    def _get_page_message_type(self, page_idx):
        page_num = page_idx + 1
        page_type_key = f"PAGE_{page_num}_TYPE"
        page_type = self.settings.get(page_type_key)
        if self._is_empty_or_null(page_type): return self.get_global_message_type()
        if page_type in self.VALID_MESSAGE_TYPES: return page_type
        return self.get_global_message_type()
    
    def get_resolved_message_type(self, page_idx, bank_idx):
        page_num = page_idx + 1
        bank_types_key = f"PAGE_{page_num}_BANK_TYPES"
        bank_types = self.settings.get(bank_types_key)
        if isinstance(bank_types, list) and len(bank_types) > bank_idx:
            bank_type = bank_types[bank_idx]
            if self._is_empty_or_null(bank_type): return self._get_page_message_type(page_idx)
            if bank_type in self.VALID_MESSAGE_TYPES: return bank_type
        return self._get_page_message_type(page_idx)

    def get_resolved_global_slider_channels(self, slider_idx):
        gsc = self.settings.get("GLOBAL_SLIDER_CHANNELS")
        if isinstance(gsc, list) and len(gsc) > slider_idx:
            val = gsc[slider_idx]
            if not self._is_empty_or_null(val):
                parsed = self._parse_channels(val)
                if parsed is not None: return parsed
        return self.get_global_channels()

    def get_resolved_slider_channels(self, page_idx, bank_idx, slider_idx):
        page_num = page_idx + 1
        key = f"PAGE_{page_num}_BANK_SLIDER_CHANNELS"
        bsc = self.settings.get(key)
        if isinstance(bsc, list) and len(bsc) > bank_idx:
            bank_row = bsc[bank_idx]
            if isinstance(bank_row, list) and len(bank_row) > slider_idx:
                val = bank_row[slider_idx]
                if not self._is_empty_or_null(val):
                    parsed = self._parse_channels(val)
                    if parsed is not None: return parsed
        return self.get_resolved_channels(page_idx, bank_idx)

    def get_loop_type(self):
        val = self.settings.get("LOOP_TYPE", self.DEFAULT_LOOP_TYPE)
        if val in self.VALID_LOOP_TYPES: return val
        return self.DEFAULT_LOOP_TYPE

    def get_cc_resolution(self):
        val = self.settings.get("CC_RESOLUTION", self.DEFAULT_CC_RESOLUTION)
        if isinstance(val, str) and val.isdigit(): val = int(val)
        if isinstance(val, bool) or not isinstance(val, int): return self.DEFAULT_CC_RESOLUTION
        if 0 <= val <= 127: return val
        return self.DEFAULT_CC_RESOLUTION

    def get_trim_silence(self):
        val = self.settings.get("TRIM_SILENCE", self.DEFAULT_TRIM_SILENCE)
        if isinstance(val, bool): return val
        return self.DEFAULT_TRIM_SILENCE

    def get_cc_reset(self):
        val = self.settings.get("CC_RESET", self.DEFAULT_CC_RESET)
        if isinstance(val, bool): return val
        return self.DEFAULT_CC_RESET

    def _validate_mapping_args(self, cc_number, channel):
        if not isinstance(cc_number, int) or not (0 <= cc_number <= 127): return False
        if not isinstance(channel, int) or not (1 <= channel <= 16): return False
        return True

    def set_global_slider_mapping(self, slider_idx, cc_number, channel, persist=True):
        if not self._validate_mapping_args(cc_number, channel): return False
        self.settings["GLOBAL_CC_BANK"][slider_idx] = cc_number
        gsc = self.settings.get("GLOBAL_SLIDER_CHANNELS")
        if not isinstance(gsc, list) or len(gsc) != 4:
            gsc = list(self.DEFAULT_GLOBAL_SLIDER_CHANNELS)
            self.settings["GLOBAL_SLIDER_CHANNELS"] = gsc
        gsc[slider_idx] = channel
        if persist: return self.save()
        return True

    def set_bank_slider_mapping(self, page_idx, bank_idx, slider_idx, cc_number, channel, persist=True):
        if not self._validate_mapping_args(cc_number, channel): return False
        page_num = page_idx + 1
        self.settings[f"PAGE_{page_num}_BANKS"][bank_idx][slider_idx] = cc_number
        key = f"PAGE_{page_num}_BANK_SLIDER_CHANNELS"
        bsc = self.settings.get(key)
        if not isinstance(bsc, list) or len(bsc) != 4:
            bsc = [list(r) for r in self.DEFAULT_BANK_SLIDER_CHANNELS]
            self.settings[key] = bsc
        bank_row = bsc[bank_idx]
        if not isinstance(bank_row, list) or len(bank_row) != 4:
            bank_row = ["", "", "", ""]
            bsc[bank_idx] = bank_row
        bank_row[slider_idx] = channel
        if persist: return self.save()
        return True

    def get_resolved_button_cc(self, page_idx, bank_idx, button_idx):
        """強化防呆：自動過濾空字串並轉型，確保不會丟出 TypeError"""
        page_num = page_idx + 1
        key = f"PAGE_{page_num}_BUTTONS"
        buttons = self.settings.get(key)
        if isinstance(buttons, list) and len(buttons) > bank_idx:
            bank_row = buttons[bank_idx]
            if isinstance(bank_row, list) and len(bank_row) > button_idx:
                val = bank_row[button_idx]
                if isinstance(val, int):
                    return val
                if isinstance(val, str) and val.isdigit():
                    return int(val)
        return page_idx * 16 + bank_idx * 4 + button_idx + 8
        
    def get_resolved_button_type(self, page_idx, bank_idx, button_idx):
        """取得指定按鈕的觸發型態 (CC 或 Note)"""
        page_num = page_idx + 1
        key = f"PAGE_{page_num}_BUTTON_TYPES"
        b_type_data = self.settings.get(key)
        if isinstance(b_type_data, list) and len(b_type_data) > bank_idx:
            bank_row = b_type_data[bank_idx]
            if isinstance(bank_row, list) and len(bank_row) > button_idx:
                val = bank_row[button_idx]
                if val in ("CC", "Note"):
                    return val
        return "CC"

    def get_resolved_button_channels(self, page_idx, bank_idx, button_idx):
        page_num = page_idx + 1
        key = f"PAGE_{page_num}_BUTTON_CHANNELS"
        b_ch_data = self.settings.get(key)
        if isinstance(b_ch_data, list) and len(b_ch_data) > bank_idx:
            bank_row = b_ch_data[bank_idx]
            if isinstance(bank_row, list) and len(bank_row) > button_idx:
                val = bank_row[button_idx]
                if not self._is_empty_or_null(val):
                    parsed = self._parse_channels(val)
                    if parsed is not None: return parsed
        return self._get_page_channels(page_idx)

settings = Settings()