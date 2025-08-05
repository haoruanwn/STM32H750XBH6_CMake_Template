# 使用命令行编译
```bash
# 调用预设的配置
cmake --preset Debug

cmake --build --preset Debug

```

# 使用pyocd烧录
```bash
pyocd flash --target stm32h750xx -O connect_mode=under-reset ./build/Debug/STM32H750XBH6_Template.bin@0x90000000
```