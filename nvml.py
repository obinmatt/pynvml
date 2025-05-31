import argparse
from pynvml import *

def main():
    parser = argparse.ArgumentParser(description='Adjust Nvidia GPU settings using pynvml.')
    parser.add_argument(
        '--gpu-index',
        type=int,
        default=0,
        help='Index of the GPU to adjust (default: 0)'
    )
    parser.add_argument(
        '--gpu-freq-offset',
        type=int,
        required=True,
        help='GPU frequency offset value (e.g., -502)'
    )
    parser.add_argument(
        '--mem-freq-offset',
        type=int,
        required=True,
        help='Memory frequency offset value (e.g., 2600)'
    )
    parser.add_argument(
        '--power-limit',
        type=int,
        help='Power limit in mW (e.g., 120000)'
    )
    args = parser.parse_args()

    try:
        nvmlInit()
        print("NVML initialized successfully.\n")

        try:
            myGPU = nvmlDeviceGetHandleByIndex(args.gpu_index)
            device_name = nvmlDeviceGetName(myGPU)
            print(f"Adjusting settings for GPU {args.gpu_index}: {device_name}\n")
        except NVMLError as err:
            print(f"Error getting GPU handle for index {args.gpu_index}: {err}\n")
            nvmlShutdown()
            return

        try:
            print(f"Setting GPU frequency offset to: {args.gpu_freq_offset}")
            nvmlDeviceSetGpcClkVfOffset(myGPU, args.gpu_freq_offset)
            print("GPU frequency offset applied.\n")
        except NVMLError as err:
            print(f"Error setting GPU frequency offset: {err}\n")


        try:
            print(f"Setting memory frequency offset to: {args.mem_freq_offset}")
            nvmlDeviceSetMemClkVfOffset(myGPU, args.mem_freq_offset)
            print("Memory frequency offset applied.\n")
        except NVMLError as err:
            print(f"Error setting memory frequency offset: {err}\n")


        if args.power_limit is not None:
            try:
                print(f"Setting power limit to: {args.power_limit} mW")
                nvmlDeviceSetPowerManagementLimit(myGPU, args.power_limit)
                print("Power limit applied.\n")
            except NVMLError as err:
                print(f"Error setting power limit: {err}\n")

    except NVMLError as err:
        print(f"NVML initialization failed: {err}\n")

    finally:
        try:
            nvmlShutdown()
            print("NVML shut down successfully.")
        except NVMLError as err:
            print(f"Error shutting down NVML: {err}")


if __name__ == "__main__":
    main()

