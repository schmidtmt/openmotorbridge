#pragma once

#include <stdint.h>

// =============================================================================
// Qorvo DW3110 Ultra-Wideband Transceiver Register Definitions & Bitfields
// IEEE 802.15.4z UWB (Channel 5 @ 6489.6 MHz, BPRF Mode, 6.8 Mbps)
// =============================================================================

// Device Identifier (Expected value for DW3110 series: 0xDECA03xx)
#define DW3110_REG_DEV_ID           0x0000
#define DW3110_DEV_ID_DECA          0xDECA
#define DW3110_DEV_ID_DW3110        0x0302

// Extended Unique Identifier (EUI-64)
#define DW3110_REG_EUI_64_LO        0x0004
#define DW3110_REG_EUI_64_HI        0x0008

// PAN Identifier & Short Address
#define DW3110_REG_PANADR           0x000C

// System Configuration Register
#define DW3110_REG_SYS_CFG          0x0010
#define DW3110_SYS_CFG_FFEN         (1UL << 0)   // Frame Filtering Enable
#define DW3110_SYS_CFG_FFBC         (1UL << 1)   // Allow Broadcast Frames
#define DW3110_SYS_CFG_DIS_FCE      (1UL << 5)   // Disable Frame Check Error reporting
#define DW3110_SYS_CFG_DIS_DRX      (1UL << 6)   // Disable Double Buffer RX
#define DW3110_SYS_CFG_PHR_6M8      (1UL << 8)   // 6.8 Mbps PHR Rate
#define DW3110_SYS_CFG_CIA_ENA      (1UL << 10)  // Channel Impulse Response Accumulator Enable
#define DW3110_SYS_CFG_FAST_AACK    (1UL << 15)  // Fast Auto-Acknowledge

// System Control Register
#define DW3110_REG_SYS_CTRL         0x0014
#define DW3110_SYS_CTRL_SFCST       (1UL << 0)   // Suppress Auto-FCS Transmission
#define DW3110_SYS_CTRL_TXSTRT      (1UL << 1)   // Start Transmission
#define DW3110_SYS_CTRL_TXDLYS      (1UL << 2)   // Transmitter Delayed Send
#define DW3110_SYS_CTRL_TRXOFF      (1UL << 6)   // Transceiver Off (Abort current TX/RX)
#define DW3110_SYS_CTRL_WAIT4RESP   (1UL << 7)   // Wait for Response after TX
#define DW3110_SYS_CTRL_RXENAB      (1UL << 8)   // Enable Receiver immediately
#define DW3110_SYS_CTRL_RXDLYE      (1UL << 9)   // Receiver Delayed Enable

// System Event Status Register (Lower 32-bit & Upper 32-bit)
#define DW3110_REG_SYS_STATUS_LO    0x0018
#define DW3110_SYS_STATUS_CPLOCK    (1UL << 1)   // Clock Phase Lock
#define DW3110_SYS_STATUS_AAT       (1UL << 3)   // Auto-Ack Triggered
#define DW3110_SYS_STATUS_TXFRB     (1UL << 4)   // TX Frame Begins
#define DW3110_SYS_STATUS_TXPRS     (1UL << 5)   // TX Preamble Sent
#define DW3110_SYS_STATUS_TXPHS     (1UL << 6)   // TX PHY Header Sent
#define DW3110_SYS_STATUS_TXFRS     (1UL << 7)   // TX Frame Sent (Success)
#define DW3110_SYS_STATUS_RXPRD     (1UL << 8)   // RX Preamble Detected
#define DW3110_SYS_STATUS_RXSFDD    (1UL << 9)   // RX SFD Detected
#define DW3110_SYS_STATUS_RXPHD     (1UL << 10)  // RX PHY Header Detected
#define DW3110_SYS_STATUS_RXFR      (1UL << 11)  // RX Frame Ready
#define DW3110_SYS_STATUS_RXFCG     (1UL << 12)  // RX Frame Check Good (CRC OK)
#define DW3110_SYS_STATUS_RXFCE     (1UL << 13)  // RX Frame Check Error
#define DW3110_SYS_STATUS_RXRFTO    (1UL << 17)  // RX Frame Wait Timeout
#define DW3110_SYS_STATUS_RXPTO     (1UL << 18)  // RX Preamble Timeout
#define DW3110_SYS_STATUS_RXOVRR    (1UL << 20)  // RX Overrun

// RX Frame Information Register
#define DW3110_REG_RX_FINFO         0x001C
#define DW3110_RX_FINFO_LEN_MASK    0x03FF       // Received frame byte count (0..1023)
#define DW3110_RX_FINFO_RNG_BIT     (1UL << 15)  // Ranging packet flag

// RX & TX Data Buffer Registers
#define DW3110_REG_RX_BUFFER        0x0020
#define DW3110_REG_TX_BUFFER        0x0024

// TX Frame Control Register
#define DW3110_REG_TX_FCTRL         0x0028
#define DW3110_TX_FCTRL_TXBR_6M8    (1UL << 13)  // 6.81 Mbps
#define DW3110_TX_FCTRL_TR_64       (0UL << 16)  // 64 MHz PRF
#define DW3110_TX_FCTRL_TXPSR_64    (0x01UL << 18) // 64 Symbol Preamble (Lowest deterministic latency)

// System Time & Timestamp Registers (for Time-of-Flight / Ranging)
#define DW3110_REG_SYS_TIME         0x0030
#define DW3110_REG_TX_TIME          0x0034
#define DW3110_REG_RX_TIME          0x0038

// RF Channel & Analog Tuning Registers
#define DW3110_REG_CHAN_CTRL        0x0040
#define DW3110_CHAN_5_FREQ_MHZ      6489.6f
#define DW3110_CHAN_5_SELECT        0x05

// Interrupt Enable / Mask Registers
#define DW3110_REG_SYS_ENABLE_LO    0x0044
#define DW3110_SYS_ENABLE_TXFRS     (1UL << 7)
#define DW3110_SYS_ENABLE_RXFCG     (1UL << 12)
#define DW3110_SYS_ENABLE_RXFCE     (1UL << 13)
#define DW3110_SYS_ENABLE_RXRFTO    (1UL << 17)

// Speed of light in air for Time-of-Flight ranging (mm / picosecond)
#define SPEED_OF_LIGHT_MM_PER_PS    0.000299792458f
#define DW3110_TIME_UNITS_PS        15.65f // 1 DW3110 timestamp unit = ~15.65 picoseconds
