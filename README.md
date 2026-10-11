# EE3021 HW-Lab2: WiFi and Sensor Data

## Team Members

- r15922131 — 莊凱皓
- r15922162 — 王昱鈞

## Implemented

- Basic Problem
- Option Problem 1

## Overview

使用 STM32 IoT Node（B-L475E-IOT01A）讀取板上 LSM6DSL 的三軸加速度，透過 WiFi 以 TCP 傳送到電腦，並用 Python 即時繪圖。Option Problem 1 另外啟用 LSM6DSL 內建的 Significant Motion Detection，偵測到時透過 EXTI 中斷通知 STM32，STM32 再把事件傳到電腦顯示。

```text
LSM6DSL --I2C--> STM32 --WiFi (es-wifi) / TCP--> PC (Python) --> matplotlib
     INT1 --PD11 (EXTI)--> STM32 --"EVENT" message--> PC
```

## Files

| File | 說明 |
|---|---|
| `main.c` | STM32 主程式。連上 WiFi 後以 TCP client 連到電腦，持續讀取加速度並以 `x,y,z\n` 格式傳送；包含 Significant Motion 的初始化（`SigMotion_Init`）、PD11 外部中斷 callback，以及事件傳送 `EVENT,SIGNIFICANT_MOTION\n` |
| `main.h` | 加入 `stm32l475e_iot01_accelero.h`，讓主程式可使用 BSP 加速度計 API |
| `stm32l4xx_it.c` | 中斷服務函式，包含 LSM6DSL INT1（PD11）所使用的 EXTI 中斷處理 |
| `plot.py` | 電腦端 Python：TCP server（port 8002），接收資料並用 matplotlib 即時畫出 X/Y/Z；收到事件時顯示 `Significant Motion Detected!` 並在終端機印出時間 |
| `recv.py` | 簡易接收測試腳本，只把收到的資料逐行印在終端機，用來驗證 WiFi/TCP 是否正常 |
| `.gitignore` | 忽略編譯產物與 IDE 設定檔 |

## Data Format

```text
一般資料:  <x>,<y>,<z>\n            例: 8,-25,1016
事件:      EVENT,SIGNIFICANT_MOTION\n
```

加速度單位為 mg（靜止平放時 Z 約 1000 mg）。

## How to Run

1. 取得 STM32CubeL4 韌體包，匯入 `Projects/B-L475E-IOT01A/Applications/WiFi/WiFi_Client_Server` 專案。
2. 將本倉庫的 `main.c`、`main.h`、`stm32l4xx_it.c` 覆蓋到專案對應位置，並在專案中加入 LSM6DSL 與 BSP 加速度計驅動（Include 路徑與檔案連結）。
3. 修改 `main.c` 的 `SSID`、`PASSWORD`、`RemoteIP`（電腦在同一個 WiFi 下的 IP）、`RemotePORT`。板子的 WiFi 模組僅支援 2.4 GHz。
4. 電腦安裝 matplotlib 後執行：

   ```
   python plot.py
   ```

   看到 `waiting` 後，燒錄並重置板子。
5. 圖上會出現 X/Y/Z 即時曲線；連續有節奏地晃動板子數秒，會觸發 Significant Motion 並在圖上與終端機顯示事件。

## Notes

- 本倉庫中的 `SSID`、`PASSWORD`、`RemoteIP` 皆為示意值，請改成自己的網路設定。
- 板子為 TCP client，電腦為 TCP server；請先啟動 `plot.py` 再重置板子。
