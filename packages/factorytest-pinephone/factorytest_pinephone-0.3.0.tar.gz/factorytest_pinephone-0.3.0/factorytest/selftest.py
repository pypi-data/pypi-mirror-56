import time
import smbus


def _read_i2c_word():
    pass


def mpu6050(bus=1, address=0):
    bus = smbus.SMBus(bus)

    # Set accel-config to self-test, 8g
    bus.write_byte_data(address, 0x1c, 0xf0)

    # Set gyro-config to self-test, 250deg/s
    bus.write_byte_data(address, 0x1b, 0xe0)

    # Wait for chip to run self-test
    time.sleep(0.25)

    # Read test results
    self_text_x = bus.read_byte_data(address, 0x0d)
    self_text_y = bus.read_byte_data(address, 0x0e)
    self_text_z = bus.read_byte_data(address, 0x0f)
    self_text_a = bus.read_byte_data(address, 0x10)

    result_accel_x = (self_text_x >> 3) | (self_text_a & 0x30) >> 4
    result_accel_y = (self_text_y >> 3) | (self_text_a & 0x0c) >> 2
    result_accel_z = (self_text_z >> 3) | (self_text_a & 0x03) >> 0

    result_gyro_x = self_text_x & 0x1f
    result_gyro_y = self_text_y & 0x1f
    result_gyro_z = self_text_z & 0x1f

    # Read the factory trim values
    trim_accel_x = (4096 * 0.34) * pow((0.92 / 0.34), (float(result_accel_x) - 1.0 / 30.0))
    trim_accel_y = (4096 * 0.34) * pow((0.92 / 0.34), (float(result_accel_y) - 1.0 / 30.0))
    trim_accel_z = (4096 * 0.34) * pow((0.92 / 0.34), (float(result_accel_z) - 1.0 / 30.0))
    trim_gyro_x = (25.0 * 131.0) * pow(1.046, float(result_gyro_x) - 1.0)
    trim_gyro_y = (-25.0 * 131.0) * pow(1.046, float(result_gyro_y) - 1.0)
    trim_gyro_z = (25.0 * 131.0) * pow(1.046, float(result_gyro_z) - 1.0)

    # Check if error is within manufacturer tolerance
    error_accel_x = 100.0 + 100.0 * (float(result_accel_x) - trim_accel_x) / trim_accel_x
    error_accel_y = 100.0 + 100.0 * (float(result_accel_y) - trim_accel_y) / trim_accel_y
    error_accel_z = 100.0 + 100.0 * (float(result_accel_z) - trim_accel_z) / trim_accel_z
    error_gyro_x = 100.0 + 100.0 * (float(result_gyro_x) - trim_gyro_x) / trim_gyro_x
    error_gyro_y = 100.0 + 100.0 * (float(result_gyro_y) - trim_gyro_y) / trim_gyro_y
    error_gyro_z = 100.0 + 100.0 * (float(result_gyro_z) - trim_gyro_z) / trim_gyro_z
    max_error = max(error_accel_x, error_accel_y, error_accel_z, error_gyro_x, error_gyro_y, error_gyro_z)

    print("MPU-6050 error is {}%".format(max_error))
    
    # Maximum error in the datasheet is 14%
    return max_error < 14
