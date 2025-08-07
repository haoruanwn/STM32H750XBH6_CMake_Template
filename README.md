# STM32H750XBH6\_CMake\_Template

## 说明

提供一个基于 CMake 构建的模块化的 STM32H750XBH6 工程模板，程序可通过pyOCD烧录并运行在开发板的外部 QSPI FLASH 中。

#### 已实现的功能

  * `pyocd` 调用 FLM 格式的外部下载算法，将程序烧录到外部 Flash 中。
  * USB 虚拟串口功能。
  * 基于命令行、VSCode、CLion 的编译和烧录方式。
  * 在 VSCode、CLion 中通过 `pyocd` 调试运行在外部 Flash 中的程序。
 

#### 前置条件

安装如下软件，并且做到可用命令行验证版本

```bash
~ 
❯ cmake --version
cmake version 3.31.6

CMake suite maintained and supported by Kitware (kitware.com/cmake).

~ 
❯ pyocd --version
0.38.0

~ 
❯ ninja --version
1.12.1

~ 
❯ arm-none-eabi-gcc --version
arm-none-eabi-gcc (Fedora 15.1.0-1.fc42) 15.1.0
Copyright (C) 2025 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

> 其中ninja和cmake可由clion提供，如果仅仅使用clion，不必添加进环境变量

### 软件版本

| 工具 | 版本 | 说明 |
| :--- | :--- | :--- |
| STM32CubeMX | 6.15 | 6.15 版本添加了对 GCC 和 ST Clang 编译器的支持，并提供了 CMake 预设脚本。 |

## 引用与致谢

  * **[反客科技](https://shop212360197.taobao.com/?spm=a21n57.shop_search.0.0.89ca4720CYzGRh)**：提供开发板资料和使用的 FLM 格式的外部下载算法。
      * 交流群：536665479、994246105
  * **[Peakors/STM32H750XBH6\_Template](https://github.com/Peakors/STM32H750XBH6_Template)**：提供 CubeMX 的 ioc 工程模板、USB 虚拟串口的实现、`printf` 和 `scanf` 重定向到串口1。本项目是在此基础上发展而来的。

## 使用说明

### 通过 CMake 子模块的方式添加用户文件

此方法便于模块化管理用户代码。例如，需要添加 `Drivers/User` 目录下的驱动文件。

`Drivers/User` 目录结构如下：

```bash
.
├── CMakeLists.txt
├── Inc
│   └── user_driver.h
└── Src
    └── user_driver.c
```

`Drivers/User/CMakeLists.txt` 文件内容如下：

```cmake
# 查找目录下的所有源文件
file(GLOB SOURCES "Src/*.c")

# 添加一个静态库
add_library(user_driver STATIC ${SOURCES})

# 指定头文件目录
target_include_directories(user_driver
    PUBLIC
    "${CMAKE_CURRENT_SOURCE_DIR}/Inc"
)

# 链接 STM32CubeMX 生成的目标
target_link_libraries(user_driver
    PRIVATE
    stm32cubemx
)
```

在顶层 `CMakeLists.txt` 中添加此模块：

```cmake
# ... (其他配置)

# Add STM32CubeMX generated sources
add_subdirectory(cmake/stm32cubemx)

# 添加 Driver/User 模块
add_subdirectory(Drivers/User)

# ... (其他配置)

# Add linked libraries
target_link_libraries(${CMAKE_PROJECT_NAME}
    stm32cubemx

    # Add user defined libraries
    user_driver
)
```

### 使用命令行编译

```bash
# 调用预设的配置 (例如 Debug)
cmake --preset Debug

