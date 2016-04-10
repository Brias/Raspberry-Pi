#!/usr/bin/python
import smbus

# EEPROM-Adresse, Register
address = 0x50
reg = 0x01
# "Hello World\0"
data = [ 0x48, 0x6e, 0x6c, 0x6c, 0x6f, 0x20, 0x57, 0x6F, 0x72, 0x6C, 0x64, 0x00 ]

eeprom = smbus.SMBus(1)

print ("I2C: Schreiben auf Device 0x%02X" % address)
try:
  eeprom.write_i2c_block_data(address, reg, data)

except IOError, err:
  print ("Fehler beim Schreiben auf Device 0x%02X" % address)
  exit(-1)
