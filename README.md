# gesture-control
Приложение, в основе которого механика управления жестами

# Запуск

 - ``pip install -r requirements.txt``
 - Создать конфиг
 - ``python main.py``

# config
Для запуска необходим файл config.json

Пример:

```
{
    "okay": "XUSB_GAMEPAD_A",
    "close": "XUSB_GAMEPAD_B"
}
```

Доступные ключи:
 - open 
 - close
 - finger 
 - okay
   
Доступные значения:

 - XUSB_GAMEPAD_DPAD_UP
 - XUSB_GAMEPAD_DPAD_DOWN
 - XUSB_GAMEPAD_DPAD_LEFT
 - XUSB_GAMEPAD_DPAD_RIGHT
 - XUSB_GAMEPAD_START
 - XUSB_GAMEPAD_BACK
 - XUSB_GAMEPAD_LEFT_THUMB
 - XUSB_GAMEPAD_RIGHT_THUMB
 - XUSB_GAMEPAD_LEFT_SHOULDER
 - XUSB_GAMEPAD_RIGHT_SHOULDER
 - XUSB_GAMEPAD_GUIDE
 - XUSB_GAMEPAD_A
 - XUSB_GAMEPAD_B
 - XUSB_GAMEPAD_X
 - XUSB_GAMEPAD_Y
