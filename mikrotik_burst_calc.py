#!/usr/bin/env python3
import os

class MikrotikBurstCalculator:
    """Modul inti untuk menghitung parameter Burst MikroTik"""
    def __init__(self):
        self.mbps_to_kbps = 1024

    def calculate(self, limit_mbps, scenario):
        """Menghitung parameter berdasarkan limit dasar dan skenario pilihan."""
        # Mapping Skenario
        # Format: (Burst Multiplier, Threshold Percent, Burst Time, Limit_At Percent)
        scenarios = {
            1: (2.0, 80, 16, 50),   # Aggressive: Rasa 2x lipat (seperti contoh sebelumnya)
            2: (1.5, 75, 32, 30),   # Balanced: Burst 1.5x, durasi perhitungan lebih panjang
            3: (1.25, 90, 16, 20)   # Conservative: Burst tipis, cepat kembali ke normal
        }

        if scenario not in scenarios:
            scenario = 1 # Default ke skenario 1 jika salah input

        burst_mult, thresh_pct, b_time, limit_at_pct = scenarios[scenario]

        limit_k = int(limit_mbps * self.mbps_to_kbps)
        burst_k = int(limit_mbps * burst_mult * self.mbps_to_kbps)
        thresh_k = int(limit_mbps * (thresh_pct / 100) * self.mbps_to_kbps)
        limit_at_k = int(limit_mbps * (limit_at_pct / 100) * self.mbps_to_kbps)

        return {
            "Max Limit": f"{limit_k}k",
            "Burst Limit": f"{burst_k}k",
            "Burst Threshold": f"{thresh_k}k",
            "Burst Time": f"{b_time}",
            "Limit At (CIR)": f"{limit_at_k}k"
        }

class AppUI:
    """Modul antarmuka baris perintah (CLI)"""
    def __init__(self):
        self.calculator = MikrotikBurstCalculator()

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def print_header(self):
        self.clear_screen()
        print("="*50)
        print("   MIKROTIK BURST QUEUE GENERATOR (KILOBIT)   ")
        print("="*50)

    def display_scenarios(self):
        print("\nPilih Skenario QoE (Quality of Experience):")
        print(" [1] Aggressive (Browsing Ngebut)  -> Burst 2x lipat, cepat habis (Seperti request Anda)")
        print(" [2] Balanced (Streaming Stabil)   -> Burst 1.5x lipat, kalkulasi lebih lambat")
        print(" [3] Conservative (Download Berat) -> Burst tipis 1.25x, prioritas limit ketat")

    def get_input(self):
        try:
            dl_limit = float(input("\nMasukkan Target Download Normal (Mbps) : "))
            ul_limit = float(input("Masukkan Target Upload Normal (Mbps)   : "))
            
            self.display_scenarios()
            scenario = int(input("\nPilih Skenario [1/2/3] : "))
            
            return dl_limit, ul_limit, scenario
        except ValueError:
            print("\n[Error] Harap masukkan angka yang valid!")
            return None, None, None

    def print_result_table(self, title, data):
        print(f"\n--- {title.upper()} ---")
        for key, value in data.items():
            print(f"{key.ljust(18)} : {value}")

    def run(self):
        while True:
            self.print_header()
            dl_mbps, ul_mbps, scenario = self.get_input()

            if dl_mbps is not None and ul_mbps is not None:
                dl_result = self.calculator.calculate(dl_mbps, scenario)
                ul_result = self.calculator.calculate(ul_mbps, scenario)

                print("\n" + "="*50)
                print(" HASIL KONFIGURASI WINBOX (TAB GENERAL & ADVANCED)")
                print("="*50)
                self.print_result_table("Target Download", dl_result)
                self.print_result_table("Target Upload", ul_result)
                print("="*50)

            cont = input("\nHitung lagi? (y/n): ").strip().lower()
            if cont != 'y':
                print("Selesai.\n")
                break

if __name__ == "__main__":
    app = AppUI()
    app.run()
chmod +x mikrotik_burst_calc.py
./mikrotik_burst_calc.py
