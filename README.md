# Credit Card BIN Generator and Checker

## Description
This Python project is a **Credit Card BIN Generator and Checker** designed **solely for educational purposes**. It allows users to generate credit card numbers based on a given (BIN) and check their validity using external APIs. The tool includes features for generating card details (e.g., expiry date, CVV), checking card status, and organizing results into VBV (Verified by Visa) and non-VBV categories. The project demonstrates concepts such as API integration, proxy usage, Luhn algorithm implementation, and file handling in Python.

**Important Notes**:
- This project is **for educational use only**. Any misuse, including unauthorized or illegal activities, is strictly prohibited and against the project's intent.
- Users must provide their own **proxies** and **API keys** (e.g., Stripe test/live keys, Bincodes API key) to use the checker functionality. The code includes placeholders for these keys.
- The Stripe integration is set to test mode by default and requires a valid `sk_test_` or `sk_live_` key from the Stripe Dashboard. Live key usage requires a paid Stripe account and compliance with Stripe's Terms of Service.
- The project uses a fallback Bincodes API for BIN validation, requiring a valid API key from [bincodes.com](https://bincodes.com).

## Features
- **BIN-based Card Generation**: Generate valid credit card numbers using a specified BIN, including Luhn algorithm validation.
- **Card Checking**: Verify card validity using a custom gateway (Stripe test mode) and fallback Bincodes API.
- **VBV/Non-VBV Sorting**: Categorize live cards as VBV or non-VBV based on simulated checks.
- **Proxy Support**: Load and use proxies from a `proxies.txt` file for anonymous requests.
- **File Input/Output**: Load BINs or cards from files and save live card details to JSON files in organized folders.
- **Input Validation**: Robust parsing and validation for BINs and card details.

## Requirements
- Python 3.6+
- Dependencies (install via `pip install -r requirements.txt`):
- Valid API keys:
  - Stripe test or live secret key (`sk_test_...` or `sk_live_...`) from [Stripe Dashboard](https://dashboard.stripe.com).
  - Bincodes API key from [bincodes.com](https://bincodes.com).

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/NotThushar/cc-checker-with-gen.git
   cd cc-checker-with-gen
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. For proxy add proxies in `proxies.txt`.
4. Obtain and configure API keys:
   - Replace `sk_test_your_test_key_here` in `bin_checker.py` with your Stripe test secret key.
   - Replace `your_bincodes_api_key_here` in `bin_checker.py` with your Bincodes API key.
   - Replace `pk_test_your_test_key_here` in `gatet.py` with your Stripe test public key.
5. Run the program:
   ```bash
   python run.py
   ```

## Usage
1. Launch the program with `python run.py`.
2. Choose a mode:
   - **Mode 1**: Generate and check cards from a BIN.
     - Enter a single BIN (e.g., `453201xxxxxx`) or load BINs from a file.
     - Specify the number of cards to generate per BIN.
   - **Mode 2**: Check specific cards.
     - Enter a single card (format: `CC|MM|YYYY|CVV`) or load cards from a file.
3. Results:
   - Live cards are saved as JSON files in `cc_results/vbv` or `cc_results/non_vbv`.
   - Console output shows card status (LIVE, DIE, ERROR) with VBV/non-VBV details.

## File Structure
- `run.py`: Main script with the user interface and header display.
- `bin_checker.py`: Core logic for card generation, checking, and file handling.
- `gatet.py`: Gateway function for Stripe API integration.
- `requirements.txt`: List of required Python packages.
- `proxies.txt`: User-provided file for proxy list (not included in repo).
- `cc_results/`: Output directory for live card details (created automatically).

## Disclaimer
This project is **strictly for educational purposes** to demonstrate programming techniques, API usage, and card number generation/validation algorithms. The authors are not responsible for any misuse or illegal activities conducted with this code. Users must:
- Use their own proxies and API keys.
- Comply with all applicable laws and terms of service for APIs used (e.g., Stripe, Bincodes).
- Avoid using live Stripe keys without proper authorization and compliance.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for bug fixes, improvements, or suggestions. Ensure all contributions align with the educational purpose of the project.

## License
[MIT License](LICENSE) - Free to use, modify, and distribute for educational purposes, provided the original author is credited and the disclaimer is included.
