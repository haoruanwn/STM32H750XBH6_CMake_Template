# pyocd_user.py

from pyocd.core.memory_map import FlashRegion
import logging

# --- 定义外部 QSPI Flash 的参数 ---
FLM_FILE = ".config/FK750M5_XBH6_V0.FLM"
QSPI_FLASH_START = 0x90000000
# QSPI_FLASH_SIZE = 32 * 1024 * 1024
QSPI_FLASH_SIZE = 8 * 1024 * 1024
QSPI_FLASH_BLOCKSIZE = 0x1000
""" 
下载算法说明：
FK750M5_XBH6_V0.FLM 用于8MB QSPI Flash 的下载算法。
FK750M6_XBH6_V0.FLM 用于32MB QSPI Flash 的下载算法。

"""

def will_connect(board):
    """
    这是一个 pyOCD 代理函数，会在连接前被自动调用。
   
    """
    target = board.target
    
    # 定义外部 Flash 区域
    external_flash = FlashRegion(
        name="qspi_flash",
        start=QSPI_FLASH_START,
        length=QSPI_FLASH_SIZE,
        blocksize=QSPI_FLASH_BLOCKSIZE,
        is_boot_memory=False,
        flm=FLM_FILE
    )
    
    # 将其添加到内存地图
    target.memory_map.add_region(external_flash)
    
    logging.info(f"用户脚本：成功添加外部 QSPI Flash 区域 '{external_flash.name}'")