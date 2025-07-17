# run_test.py

import threading
import test_helper

# Sample test HTML
html_cart = """
#<item>Sneakers</item><item>Backpack</item><item>Watch</item>
<item>101 18V Cordless Drill 2 89.99 2025-07-15 14:22:35</item>
<item>102 6-inch Wood Clamp 4 12.50 2025-07-14 10:18:20</item>
<item>103 Carpenter's Hammer 1 19.99 2025-07-13 09:02:47</item>
<item>104 Adjustable Wrench Set 1 34.99 2025-07-12 16:45:01</item>
<item>105 Box of Drywall Screws 3 7.49 2025-07-11 12:30:55</item>
<item>106 Laser Distance Measurer 1 59.95 2025-07-10 08:15:22</item>
<item>107 Heavy Duty Tape Measure 2 14.25 2025-07-09 17:59:10</item>
<item>108 4-Foot Level Tool 1 24.99 2025-07-08 11:03:46</item>
<item>109 12V Cordless Impact Driver 1 109.00 2025-07-07 13:42:30</item>
<item>110 Safety Goggles (ANSI Z87) 2 6.75 2025-07-06 15:20:05</item>
"""

@test_helper.timed
def test_extract():
    results = test_helper.extract_strings_recursive(html_cart, "item")
    print("[TEST] Extracted Items (recursive):", results)
    regex_items = test_helper.extract_item_names(html_cart)
    print("[TEST] Extracted Items (regex):", regex_items)

# Test socket communication
def test_socket():
    server_thread = threading.Thread(target=test_helper.start_ingress_server, daemon=True)
    server_thread.start()
    time.sleep(1)
    test_helper.egress_to_server("Sneakers, Backpack, Watch")

# Run everything
if __name__ == "__main__":
    test_extract()
    test_socket()
    test_helper.list_process_memory()