# 使用预设进行构建
cmake --build --preset Debug
```

### 使用 pyocd 烧录

不同容量的QSPI FLASH使用的配置不同，具体参考`pyocd_user.py`

```bash
pyocd flash --target stm32h750xx -O connect_mode=under-reset ./build/Debug/STM32H750XBH6_Template.bin@0x90000000
```

> **原理参考**: [使用pyocd调用FLM格式的外部下载算法](https://haoruanwn.github.io/2025/08/03/%E4%BD%BF%E7%94%A8pyocd%E8%B0%83%E7%94%A8FLM%E6%A0%BC%E5%BC%8F%E7%9A%84%E5%A4%96%E9%83%A8%E4%B8%8B%E8%BD%BD%E7%AE%97%E6%B3%95/)

### 使用 VSCode 开发和调试

参考文件[使用 VSCode 开发和调试](./docs/使用VSCode开发和调试.md)

### 使用 CLion 开发和调试

参考文件[使用 Clion 开发和调试](./docs/使用Clion开发和调试.md)

## 适用开发板

本模板要求开发板 QSPI Flash 的引脚配置与反客科技的开发板一致。

| 开发板 | 淘宝链接 |
| :--- | :--- |
| 核心板1 | [Taobao Link](https://item.taobao.com/item.htm?id=677786502974&pisk=gxyZ4GZVzQpBzeutsJM2zn1hWrDtQx7SI-gjmoqmfV0i5-a4mmoqmdmmnvXnq29fXA1x3ruUkVGsIV9q3ozYlj2jl--TLzJXCNCTmKkjna_5FTZTfxHcPK228TttcmimmEgm-DDj05553IrTXxHDAEf7tlKVgX82mm0cYvmqDcDDnqXhYmiSox0iieAnm2Dmnjc0xvmsDCximqjet0mJSEmmjkcnf0pmnx4mKv0KmxmgoxmL_xDJP0cGxxThkBf1vf0uj2JDU3nZsLq9GKJV1cGirfgWnWwEbfuuj8PbdXnzaJl7sGfi4xuLXJGNWFMYA7z4irCW9Ar0szh89iAKv54ULbev-ZGTmWzEbP_ykqwTf-u_b1bTYv0amjzVuIoaNPzxSlYdvvZ0xA3TATS8uuaa3ba1KdlIC0h7gP_pnVNzxyl7de9SHyF0omzhHemLQuNS_57wFqhc4XYxxu88H58DgfmKY4sFYKqFHVwF21oyMIh9vDu5XjAvMfmKY4sFYIdx6NnEPGhc.&spm=a21xtw.29978518.0.0&sku_properties=-1%3A-1) |
| 核心板2 | [Taobao Link](https://item.taobao.com/item.htm?id=838568127129&pisk=g4ZK2a0lBEDCdBqKIJ7MEatua6Xg9N2F6WyXqbcHP5FTFWGnZ4gI5fMxFv9BA8MS25NlLX25T7E-18zhL4feePFUh2V8U9kSN7N-ZybGmJyE401mwij0LAiF8dPpR3T1FxkvNO0CIWwtJ01ciiYMC25nV7DvpQs65xlsdYGIROps3vnSdHi5BfM-3UtQN76t5YHSdpGIdGTs3fOWA3MB5dMoEBMIPe6TCfkSVbNSROesvSYKaUlW2yH2dJ4FyT-y4lHKJbKo63h8Vn0EGpG223hZE2p3dfKWVlURYvGnwGOxalN-c0gvn6eEX8VxnWj6vSe4b5H_GgKoZkPLYDq1hFhuuxFnsSsXXcwgC7047_-m75E-ukgBFsGbHJajfuXW3VFsn-MUGsInSW4sorNlFEhzIrF-TVAM5Swgnkua2sdsayDqfx2FvhnbdyqExPCwWfZTFkumcgS4moCErIcxEe6OBU8rRA8lCjDz47D1zAhcIRYyzVbjBjXOBU8rRAktiOcHzUuGl&spm=a21xtw.29978518.0.0&sku_properties=-1%3A-1) |
| 核心板3 | [Taobao Link](https://item.taobao.com/item.htm?id=682521953131&pisk=g4jq2B6aT2n7biAvogtZTAauM1xv2hPBmGO6IOXMhIADGG1NIdJwImvMj3qkKQi_Hna9b1RP6ITXmIiwbO5O1Fj61GkA46oscSUAIc-6jWNQAk6AhhKgOcjZakGvKpvgfCmDEnp6YyNZ7k6AHhHqsJ_uAA86PMkmSCfMqUvMQhcMsq2yqpvpjmYim4AkwQxMIFxMquvMLx0Ms10oEdJeIK0DnQxkId-Ms1xgUTAJQhAivutMvX9Ho8xsZ53o6VYXttArjDkp3E2NpVitXxvDoBYXOcY54K82ttjF5gTJLwSyRZ20op-wwtIWuShXXT_F_NfTR4KVIZfpJaeiyLQcag8dXbV6kObPaK5bTfd1DtswGtz0MT-kgOYN_5uw3w1V6IXmw8K5ITxvMTZUp1WCgG8CGum2Pn9pRN5bwcAf8TfyRgGSAhCRS1vNZlhkeiWCRE74gDO9Sgyn6LXE9GQqsV8DeLRQU8oGUldf4JU2LV39kYpyO-LiWVLDeLRQU8utWEFvUBwvS&spm=a21xtw.29978518.0.0&sku_properties=-1%3A-1) |
| 金手指核心板 | [Taobao Link](https://item.taobao.com/item.htm?id=956806857353&pisk=g1oZ2qM2aaII7mNTSDZVatTH6jqTAoR7jmNbnxD0C5Vg1mGqn-y4nG20mkx3EWsXBlTY0jPEM5a_j5s40xlxGrmbGmWtYbSffCLtnirbmQOWV3MtCoEDNimVT31TF-jMcSVG-leb4UOVu3MtBoBNiLgHVtzbRqBGoSc0xy203of0iNvUxReYmG4cjwV39Wq0nrq0xH20UOb0ijxhx8ygiZj0I6V3F-E0ijqDLvVL3oVmv2q02_wuSpqftIQha6UUZAVFmgW8QPYr_ZslqZyTS74_Ni4IYRzaZAmrlDaLU4oUPVvMS8r49AnQ7CC_DvgrgqcvPwEZnVc8y2pcJJ3iTDz-D6AbWx0ETRl6asFjXAi41A8M6vr3_x4qgI74Q4GZM5DG9pEInvqT6vtyejkS_mzS1HjaRlw8Pql69iVszvcUPD1CVohKoj2qtnC3pckSPPuw_gNYogPhMJDPwm3NiZzgpJPWLpSmLnFsYLLaUZQYW9eUNdUckZUgpJPWLphttps://item.taobao.com/item.htm?id=956163066774&pisk=gIkqqziw86B7VBaYiYwN8GOkkV2YER8QnAa_jcmgcr40lAgZjlrajtqgI8vuxz66D-OTQVzrWrNbnr6aQcut55D_5ASxU2W1hEdxjOy_IeTBdpixcReMRODNzpsYfkjcINa0E72_bjRBQ1oxDReGVNAIZmIw_7k1ml4M48qaXo2GIPvk4lZVsR40safujz2gI5Viq8qbXsj0jPxyEkZQm140I_fuxkBgIR0gE3rTro2gIDh7IJQQxSxuCaYOZ1_aZym0zOXFvoPDWqC1d96LmS43GPWgNYr4gymmLfM7wklEUWGDmIqUQznxFS8AlRnSTVliWB183ccmJWhJj_E-i4kz9AQk5Snia4rqle7T5xnjQri2iEnzErog_V8N_olIuVUmmaK8FcmuHrnWLH3ZAqkaOq9l37wbvWGZlUBglXoozWM5P9wtyf0gb4vOruHqAXNqgEWQW5jrKNEoYwHtgNfaiuEzR3-PI0JTlY-pgk5O6SI84ytYs1CTiuEzR3-P61FvkuzBD5f..&spm=a21xtw.29978518.0.07AkPdTL79To&spm=a21xtw.29978518.0.0&skuId=6048697183505) |
| B2B核心板 | [Taobao Link](https://item.taobao.com/item.htm?id=955681215463&pisk=g7wn2-cynIxWrS7t6RMCOkIap9CTOvMSRzp-yY3P_Vu6pzHKefkZq0OrzXRe75qbr2I5OvFirPzi8pICObuuRVUJekeu1LqbVJIIeMMQAYMPkZBxEkZIFmzlICwn_Vo7bLJEY1Hwdh0yqZBAHk1EAYENk8h0p1nKDLkrTbuZQVieUHzrThWZ50iy80uFjG0s20urTBuwQDnvUYREYdRZA0mrYDuy_Vus4YuzzYSiQVirA3IEJyaYQa4WoXN-O_2ExX04Y2rLvRJqLBZiSOWgIWG-uZ3MULyixujYul9NUqPb75PUiHJtwAggCD45hpMEZSZ-qyXHLAFYRSlb1aAmuSEjLmECKdD4Y5eoX8IJZ2zQIlyIsnvmt7P0nvPh5CML-RkI8PBH7zULpz2KEOts8SNT8cq9https://item.taobao.com/item.htm?id=956163066774&pisk=gIkqqziw86B7VBaYiYwN8GOkkV2YER8QnAa_jcmgcr40lAgZjlrajtqgI8vuxz66D-OTQVzrWrNbnr6aQcut55D_5ASxU2W1hEdxjOy_IeTBdpixcReMRODNzpsYfkjcINa0E72_bjRBQ1oxDReGVNAIZmIw_7k1ml4M48qaXo2GIPvk4lZVsR40safujz2gI5Viq8qbXsj0jPxyEkZQm140I_fuxkBgIR0gE3rTro2gIDh7IJQQxSxuCaYOZ1_aZym0zOXFvoPDWqC1d96LmS43GPWgNYr4gymmLfM7wklEUWGDmIqUQznxFS8AlRnSTVliWB183ccmJWhJj_E-i4kz9AQk5Snia4rqle7T5xnjQri2iEnzErog_V8N_olIuVUmmaK8FcmuHrnWLH3ZAqkaOq9l37wbvWGZlUBglXoozWM5P9wtyf0gb4vOruHqAXNqgEWQW5jrKNEoYwHtgNfaiuEzR3-PI0JTlY-pgk5O6SI84ytYs1CTiuEzR3-P61FvkuzBD5f..&spm=a21xtw.29978518.0.0VCqsa5eIGJQwKxPbvvFzPsdsKuPUljN14Ci_TP2iG8Th4pOwg7-9FcS8QQOSTciik7pUbEUFWXXdjGAqNXosAOjGjQOSTciikGjMgrGEfD6G.&spm=a21xtw.29978518.0.0&skuId=6047678390178) |
| 邮票孔核心板 | [Taobao Link](https://item.taobao.com/item.htm?id=956163066774&pisk=gIkqqziw86B7VBaYiYwN8GOkkV2YER8QnAa_jcmgcr40lAgZjlrajtqgI8vuxz66D-OTQVzrWrNbnr6aQcut55D_5ASxU2W1hEdxjOy_IeTBdpixcReMRODNzpsYfkjcINa0E72_bjRBQ1oxDReGVNAIZmIw_7k1ml4M48qaXo2GIPvk4lZVsR40safujz2gI5Viq8qbXsj0jPxyEkZQm140I_fuxkBgIR0gE3rTro2gIDh7IJQQxSxuCaYOZ1_aZym0zOXFvoPDWqC1d96LmS43GPWgNYr4gymmLfM7wklEUWGDmIqUQznxFS8AlRnSTVliWB183ccmJWhJj_E-i4kz9AQk5Snia4rqle7T5xnjQri2iEnzErog_V8N_olIuVUmmaK8FcmuHrnWLH3ZAqkaOq9l37wbvWGZlUBglXoozWM5P9wtyf0gb4vOruHqAXNqgEWQW5jrKNEoYwHtgNfaiuEzR3-PI0JTlY-pgk5O6SI84ytYs1CTiuEzR3-P61FvkuzBD5f..&spm=a21xtw.29978518.0.0) |

## 拓展内容

等待补充

- [**开启浮点数打印支持**](./docs/拓展内容/开启浮点数打印支持.md)
- 使用c++开发（待更新）
