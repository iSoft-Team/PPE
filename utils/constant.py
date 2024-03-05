from pydantic import BaseSettings
import os
from utils.project_config import project_config as cf

def generate_style(path):
    return f"background-image: url('{path}'); background-position: center; color: white; border: none"

def icon_path(name):
    return os.path.join(cf.ROOT_UI_PATH, name)

class Constant(BaseSettings):
    SIMULATE_PATH: str = generate_style(icon_path("detect-on.png"))
    BUTTON_DONE_PATH: str = generate_style(icon_path("Button highligt done.png"))
    BUTTON_PATH: str = generate_style(icon_path("Button highligt detect.png"))
    ENZIN_LABEL_ENZIM_PATH: str = generate_style(icon_path("enzim-on.png"))
    ENZIN_LABEL_NO_ENZIM_PATH: str = generate_style(icon_path("enzim-off.png"))
    DISABLE_SIMULATE_PATH: str = generate_style(icon_path("detect-off.png"))
    DISABLE_BUTTON_PATH: str = generate_style(icon_path("Disable Detect Button highligt.png"))
    BACKGROUND_PATH: str = generate_style(icon_path("Mask group landscape.png"))
    PASS_PATH: str = generate_style(icon_path("button-pass.png"))
    FAIL_PATH: str = generate_style(icon_path("button-fail.png"))
    INFO_PATH: str = generate_style(icon_path("About.png"))
    CLOSE_PATH: str = generate_style(icon_path("close-form.png"))
    INFO_BACKGROUND_PATH: str = icon_path("info_landscape.png")
    LOADING_BACKGROUND_PATH: str = generate_style(icon_path("ai_background_1920.png"))
    DOOR_CLOSE_PATH: str = generate_style(icon_path("door-close.png"))
    DOOR_OPEN_PATH: str = generate_style(icon_path("door-open.png"))
    MACHINE_ON_PATH: str = generate_style(icon_path("machine-on.png"))
    MACHINE_OFF_PATH: str = generate_style(icon_path("machine-off.png"))
    INTERLOCK_ON_PATH: str = generate_style(icon_path("interlock_on.png"))
    INTERLOCK_OFF_PATH: str = generate_style(icon_path("interlock_off.png"))
    SYSTEM_READY_PATH: str = generate_style(icon_path("ready.png"))
    SYSTEM_NOT_READY_PATH: str = generate_style(icon_path("not_ready.png"))
    BUZER_ON_PATH: str = generate_style(icon_path("buzer_on.png"))
    BUZER_OFF_PATH: str = generate_style(icon_path("buzer_off.png"))
    BUTTON_BG_PATH: str = generate_style(icon_path("Rectangle 208.png"))
    COLLECT_DATA: str = generate_style(icon_path("collect_data.png"))
    DETECT_PATH: str = generate_style(icon_path("detect-program.png"))
    CAMERA_DISCONNECT_PATH: str = icon_path("camera_disconnected.jpg")
    SETTING_PATH: str = generate_style(icon_path("button-setting.png"))
    SPARE1_ON_PATH: str = generate_style(icon_path("spare1_on.png"))
    SPARE2_ON_PATH: str = generate_style(icon_path("spare2_on.png"))
    SPARE3_ON_PATH: str = generate_style(icon_path("spare3_on.png"))
    SPARE4_ON_PATH: str = generate_style(icon_path("spare4_on.png"))
    SPARE5_ON_PATH: str = generate_style(icon_path("spare5_on.png"))
    SPARE1_OFF_PATH: str = generate_style(icon_path("spare1_off.png"))
    SPARE2_OFF_PATH: str = generate_style(icon_path("spare2_off.png"))
    SPARE3_OFF_PATH: str = generate_style(icon_path("spare3_off.png"))
    SPARE4_OFF_PATH: str = generate_style(icon_path("spare4_off.png"))
    SPARE5_OFF_PATH: str = generate_style(icon_path("spare5_off.png"))




constant = Constant()
    